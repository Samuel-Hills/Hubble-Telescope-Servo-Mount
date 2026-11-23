# Engineering notes

## Evidence and assumptions

| Item | Known from supplied files | Current treatment |
|---|---|---|
| Telescope mass | User supplied: 0.925 kg without LEGO stand | Use as minimum moving mass. Add the moving cradle/adapter mass when measured. |
| Telescope envelope | Approx. 380 × 380 × 320 mm was recorded from a product listing in earlier notes; the exact source URL is not archived | Reserve a wide open clearance zone. The envelope is not a swept-volume model. |
| Telescope geometry / CG | Not dimensioned in the supplied instructions | Must locate by balancing the assembled model with solar panels installed. |
| Telescope-side interface | User reports two LEGO cross-shaped features on opposite sides, about 105 mm centre-to-centre, near the telescope centre of mass | Side-to-side horizontal tilt axis through the U-yoke. Driven side uses an axial cross socket; the passive side uses a printed cross pivot with a round journal running directly in the yoke bore. Current sockets assume male cross axles project sideways; reverse the interface if the actual model has female holes. |
| Servo body | Datasheet: 45.2 × 24.7 × 35 mm; STEP bounding box: 45.22 × 37.8 × 24.72 mm including protrusions | Bay uses the nominal body envelope with 0.6 mm clearance; check actual printed fit and case orientation. The detailed STEP has invalid solids in the original file, so the assembly layout uses a clean simplified envelope instead. |
| Servo output-axis offset | The supplied C044 datasheet drawing places the output axis 12.5 mm from the centre of the 45.2 mm case dimension | CAD seats each case using this offset. Pan case and unchanged retainer rails shift 12.5 mm in X while the base output port remains at (0,0). Tilt case sits 12.5 mm below its fixed output axis; the retainer flange retains the existing bracket/yoke bolt coordinates. Verify offset direction against each physical servo before assembly. |
| Servo output | C044 datasheet: 25T, Ø5.9 mm, M3×6 centre screw; STS3215 accessory drawing shows 4-M3 on Ø14 cardinal pitch | Both pan and tilt adapters now use four M3 clearance holes on Ø14 pitch. Verify the actual C044 horn plate before final printing. |
| Servo mounting | Datasheet drawing shows case and screw features; no fully dimensioned hole table | Mount slots are provisional. Measure the physical case/hole centres before drilling or printing a final clamp. |
| Pan bearing | Not supplied | Assumed 100 mm thin turntable bearing, with separate radial slot patterns centred at 44 mm (base/outer race) and 31 mm (deck/inner race). Buy bearing first and check its actual hole layout and thickness. |
| Tilt support | Not supplied | The motor side still uses the existing 608 bearing and driven trunnion. The passive side now uses a printed 21.6 mm journal directly in the yoke's nominal 22 mm bore; fit/friction must be checked because both contact surfaces are printed. |
| Cross-pin profile | Not specified by the user or supplied drawings | Editable provisional female sockets: 4.8 mm overall cross size and 1.8 mm arm width. The driven socket is through-bored; the passive printed pivot has a 12 mm blind socket. Print a fit gauge and measure the actual feature before use. |
| Material | Not specified | PETG or PA for structural parts; use 5+ perimeters and 35–50% infill as a starting prototype setting. Avoid brittle PLA for loaded pivots. |

The supplied 3D file is the servo, not a telescope. The LEGO PDF is a visual
assembly guide and parts inventory, not a dimensioned model. No exact LEGO
attachment dimensions have been inferred from its perspective illustrations.

## Servo rating and torque

Datasheet values relevant to sizing:

- Supply range: 5–8.4 V; rated operation values listed at 6 V and 7.4 V.
- Rated torque: 8 kg·cm at 6 V; 9 kg·cm at 7.4 V.
- Stall torque: 24.3 / 27.4 kg·cm. **Do not use this for continuous design sizing.**
- Single-turn position mode: 0–360° over command values 0–4095; 0.088°/count.
- Multi-loop mode supports up to ±7 turns, but turn count does not survive power loss.
- Datasheet calls the output “no limit”; position control range/mode must be configured.

Rated torque in SI units:

| Supply | Rated torque |
|---|---:|
| 6 V | 8 kg·cm = 0.785 N·m |
| 7.4 V | 9 kg·cm = 0.883 N·m |

Static gravity torque about the tilt axis is `T = m g e`, where `e` is the
perpendicular distance between the combined moving centre of gravity and the
tilt axis. For the telescope alone (0.925 kg):

| CG offset `e` | Telescope-only gravity torque |
|---:|---:|
| 10 mm | 0.091 N·m |
| 30 mm | 0.272 N·m |
| 50 mm | 0.454 N·m |
| 100 mm | 0.907 N·m |

At 6 V, the rated-torque-only offset limit for the telescope alone is about
86 mm. That is not an acceptable design target: it leaves no allowance for the
printed cradle, acceleration, bearing friction, cable drag, manufacturing
variation or a safety margin.

As an initial sizing example only, assume 0.20 kg of cradle/adapter with its
centre 40 mm from the pivot. That contributes about 0.078 N·m. With a 2:1
static margin against the 6 V rated torque, the combined load budget is
0.392 N·m; the telescope CG then needs to be within about 35 mm of the pivot.
This simple calculation omits inertia and dynamic loads. The practical target
is to balance the real complete moving assembly within 10–15 mm, and verify
tilt holding and temperature at a deliberately limited speed.

The pan axis is vertical, so gravity creates no ideal pan torque. Pan motor
load is set by rotational inertia, acceleration, bearing drag, wire routing,
and any CG eccentricity. The 380 mm model envelope makes low acceleration and
clearance checking important.

## Motion limits and controls

- Pan target: software-limited to ±120° from a calibrated centre. This fits
  within the servo's single-turn 0–360° range if centre is set near 180°.
- Tilt target: software-limited to ±30° around the measured balanced position.
- Add independent physical travel stops after the final LEGO envelope is known;
  the current CAD contains no hard stops because their locations need the real
  model and swept-clearance checks.
- Keep wiring near the pan axis and provide a controlled loop around tilt. Do
  not rely on continuous rotation: the intended move range is bounded.
- Use the servo's reported position, load, current and temperature telemetry.
  Configure current/overload protection and stop motion on a fault.
- Do not treat the servo's internal overload protection as a mechanical brake.

## Print and assembly limits

- All parts are split into plate-like or upright pieces intended for common
  220 × 220 mm printers. Check the printer's actual build volume and orient parts
  for layer lines across the load path.
- Use the turntable bearing for the pan load and one 608 bearing for the
  motor-side tilt support. The passive pivot runs directly against printed
  plastic; inspect it for friction and wear.
- The motor-side 608 seat and driven 8 mm journal are nominal; tune for the
  bearing and print material. Confirm axial retention on both tilt sides.
- Add metal washers or wide backing plates at every screw into printed plastic.
- Use heat-set inserts or captive nuts where a screw will be removed repeatedly.
- The current changed print files are `base`, `tilt_servo_retainer`,
  `tilt_servo_retainer_lid`, and `tilt_passive_printed_pivot`. Existing printed
  servo rails, tilt bracket and output-axis holes remain geometrically
  unchanged.
- Pan and tilt servo horn adapters use the same provisional Ø14 four-hole
  pattern. Verify the exact horn plate before final printing; do not clamp
  fragile panels or unsupported decorative LEGO parts.

## Physical measurements needed for Rev B

1. Weigh the complete moving telescope plus adapter and cradle.
2. Find the combined centre of gravity with solar arrays and door in intended
   display positions; record the three-axis offsets from a chosen datum.
3. Measure both side features' orientation, male/female form, cross profile, usable
   engagement depth and exact centre spacing. Confirm 105 mm and pivot-axis height;
   print a small socket/sleeve gauge before printing the full yoke.
4. Measure the real servo case, output axis, horn stack height and mounting
   holes. In particular, confirm the 12.5 mm output-axis offset direction and
   how each servo is oriented in its cradle. Compare its supplied STEP coordinate
   orientation with the physical unit.
5. Purchase the chosen 100 mm bearing and record thickness and both ring hole
   coordinates. Update `PAN_BEARING_BOLT_R` / slots if needed.
6. Measure the desk footprint and verify the 190 mm base cannot tip with the
   solar arrays rotated into the worst overhang position.

The exports are geometrically editable and useful for fitting hardware. They
are not structural certification or a substitute for a guarded, low-speed load
test with a dummy mass.
