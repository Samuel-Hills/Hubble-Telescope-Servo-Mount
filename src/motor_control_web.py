"""Tiny localhost web controller for two Feetech STS3215 servos.

Run from the project root with `python src/motor_control_web.py`.
The browser UI only sends position-mode jog targets while a button is held.
"""
from __future__ import annotations

import json
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

try:
    import serial
except ImportError as exc:
    raise SystemExit("pyserial is required. Install with: python -m pip install pyserial") from exc

import test_servos as st

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "web" / "motor_control.html"
HOST = "127.0.0.1"
PORT = 8765
SERVO_IDS = (1, 2)


class ServoController:
    def __init__(self):
        self.lock = threading.RLock()
        self.port = None
        self.port_name = "COM5"
        self.servo_ids: set[int] = set()
        self.jogs: dict[int, dict] = {}
        self.last_error = ""

    def _require_port(self):
        if self.port is None or not self.port.is_open:
            raise RuntimeError("Connect to the servo controller first.")

    def connect(self, port_name: str):
        name = (port_name or "COM5").strip() or "COM5"
        with self.lock:
            self.disconnect()
            try:
                link = serial.Serial(name, st.BAUD, bytesize=8, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE, timeout=0.01,
                                     write_timeout=0.2)
                found = set()
                for servo_id in SERVO_IDS:
                    if st.ping(link, servo_id) is not None and st.telemetry(link, servo_id) is not None:
                        found.add(servo_id)
                if not found:
                    link.close()
                    raise RuntimeError(f"No valid servo response on {name}. Check power, bus wiring and IDs 1/2.")
                self.port = link
                self.port_name = name
                self.servo_ids = found
                self.last_error = ""
            except (serial.SerialException, OSError) as exc:
                raise RuntimeError(f"Could not open {name}: {exc}") from exc
        return self.status()

    def disconnect(self):
        with self.lock:
            if self.port is not None:
                for servo_id in list(self.jogs):
                    self._stop_locked(servo_id)
                try:
                    self.port.close()
                except Exception:
                    pass
            self.port = None
            self.servo_ids.clear()
            self.jogs.clear()

    def status(self):
        with self.lock:
            if self.port is None or not self.port.is_open:
                return {"connected": False, "port": self.port_name, "servos": [], "error": self.last_error}
            states = []
            for servo_id in SERVO_IDS:
                if servo_id not in self.servo_ids:
                    states.append({"id": servo_id, "online": False, "jogging": False})
                    continue
                state = st.telemetry(self.port, servo_id)
                if state is None:
                    states.append({"id": servo_id, "online": False, "jogging": servo_id in self.jogs})
                else:
                    states.append({"id": servo_id, "online": True, "jogging": servo_id in self.jogs,
                                   **state})
            return {"connected": True, "port": self.port_name, "servos": states,
                    "error": self.last_error}

    def _read_safe_state(self, servo_id: int):
        self._require_port()
        if servo_id not in self.servo_ids:
            raise RuntimeError(f"Servo ID {servo_id} is not responding.")
        state = st.telemetry(self.port, servo_id)
        if state is None:
            raise RuntimeError(f"Lost telemetry from servo ID {servo_id}; no new jog command sent.")
        if state["status"] != 0:
            raise RuntimeError(f"Servo ID {servo_id} reports fault 0x{state['status']:02X}; jog blocked.")
        if not st.MIN_SERVO_V <= state["voltage"] <= st.MAX_SERVO_V:
            raise RuntimeError(f"Servo ID {servo_id} reports {state['voltage']:.1f} V; jog blocked.")
        if state["temperature"] >= 60:
            raise RuntimeError(f"Servo ID {servo_id} is {state['temperature']} C; jog blocked.")
        return state

    def start_jog(self, servo_id: int, direction: int, speed: int, limit_deg: float):
        servo_id = int(servo_id)
        direction = int(direction)
        speed = max(10, min(1000, int(speed)))
        limit_deg = max(1.0, min(180.0, float(limit_deg)))
        if servo_id not in SERVO_IDS or direction not in (-1, 1):
            raise ValueError("Invalid servo or direction.")
        with self.lock:
            if servo_id in self.jogs:
                raise RuntimeError(f"Servo ID {servo_id} is already jogging.")
            state = self._read_safe_state(servo_id)
            now = time.monotonic()
            self.jogs[servo_id] = {
                "start": state["position"], "target": state["position"],
                "direction": direction, "speed": speed,
                "limit": max(1, round(limit_deg * st.POSITION_COUNTS / 360)),
                "fraction": 0.0, "last": now,
            }
            return {"id": servo_id, "position": state["position"], "active": True}

    def jog_tick(self, servo_id: int):
        servo_id = int(servo_id)
        with self.lock:
            self._require_port()
            jog = self.jogs.get(servo_id)
            if jog is None:
                return {"id": servo_id, "active": False}
            now = time.monotonic()
            dt = max(0.0, min(0.12, now - jog["last"]))
            jog["last"] = now
            exact = jog["speed"] * dt + jog["fraction"]
            step = int(exact)
            jog["fraction"] = exact - step
            if step < 1:
                return {"id": servo_id, "active": True, "target": jog["target"]}

            lo = max(0, jog["start"] - jog["limit"])
            hi = min(st.POSITION_COUNTS - 1, jog["start"] + jog["limit"])
            target = max(lo, min(hi, jog["target"] + jog["direction"] * step))
            if target == jog["target"]:
                self.jogs.pop(servo_id, None)
                return {"id": servo_id, "active": False, "target": target, "limit": True}
            result = st.write_position(self.port, servo_id, target, jog["speed"])
            if result is None or result[4] != 0:
                self.jogs.pop(servo_id, None)
                raise RuntimeError(f"Servo ID {servo_id} did not acknowledge the jog target; jogging stopped.")
            jog["target"] = target
            reached = target in (lo, hi)
            if reached:
                self.jogs.pop(servo_id, None)
            return {"id": servo_id, "active": not reached, "target": target, "limit": reached}

    def _stop_locked(self, servo_id: int):
        jog = self.jogs.pop(servo_id, None)
        if jog is None or self.port is None or not self.port.is_open:
            return
        state = st.telemetry(self.port, servo_id)
        if state is not None:
            # Cancel the small remaining jog by targeting the measured position.
            st.write_position(self.port, servo_id, state["position"], jog["speed"])

    def stop_jog(self, servo_id: int):
        servo_id = int(servo_id)
        with self.lock:
            self._stop_locked(servo_id)
            return {"id": servo_id, "active": False}

    def stop_all(self):
        with self.lock:
            for servo_id in list(self.jogs):
                self._stop_locked(servo_id)
            return {"active": False}


controller = ServoController()


class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _body(self):
        length = min(int(self.headers.get("Content-Length", "0")), 8192)
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/status":
            try:
                return self._json(200, controller.status())
            except Exception as exc:
                return self._json(500, {"error": str(exc)})
        if path in ("/", "/index.html"):
            data = PAGE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self._json(404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = self._body()
            if path == "/api/connect":
                result = controller.connect(body.get("port", "COM5"))
            elif path == "/api/disconnect":
                controller.disconnect()
                result = {"connected": False}
            elif path == "/api/jog/start":
                result = controller.start_jog(body["id"], body["direction"], body["speed"], body["limit_deg"])
            elif path == "/api/jog/tick":
                result = controller.jog_tick(body["id"])
            elif path == "/api/jog/stop":
                result = controller.stop_jog(body["id"])
            elif path == "/api/stop-all":
                result = controller.stop_all()
            else:
                return self._json(404, {"error": "Not found"})
            self._json(200, result)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            self._json(400, {"error": f"Invalid request: {exc}"})
        except Exception as exc:
            controller.last_error = str(exc)
            self._json(409, {"error": str(exc)})

    def log_message(self, fmt, *args):
        print("[web] " + fmt % args)


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}/"
    print(f"Hubble motor control: {url}")
    print("Use Connect in the page to open COM5. No servo motion is sent until a jog button is held.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.disconnect()
        server.server_close()


if __name__ == "__main__":
    main()
