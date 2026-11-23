# Preliminary bill of materials

**Status: not order-ready.** This is a traceable parts list for the current CAD
baseline. Items marked provisional require measurement or a purchase decision
before the corresponding final part is printed. Quantities for project-specific
screws are incomplete where the mating hardware geometry is not yet fixed.

## Electronics and purchased mechanical parts

| Item | Qty. | Status | Fit / evidence notes |
|---|---:|---|---|
| Feetech STS3215-C044 bus servo | 2 | User supplied | One pan, one tilt. Datasheet ratings and envelope are summarized in [engineering notes](engineering_notes.md). Confirm both IDs, output mode, horn spline, output-axis offset and fault-free motion before loading. |
| Waveshare bus-servo controller | 1 | User supplied | Used for bench communication. Confirm board revision, power path and firmware/software compatibility before final wiring. |
| Regulated servo supply | 1 | User supplied: 5 V / 5 A bench supply | Bench-test supply only. It is at the bottom of the servo's documented voltage range; loaded torque at 5 V is not established by the 6 V rated-torque figure. |
| Feetech-compatible 25T horn / plate | 2 | Required; actual parts unverified | One per servo. Verify spline, centre screw, plate thickness and four-hole pattern. CAD uses a simplified Ø14 mm cardinal M3 pattern. |
| 100 mm thin turntable bearing | 1 | Assumed, not selected or measured | Pan structural support. CAD uses an envelope and adjustable slots, not a supplier-specific bearing. Record actual thickness and both ring patterns before final base/deck print. |
| 608 bearing, 8 × 22 × 7 mm | 1 | Required in current CAD | Motor-side tilt radial support. The passive side now uses a printed journal instead. |
| M3 × 30 mm screws and locknuts | 4 each | Provisional assembly note | Tilt cradle/bracket/yoke clamp stack; verify actual stack length and head access on the printed parts. |
| M3 × 8 mm screws | 4 | Provisional assembly note | Tilt servo cradle lid; screw engagement and insert depth must be checked. |
| M3 heat-set inserts | 4 for lid; additional base inserts may be needed | Provisional | Verify all insert pilot locations, insert style and installed depth against the printed parts. |
| M3 screws for horn plates | 8 clearance positions total | Length not selected | Four holes per horn interface; use only after confirming actual horn plates and flange stack. Do not assume every clearance hole is populated if the purchased horn differs. |
| M4 pan-bearing fasteners | Quantity and length TBD | Depends on bearing | Base/deck slots are provisional. Match fasteners to the selected bearing's ring holes and thickness. |
| M5 yoke-to-deck fasteners | Quantity and length TBD | Provisional | Use wide washers/backing support. Confirm the actual printed joint and edge distance. |
| Thin TPU, silicone or felt pads | As required | Optional interface protection | Keep pad material clear of moving pivots and verify it does not allow the telescope to slip. |

## Printed parts

The current unique CAD parts are listed in [exports/README.md](../exports/README.md).
The pan servo rails are printed twice, so the current assembly uses twelve
printed pieces from eleven unique part files.

| Part(s) | Qty. | Baseline status |
|---|---:|---|
| base | 1 | Revised; unprinted |
| pan_deck | 1 | Existing design |
| yoke_left, yoke_right | 1 each | Existing printed parts; preserve their current hole pattern |
| servo_retainer | 2 | Existing printed rails; install at the revised base coordinates |
| pan_drive_adapter | 1 | Existing design |
| tilt_drive_socket | 1 | Existing design; verify cross and horn fits |
| tilt_passive_printed_pivot | 1 | New; print and hand-fit unloaded |
| tilt_servo_bracket | 1 | Already printed; its mounting holes and output-axis opening remain unchanged |
| tilt_servo_retainer, tilt_servo_retainer_lid | 1 each | Revised; unprinted |

## Before ordering or final printing

1. Measure both physical servo cases, output offsets, horns and mounting details.
2. Select the turntable bearing and measure its thickness and bolt patterns.
3. Verify the LEGO cross-feature type, profile, spacing and usable engagement depth.
4. Confirm the real moving assembly mass and centre of gravity.
5. Resolve whether the printed passive journal's material and clearance are suitable
   for the intended duty cycle.

Record actual manufacturer, part number, measured dimensions and any substitutions
in this file. Do not convert an assumed envelope into a purchase specification
without a physical fit check.
