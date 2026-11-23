# Verification and release plan

**Current release state: prototype only.** The model has not passed the gates
below as a complete loaded assembly. Do not mount the LEGO telescope until
interface fit, retention, balance and travel have been checked.

## Gate 0 — capture inputs

Record the design commit, CAD revision, printer, material, slicer profile,
fastener substitutions, servo IDs and supply voltage for each build.

Measure and record:

- complete moving mass, including telescope, cross adapters and any moving cradle;
- three-axis centre of gravity in the intended display configuration;
- both side-feature centres, orientation, male/female form, cross profile and
  usable engagement depth;
- both servo case envelopes, output-axis offset directions and actual horn pattern;
- the selected pan bearing's thickness and mounting-hole coordinates;
- base footprint and the worst-case telescope/panel overhang.

**Pass condition:** every interface value used to authorize a loaded build is
measured, tied to a physical part, and entered in the engineering notes or BOM.
A user estimate can guide a prototype, but is not a measured acceptance value.

## Gate 1 — interface coupons and hardware fit

Before printing a full revised assembly:

1. Print a small gauge for the LEGO cross interface from the measured profile.
   No dedicated gauge is currently included in the CAD; add and review one before
   treating the cross socket as fitted.
2. Print a journal/bore coupon using the production material and orientation.
   The current nominal sizes are Ø21.6 mm journal and Ø22 mm yoke bore; printer
   shrinkage and surface finish can change the actual sliding fit.
3. Fit each physical servo, horn, bearing and fastener to representative printed
   features. Check cable exit, tool access, screw engagement and collision with the
   case.
4. Verify the existing servo output-axis openings and associated printed
   mounting-hole locations remain unchanged.

**Pass condition:** parts seat by hand without forcing, cracking, visible
deformation, or uncontrolled looseness; the pivot rotates through the intended
range by hand. Record actual measured clearances. If the fit is not acceptable,
change the parametric source and regenerate the affected exports.

## Gate 2 — unloaded structure and retention

Assemble the base, pan bearing, deck, yokes, both tilt supports, servos, horns
and retainers without the telescope.

- Verify the bearing races are mounted to the intended stationary and moving parts.
- Verify tilt radial loads are carried by the 608 bearing and passive journal,
  not by a servo output shaft.
- Check axial retention on both tilt sides and confirm no fastener can enter a
  moving clearance.
- Rotate both axes by hand; inspect for rubbing, interference, joint play and
  wire trapping.
- Confirm each servo case is positively restrained against reaction torque.

**Pass condition:** no binding, pull-out, rocking that compromises engagement,
loose fasteners, or contact between moving and fixed structure over the
unloaded mechanical sweep.

## Gate 3 — powered unloaded motion

Test one axis at a time with no telescope attached and the mechanism clear.

- Confirm each servo's ID, position mode, soft limits and telemetry.
- Begin with small, low-speed targets; verify the physical direction matches
  the UI labels.
- Confirm release/stop behaviour and stop immediately on any servo fault.
- Do not move ID 1 again while it reports the fault recorded in the
  [hardware log](hardware-test-log.md).
- The jog application inhibits reported faults, voltage outside 5.0–8.4 V and
  temperature at or above 60 °C; these software checks are not safety-rated
  interlocks.

**Pass condition:** repeatable low-speed motion without a fault, collision,
unexpected case movement or temperature rise that requires stopping. Record
commanded/observed positions, voltage, temperature, status and settling time.

## Gate 4 — balance, torque and stability

Use a guarded dummy mass before the telescope.

The static tilt estimate is T = m g e, where m is the complete moving mass and
e is the perpendicular distance from the combined centre of gravity to the
tilt axis. Compare the result with the **rated** servo torque at the actual
operating voltage, and include cradle mass, inertia, acceleration, friction,
cable drag and a documented margin. Do not size from stall torque. The
datasheet's 6 V rated value is not a rated-torque guarantee at the user's 5 V
bench supply.

Check that the base remains stable at the worst telescope and solar-panel
orientation. A successful brief movement does not establish a safe continuous
load.

**Pass condition:** the measured balance and torque margin meet a documented
design requirement, and the base does not lift, slide or tip during a guarded,
low-speed dummy-load trial. Define the numerical margin before authorizing the
loaded test; none is yet approved for this prototype.

## Gate 5 — travel and display-load trial

Only after Gates 0–4 pass:

- Establish hard stops and software limits from the real swept envelope.
- Verify cable loops remain clear at the pan and tilt limits.
- Increase dummy load and speed in controlled increments; inspect the printed
  parts, inserts, fasteners and bearings after each stage.
- Attach the LEGO telescope only after the dummy-load procedure passes.
- Record final test conditions and remaining restrictions in the hardware log.

Stop immediately for a servo fault, binding, unexpected deflection, cracking,
fastener movement, loss of telescope engagement, cable snag or unstable base.
Power down before touching or clearing a jam.

## Test record template

Copy this block into the hardware log for each build or meaningful design change:

- Commit / CAD revision:
- Date and operator:
- Printer / material / orientation / slicer profile:
- Servo IDs / horn part numbers / controller / supply voltage:
- Bearing part number and measured dimensions:
- Moving mass and measured centre of gravity:
- Measured LEGO interface and pivot clearances:
- Axis / commanded range / speed / dummy load:
- Voltage / temperature / status before and after:
- Observed deflection, rubbing, play, wear or faults:
- Result: pass / fail / not run:
- Follow-up action:
