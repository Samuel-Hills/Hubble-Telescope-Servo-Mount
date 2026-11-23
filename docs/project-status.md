# Project status

**Revision:** current working prototype (2026-11-23)
**Use:** parametric fit prototype and low-speed bench testing; not approved for
unattended or display-load operation.

## Current design changes

- The pan servo case pocket and its base retaining-rail features are offset
  12.5 mm to align its output shaft with the fixed central base port.
- The tilt servo case cradle sits 12.5 mm below the fixed output axis. Its
  mounting holes remain aligned with the already printed tilt bracket and yoke.
- The passive tilt-side 608 bearing was removed from the assembly model and
  replaced with `tilt_passive_printed_pivot`, a 21.6 mm journal in the existing
  22 mm yoke bore.
- The old passive sleeve files are archived and are not included in the current
  assembly model.

## What is still assumed

| Item | Current value or assumption | Evidence / next check |
|---|---|---|
| Telescope mass | About 925 g without its LEGO stand | User-provided; weigh complete moving assembly |
| Tilt-feature spacing | About 105 mm | User measurement; verify pivot centers and parallelism |
| LEGO cross profile | Provisional 4.8 mm overall, 1.8 mm arm width in CAD | Measure/gauge actual features before loading |
| Cross-feature type | Current driven and passive sockets assume male cross axles | Confirm both sides; reverse socket geometry if the set presents female holes |
| Telescope centre of gravity | Unknown | Balance assembled telescope with arrays and door in display pose |
| Servo output offset | 12.5 mm from case centre per supplied C044 drawing | Confirm direction against both physical servos |
| Pan bearing | 100 mm thin turntable bearing envelope and slot pattern | Purchase/measure bearing before final base print |
| Motor-side tilt support | One 608 bearing | Still required in the current CAD; user has reported not having bearings |
| Passive-side printed pivot fit | Ø21.6 journal in nominal Ø22 yoke bore; 0.4 mm diametral clearance | Print a low-cost fit check and measure actual hole/pivot |
| Base tipping margin | Unknown | Verify on desk with full telescope at worst panel orientation |

## Open work before attaching the telescope

1. Resolve the observed ID 1 servo fault and confirm both servos move unloaded
   without binding. See `hardware-test-log.md`.
2. Confirm the user has the turntable bearing and motor-side 608 bearing, or
   design and validate printed replacements for those locations.
3. Print and hand-fit the passive pivot. It must rotate in the yoke bore without
   binding and must not rock excessively.
4. Gauge the LEGO cross interfaces with a small test coupon before printing or
   loading full-scale cross sockets.
5. Find the complete assembly's centre of gravity and check rated-torque
   margin. Do not use servo stall torque for sizing.
6. Add or verify hard travel stops, cable loops and telescope/yoke/base
   clearances over the intended pan and tilt range.
7. Run a low-speed dummy-load test with telemetry, then inspect temperature,
   plastic wear, fastener movement and joint backlash.

## Validation limits

The CAD generator has been run to export the current component set. The
passive-pivot solid is valid and has no modeled interference with the right
yoke. This is a CAD geometry check only. It does not establish bearing-like
friction, print accuracy, material strength, servo compatibility, LEGO fit,
balance or collision-free motion through ±120° pan / ±30° tilt.

## Build and validation record

The checked-in CAD export baseline was generated with CPython 3.13.14 and
CadQuery 2.8.0. The passive-pivot geometry was checked as a valid solid with no
modeled interference against the right yoke. No automated regression suite or
continuous-integration build is configured. That geometry check does not
validate print accuracy, strength, friction, servo torque, LEGO fit, stability
or the full swept motion. The release gates are listed in
[verification-plan.md](verification-plan.md).
