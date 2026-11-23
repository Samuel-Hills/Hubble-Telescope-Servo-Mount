"""Read and gently bench-test Feetech STS3215 servos on a serial bus.

Default is read-only. To make a small out-and-back test move, pass --move.
The WaveShare Bus Servo Adapter (A) uses the same UART protocol as the STS
servos; default link settings are COM3 and 1,000,000 baud.
"""
import argparse
import struct
import sys
import time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    print("pyserial is required. Install with: python -m pip install pyserial")
    raise SystemExit(2)


BAUD = 1_000_000
TELEMETRY_ADDRESS = 0x38
GOAL_ADDRESS = 0x2A
POSITION_COUNTS = 4096
MIN_SERVO_V = 5.0
MAX_SERVO_V = 8.4


def packet(servo_id, instruction, params=b""):
    length = len(params) + 2
    checksum = (~(servo_id + length + instruction + sum(params))) & 0xFF
    return bytes((0xFF, 0xFF, servo_id, length, instruction)) + params + bytes((checksum,))


def read_response(port, servo_id, timeout=0.10):
    """Read one checksum-valid response packet from the requested servo ID."""
    deadline = time.monotonic() + timeout
    buf = bytearray()
    while time.monotonic() < deadline:
        chunk = port.read(1)
        if not chunk:
            continue
        buf += chunk
        while len(buf) >= 2 and buf[:2] != b"\xff\xff":
            del buf[0]
        if len(buf) < 4:
            continue
        if buf[2] != servo_id:
            del buf[0]
            continue
        total = buf[3] + 4
        if total < 6 or total > 64:
            del buf[0]
            continue
        if len(buf) < total:
            continue
        frame = bytes(buf[:total])
        del buf[:total]
        if ((sum(frame[2:-1]) + frame[-1]) & 0xFF) != 0xFF:
            continue
        return frame
    return None


def exchange(port, servo_id, instruction, params=b"", timeout=0.10):
    port.reset_input_buffer()
    port.write(packet(servo_id, instruction, params))
    port.flush()
    return read_response(port, servo_id, timeout)


def ping(port, servo_id):
    frame = exchange(port, servo_id, 0x01)
    if frame is None:
        return None
    return frame[4]


def telemetry(port, servo_id):
    # ST memory map 0x38..0x3F: position, speed, load, voltage, temperature.
    frame = exchange(port, servo_id, 0x02, bytes((TELEMETRY_ADDRESS, 8)), timeout=0.20)
    if frame is None or len(frame) != 14:
        return None
    status = frame[4]
    data = frame[5:-1]
    raw_pos = struct.unpack_from("<H", data, 0)[0]
    pos = raw_pos & 0x7FFF
    voltage = data[6] / 10.0
    temperature = data[7]
    return {"status": status, "raw_position": raw_pos, "position": pos,
            "voltage": voltage, "temperature": temperature}


def write_position(port, servo_id, position, speed):
    # ST-series goal block: position(2), reserved(2), speed(2), little-endian.
    params = bytes((GOAL_ADDRESS,)) + struct.pack("<HHH", position, 0, speed)
    return exchange(port, servo_id, 0x03, params, timeout=0.20)


def write_byte(port, servo_id, address, value):
    return exchange(port, servo_id, 0x03, bytes((address, value)), timeout=0.20)


def change_id(port, old_id, new_id):
    """Persist a new ID using the ST-series EPROM unlock/write/relock sequence."""
    if old_id == new_id:
        raise RuntimeError("Old and new IDs are identical")
    if ping(port, new_id) is not None:
        raise RuntimeError(f"ID {new_id} already responds; refusing to create duplicate IDs")
    if ping(port, old_id) is None:
        raise RuntimeError(f"Old ID {old_id} did not respond; refusing to change ID")

    print(f"\nChanging the isolated servo ID {old_id} -> {new_id} (stored in servo EPROM).")
    print("Only one servo may be connected while changing its ID.")
    if input(f"Type SET ID {old_id} TO {new_id} to continue: ").strip() != f"SET ID {old_id} TO {new_id}":
        print("Cancelled; no ID setting commands sent.")
        return False

    # ST-series memory map: lock flag 0x37, servo ID 0x05. The official
    # sequence unlocks under the old ID, writes the new ID, then relocks at it.
    unlock = write_byte(port, old_id, 0x37, 0)
    if unlock is None or unlock[4] != 0:
        raise RuntimeError("EPROM unlock was not acknowledged; ID unchanged")
    port.reset_input_buffer()
    port.write(packet(old_id, 0x03, bytes((0x05, new_id))))
    port.flush()
    time.sleep(0.08)
    port.reset_input_buffer()
    if ping(port, new_id) is None:
        raise RuntimeError(f"ID {new_id} did not answer after change; stop and keep this servo isolated")

    lock = write_byte(port, new_id, 0x37, 1)
    if lock is None or lock[4] != 0:
        raise RuntimeError(f"ID {new_id} responds, but EPROM relock was not acknowledged")
    if ping(port, old_id) is not None:
        raise RuntimeError(f"Old ID {old_id} still responds; verify the servo bus before connecting another")
    print(f"ID change confirmed: servo now responds at ID {new_id} only.")
    return True


def show_state(servo_id, state):
    print(f"ID {servo_id}: position={state['position']} counts, "
          f"voltage={state['voltage']:.1f} V, temperature={state['temperature']} C, "
          f"status=0x{state['status']:02X}")


def do_test_move(port, servo_id, state, degrees, speed):
    if state["status"] != 0:
        raise RuntimeError(f"ID {servo_id} reports servo fault/status 0x{state['status']:02X}; refusing to move")
    if not MIN_SERVO_V <= state["voltage"] <= MAX_SERVO_V:
        raise RuntimeError(f"ID {servo_id} reports {state['voltage']:.1f} V; outside the specified 5.0-8.4 V range")
    if state["temperature"] >= 60:
        raise RuntimeError(f"ID {servo_id} is already at {state['temperature']} C; refusing to move")

    origin = state["position"]
    delta_counts = max(1, round(degrees / 0.0879))
    delta = delta_counts if origin <= POSITION_COUNTS - delta_counts - 1 else -delta_counts
    target = origin + delta
    print(f"\nID {servo_id}: test move {origin} -> {target} -> {origin} "
          f"(about {degrees:g} degrees each way at {speed} steps/second).")
    print("If multiple servos share this ID, they will all receive the same command.")
    print("Only continue with unloaded servo horns and clear movement around them.")
    if input("Type MOVE to perform this out-and-back test: ").strip() != "MOVE":
        print("Cancelled; no movement command sent.")
        return

    result = write_position(port, servo_id, target, speed)
    if result is None:
        raise RuntimeError("No acknowledgement to the move command; stopping without a return command")
    if result[4] != 0:
        raise RuntimeError(f"Servo rejected move with status 0x{result[4]:02X}")
    time.sleep(max(1.0, abs(target - origin) / speed * 1.5 + 0.3))
    moved = telemetry(port, servo_id)
    if moved is None:
        raise RuntimeError("Lost telemetry after the test move; not sending another target")
    show_state(servo_id, moved)
    # Return only if voltage/status are still acceptable.
    if moved["status"] != 0 or not MIN_SERVO_V <= moved["voltage"] <= MAX_SERVO_V:
        raise RuntimeError("Servo reported a fault or out-of-range voltage; leaving the current target unchanged")
    result = write_position(port, servo_id, origin, speed)
    if result is None or result[4] != 0:
        raise RuntimeError("No valid acknowledgement to return command")
    time.sleep(max(1.0, abs(target - origin) / speed * 1.5 + 0.3))
    final = telemetry(port, servo_id)
    if final:
        print("Returned to the original target:")
        show_state(servo_id, final)


def main():
    ap = argparse.ArgumentParser(description="Read or gently test Feetech STS3215 servos")
    ap.add_argument("--port", default="COM5", help="USB serial port (default: COM5)")
    ap.add_argument("--baud", type=int, default=BAUD, help="servo-bus baud rate (default: 1000000)")
    ap.add_argument("--ids", type=int, nargs="+", default=[1, 2], help="servo IDs to check (default: 1 2)")
    ap.add_argument("--move", type=int, metavar="ID", help="make a prompted out-and-back test move for this ID")
    ap.add_argument("--degrees", type=float, default=1.76, help="test move angle each way (default: 1.76)")
    ap.add_argument("--speed", type=int, default=50, help="speed in ST servo steps/second (default: 50)")
    ap.add_argument("--set-id", type=int, metavar="OLD_ID", help="persistently change the ID of one isolated servo")
    ap.add_argument("--to", type=int, metavar="NEW_ID", help="new ID used with --set-id")
    args = ap.parse_args()
    if (args.set_id is None) != (args.to is None):
        ap.error("--set-id and --to must be used together")
    if args.degrees <= 0 or args.degrees > 180:
        ap.error("--degrees must be greater than 0 and no more than 180")
    if args.speed < 1 or args.speed > 1000:
        ap.error("--speed must be in the range 1..1000 steps/second")
    ids = args.ids + ([args.move] if args.move is not None else []) + ([args.set_id, args.to] if args.set_id is not None else [])
    ids = list(dict.fromkeys(ids))
    if any(i < 0 or i > 253 for i in ids):
        ap.error("IDs must be in the range 0..253")

    print(f"Opening {args.port} at {args.baud} baud, 8-N-1")
    try:
        with serial.Serial(args.port, args.baud, bytesize=8, parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE, timeout=0.01, write_timeout=0.2) as port:
            found = []
            for servo_id in ids:
                try:
                    result = ping(port, servo_id)
                except serial.SerialException as exc:
                    raise RuntimeError(f"Serial I/O error: {exc}") from exc
                if result is None:
                    print(f"ID {servo_id}: no PING response")
                    continue
                print(f"ID {servo_id}: PING response, status=0x{result:02X}")
                state = telemetry(port, servo_id)
                if state is None:
                    print(f"ID {servo_id}: could not read telemetry (check duplicate IDs / bus wiring)")
                    continue
                show_state(servo_id, state)
                found.append((servo_id, state))

            if not found:
                print("No responding servos. No motion commands were sent.")
                return 1
            states = dict(found)
            if args.set_id is not None:
                old_state = states.get(args.set_id)
                if old_state is None:
                    print(f"ID {args.set_id} did not return valid telemetry; refusing to change ID.")
                    return 1
                if not change_id(port, args.set_id, args.to):
                    return 0
                new_state = telemetry(port, args.to)
                if new_state is None:
                    raise RuntimeError(f"ID {args.to} answers PING, but telemetry is invalid")
                show_state(args.to, new_state)
                states[args.to] = new_state
            if args.move is not None:
                match = states.get(args.move)
                if match is None:
                    print(f"ID {args.move} did not return valid telemetry; refusing to move.")
                    return 1
                do_test_move(port, args.move, match, args.degrees, args.speed)
            else:
                print("Read-only check complete. No movement commands were sent.")
                print("To make a small prompted test move, rerun with --move ID after checking the setup.")
    except (serial.SerialException, OSError) as exc:
        print(f"Could not open/use {args.port}: {exc}")
        return 1
    except RuntimeError as exc:
        print(f"STOP: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
