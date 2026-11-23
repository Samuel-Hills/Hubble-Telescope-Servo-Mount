# Hardware test log

This records user-observed bench results in this project conversation. Readings
are snapshots, not a complete diagnostic trace. Times were not recorded.

## 2026-11-23 — two-servo bench check

**Setup:** Waveshare controller on COM5 at 1 Mbaud, two STS3215 servos at IDs
1 and 2, bench supply set to 5 V / 5 A. Both servos answered ping and telemetry.

### Before jog

| ID | Position | Voltage | Temperature | Status |
|---:|---:|---:|---:|---|
| 1 | 3431 / 4095 | 5.5 V | 27 °C | 0x00 |
| 2 | 2201 / 4095 | 5.6 V | 22 °C | 0x00 |

A commanded approximately 20° out-and-back jog used 350 position counts/s.
The acknowledgement was received, but ID 1 did not return to its starting
position during the observed window. ID 2 returned close to its start. This
test should not be treated as a successful repeatable motion test.

### Later controller snapshots

The user later reported ID 1 at 3998/4095 with 5.5 V, 39 °C and `FAULT`, then
at 2710/4095 with 5.5 V, 42 °C and `FAULT`. A direct read of the local jog
server at the latter state showed:

| ID | Position | Voltage | Temperature | Raw status | Jog active |
|---:|---:|---:|---:|---:|---|
| 1 | 2710 / 4095 | 5.5 V | 42 °C | 0x20 | No |
| 2 | 3053 / 4095 | 5.6 V | 23 °C | 0x00 | No |

The app labels every nonzero status as `FAULT`; it does not decode status bits.
Treat ID 1 as faulted and do not command more motion until it is unloaded and
the source of resistance is found. The available telemetry does not identify
whether the cause is a hard stop, binding, excessive load or another servo
condition. The state log is not evidence that the CAD mechanism itself caused
the fault.

## Next safe diagnostic sequence

1. Keep the Hubble and all printed load off the servos. Switch servo power off
   before inspecting the output and cable path.
2. Verify the horn can move through the intended small test range without
   touching the cradle, yoke, base or a wire.
3. With the mechanism unloaded and clear, restore power and read both IDs only.
   If ID 1 still reports a fault, do not jog it; consult Feetech documentation
   or inspect the servo independently.
4. Record the commanded target, observed position after settling, status,
   voltage and temperature for each later test.
