# Motor-control setup

## Hardware and defaults

- Board: Waveshare bus-servo controller, USB serial adapter reported as COM5.
- Bus: Feetech STS protocol at 1,000,000 baud, 8-N-1.
- Servo IDs expected by the application: 1 (pan) and 2 (tilt).
- Bench supply used in the reported test: 5 V / 5 A. Live servo telemetry
  during the test showed about 5.4–5.6 V.

Run the local jog page with `run_motor_control.bat` or:

```powershell
python src/motor_control_web.py
```

The page is served at `http://127.0.0.1:8765`. Press **Connect** before use;
connection opens COM5 but does not move a servo. Each axis has its own jog
buttons, speed and maximum travel-per-hold control. Release a button or press
**Stop all** to end a jog. The server also stops its jog targets on page blur,
page hiding and disconnect.

The server blocks a new jog if telemetry is missing, reports a nonzero status,
falls outside 5.0–8.4 V, or reports 60 °C or more. This is only software
guarding. Keep the mechanism unloaded and physically clear; do not use this
page as a safety controller or as a hard travel stop.

## Read-only check and prompted move

The default script is read-only:

```powershell
python src/test_servos.py --port COM5 --ids 1 2
```

To make a small prompted test move for one servo, the script supports
`--move ID`. It requests typing `MOVE` before issuing an out-and-back target.
Only use it with the mechanism unloaded and known to be clear. Do not repeat a
move while a servo reports a fault; the position write may clear a latched
protection flag and immediately retry against the obstruction.

## Fault response

If the page shows **FAULT**, release all buttons and stop further motion. Check
whether the horn, printed part, wire or load is binding. If the servo buzzes,
pushes against a stop, or heats under load, switch off servo power before
handling the mechanism. Do not force the output by hand while powered.

The control UI reports any nonzero servo status as `FAULT`; it does not decode
individual causes. A `hold limit reached` message means the software stopped a
single held jog at its configured per-hold limit or at the 0/4095 single-turn
position boundary. That message is separate from a servo-reported fault.

For captured bench telemetry, including the recent ID 1 status `0x20`, see
[`hardware-test-log.md`](hardware-test-log.md). The servo datasheet documents
overload and thermal protection in `reference/`.
