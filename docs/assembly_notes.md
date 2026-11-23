# Prototype assembly plan

This sequence is for a low-speed dummy-load prototype. Do not mount the LEGO
telescope until the fit, balance, retention and range checks below are complete.

## Purchased hardware

- 2 × Feetech STS3215-C044 servos, operated from a regulated supply sized for
  their current draw. Datasheet rated current is 1.0 A at 6 V / 1.2 A at 7.4 V;
  stall current is higher (3.2 / 3.8 A), so size the supply and wiring for peaks.
- 1 × thin 100 mm turntable bearing (lazy-Susan style), purchased before the
  final base/deck print so its mounting pattern can be checked.
- 1 × 608 bearing, 8 × 22 × 7 mm, for the motor-side tilt pivot. The passive
  side uses `tilt_passive_printed_pivot` directly in the yoke bore.
- Axial retainers for the side trunnions. Consider metal 8 mm journals for a
  durable build; the current journals are printed fit prototypes.
- 25T servo horns compatible with the actual Feetech output; verify spline and
  screw before ordering. The datasheet lists a 25T, Ø5.9 mm output and M3×6 screw.
- M3, M4 and M5 screws, washers and locknuts; heat-set inserts or captive nuts.
- Tilt-servo case retainer: 4 × M3 × 30 mm screws and locknuts to pass through
  the retainer flange, existing bracket and yoke; 4 × M3 heat-set inserts and
  4 × M3 × 8 mm screws for the removable cradle lid.
- Thin TPU, silicone or felt pads for the LEGO contact surfaces.

## Intended stack

1. Install heat-set M3 inserts in the base pilots. Seat the pan servo in its
   underside bay and install two `servo_retainer` rails (print the part twice).
   The rails support the case and screw into the inserts; add thin pads and do
   not let the cable pinch.
   The revised bay and its rail seats are offset 12.5 mm from the fixed pan
   output axis to match the datasheet case-to-output offset. The bearing and
   centred output port remain on the original axis. The `servo_retainer` STL is
   unchanged; align its installed position with the shifted base pilots.
2. Fasten the stationary bearing ring to the base radial slots. Keep the bearing
   centred on the vertical servo axis.
3. Fasten `pan_deck` to the rotating bearing ring. The bearing carries the stand
   weight; the servo horn and `pan_drive_adapter` transmit torque only.
4. Fit the yoke uprights to the pan deck using M5 fasteners and wide washers.
   Keep the yoke's nominal 22 mm tilt bores clear; the passive printed pivot
   replaces the right-side bearing.
5. Seat the 608 bearing in the motor-side yoke arm and install the keyed left
   trunnion. Insert `tilt_passive_printed_pivot` into the opposite yoke bore.
   The trunnion and yokes carry radial load; do not rely on the servo output
   shaft to support the telescope. Check the printed pivot turns freely before
   attaching the model.
6. Mount the tilt servo and bracket outside the left yoke arm. Couple the selected
   25T horn to the left trunnion flange after confirming the spline, screw and
   axial stack. The left trunnion cross socket engages one side cross feature.
7. Fit the telescope's opposite cross feature into the female socket of
   `tilt_passive_printed_pivot`. Its round journal turns directly in the right
   yoke's printed 22 mm bore. The nominal axis spacing is 105 mm. Confirm the
   cross profile, axis height, sliding fit and engagement with the physical
   LEGO feature before attaching the model.

## Bearing-free passive-side pivot

`tilt_passive_printed_pivot` replaces the passive-side 608 bearing and the
earlier thin sleeves. Its 21.6 mm round journal sits directly in the existing
nominal 22 mm yoke bore; a 26 mm flange retains it axially. A blind female
cross socket accepts the LEGO side feature. Both the journal and yoke are
printed plastic, so expect more friction and wear than a real bearing. Print
and test the pivot unloaded first. Adjust `PASSIVE_PIVOT_OD` and the cross
clearance in `src/hubble_stand.py` if the fit binds or rattles. This change
replaces only the passive-side tilt bearing: the current motor-side tilt design
still calls for one 608 bearing.

## Fit and motion checks

1. Check the servo outline against the supplied STEP and physical servo. Adjust
   the bay and retainer before installing electronics.
2. Confirm the turntable and motor-side tilt bearings rotate freely with
   fasteners tightened. Check that the passive printed pivot moves freely in
   the yoke bore and that no flange or fastener rubs.
3. Turn each pivot by hand through its full proposed range with no telescope.
   Add physical stops that keep wiring, yoke and adapter clear.
4. Fit a 0.925 kg dummy load, then the measured cradle mass. Test at low speed,
   first balanced and then with small known CG offsets. Record current, case
   temperature, backlash and any plastic flex after each trial.
5. Only proceed if the combined tilt CG is close to the pivot and the rated
   torque margin remains adequate. Tune acceleration and software limits before
   attaching the LEGO build.

The assembly STEP is an envelope/layout illustration: purchased parts appear as
simplified shapes, the cradle is shown nominally level, and it does not prove
collisions or clearances at ±120° pan / ±30° tilt. `visual_model.glb` adds a
simple Hubble body, solar-panel envelope and two stylized side cross-feature blocks
for viewing; the telescope is not brick-accurate. The nominal 105 mm side-pivot spacing is represented in the yoke CAD.
Swept-clearance checks depend on the real telescope geometry.

## Driven cross adapter and horn interface

`tilt_drive_socket` is the printed part for the driven telescope side. Its female
cross-shaped bore faces inward toward the telescope and passes through the full
15.5 mm length of the round journal, stopping at the solid horn flange. The
nominal LEGO cross axle enters from the telescope side. The 7.8 mm round journal
passes through the left 608 bearing inner race, so the bearing carries radial load. The outer
21.6 mm flange has four M3 clearance holes at the cardinal points on a 14 mm
pitch circle, matching the Feetech STS3215 accessory drawing.

The viewer shows `tilt_servo_horn_reference` as a simplified purchased 25T metal
horn. The horn plate sits against the printed flange; four M3 screws connect the
plate to the printed part. Its four-hole pattern follows the Ø14 cardinal pattern
in Feetech's STS3215 accessory drawing. The spline, hub and other plate details
are visualization envelopes, not a verified C044 horn model. Check the actual
horn and the real LEGO cross axle before printing the final coupling. The CAD currently shows the
nominal flange/horn stack aligned and the journal inside the 608 bearing; this is
not a physical fit test.

## Tilt-servo case retainer add-on

`tilt_servo_retainer` and `tilt_servo_retainer_lid` are printable add-on parts;
they do not require changing the already printed `tilt_servo_bracket`. The
open-top cradle surrounds the servo case, has a rear stop with a cable exit, and
registers to the servo envelope. Its front flange sits against the outboard face
of the existing bracket, with four holes aligned to that bracket's existing
slots and the yoke holes. Replace the four bracket-to-yoke screws with longer
M3 × 30 mm screws and locknuts so they clamp the retainer flange, bracket and
yoke as one stack. The cradle's separate lid closes over the servo with four
M3 × 8 mm screws into heat-set inserts in the cradle rails.

The revised tilt case seat is 12.5 mm below the fixed servo output axis to
follow the C044 datasheet offset in the selected orientation. The retainer
flange and all four mounting holes stay on the original bracket/yoke pattern;
the already printed `tilt_servo_bracket` is not changed. Check that the output
shaft and horn pass through the original bracket aperture before tightening the
long through-bolts.

The CAD envelope gives the case approximately 0.6 mm clearance per side. Check
the real servo case, connector/cable exit and screw-head access before printing;
add thin TPU pads if the case rattles. The rectangular cradle resists case
rotation by shape, while the rear stop prevents it sliding outward. The servo
output shaft remains clear and carries torque only.
