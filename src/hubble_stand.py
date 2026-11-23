"""Parametric prototype CAD for a two-axis LEGO Hubble display stand.

Units are millimetres. This is an evolving fit-check design, not a
load-certified product. See docs/project-status.md before printing or use.
Requires CadQuery 2.8+; run from the repository root with `python src/hubble_stand.py`.
"""
from pathlib import Path
import math
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exports"
OUT.mkdir(exist_ok=True)

# Configurable dimensions. Servo outline is from the supplied C044 data sheet.
SERVO_L = 45.2
SERVO_W = 24.7
SERVO_H = 36.5          # incl. output boss; case nominal height is 35 mm
SERVO_CLEAR = 0.6       # print clearance; verify on the physical unit
SERVO_OUTPUT_OFFSET = 12.5  # datasheet: output axis offset from the case centre
PAN_CASE_SHIFT_X = -SERVO_OUTPUT_OFFSET
TILT_CASE_SHIFT_Z = -SERVO_OUTPUT_OFFSET  # user-selected: case sits below the tilt axis
BASE_XY = 190.0
BASE_H = 46.0
PAN_BEARING_OD = 100.0  # assumed slim turntable bearing; drill pattern is adjustable
PAN_BEARING_OUTER_BOLT_R = 44.0
PAN_BEARING_INNER_BOLT_R = 31.0
PAN_BEARING_T = 5.0    # visual stack assumption only; measure purchased bearing
PAN_DECK_D = 180.0
PAN_DECK_T = 10.0
YOKE_SPAN = 105.0
YOKE_HEIGHT = 166.0
TILT_AXIS_Z = 140.0
BEARING_608_OD = 22.0
BEARING_608_ID = 8.0
BEARING_608_W = 7.0
PASSIVE_PIVOT_OD = BEARING_608_OD - 0.4  # plain printed journal in the yoke's 22 mm bore
PASSIVE_PIVOT_FLANGE_OD = 26.0
PASSIVE_PIVOT_FLANGE_T = 2.5
PASSIVE_PIVOT_CROSS_DEPTH = 12.0
M3_CLR = 3.4
M4_CLR = 4.5
M5_CLR = 5.5
CONNECTOR_SPACING = 105.0  # user-measured centre distance between LEGO cross features
CROSS_PIN_OVERALL = 4.8   # nominal Technic cross-axle size; gauge the actual interface
CROSS_PIN_ARM = 1.8       # editable fit parameter
CROSS_PIN_LENGTH = 8.0    # nominal engagement length
DRIVE_FLANGE_OD = 21.6    # fits within the nominal 22 mm yoke bearing-seat bore
DRIVE_FLANGE_T = 3.0
HORN_PLATE_OD = 21.6      # purchased 25T horn envelope; verify the actual part
HORN_PLATE_T = 2.5
HORN_HOLE_PITCH = 14.0    # Feetech STS3215 accessory drawing: four cardinal holes on Ø14
HORN_HOLE_RADIUS = HORN_HOLE_PITCH / 2
HORN_HOLE_POINTS = ((HORN_HOLE_RADIUS, 0), (-HORN_HOLE_RADIUS, 0),
                    (0, HORN_HOLE_RADIUS), (0, -HORN_HOLE_RADIUS))
SERVO_CASE_CLEAR = 0.6
SERVO_CAGE_LENGTH = 36.5
SERVO_CAGE_WALL = 3.0


def rounded_plate(x, y, z0, thick, radius, holes=()):
    shape = (cq.Workplane("XY").rect(x, y).extrude(thick)
             .edges("|Z").fillet(radius).translate((0, 0, z0)))
    for hx, hy, dia in holes:
        cutter = cq.Workplane("XY").circle(dia / 2).extrude(thick + 2).translate((hx, hy, z0 - 1))
        shape = shape.cut(cutter)
    return shape


def slot_cutter(cx, cy, length, width, angle, z0, height):
    """Straight slot whose long axis follows `angle` degrees from +X."""
    s = cq.Workplane("XY").slot2D(length, width, angle).extrude(height)
    return s.translate((cx, cy, z0))


def z_cylinder(radius, height, x, y, z0):
    return cq.Workplane("XY").circle(radius).extrude(height).translate((x, y, z0))


def x_cylinder(radius, length, x0, y, z):
    return cq.Workplane("YZ").center(y, z).circle(radius).extrude(length).translate((x0, 0, 0))


def y_cylinder(radius, length, x, y0, z):
    """Cylinder along -Y, starting at y0; used for transverse clamp screws."""
    return cq.Workplane("XZ").center(x, z).circle(radius).extrude(length).translate((0, y0, 0))


def make_base():
    # Broad low footprint with a blind servo bay opening from underneath.  The
    # servo retaining strap and bay end clearance remain adjustable after fit check.
    base = rounded_plate(BASE_XY, BASE_XY, -BASE_H, BASE_H, 14)
    bay_x = SERVO_L + 2 * SERVO_CLEAR + 4
    bay_y = SERVO_W + 2 * SERVO_CLEAR + 4
    bay_depth = BASE_H - 3.4  # leave clearance for the nominal horn/output projection
    bay = cq.Workplane("XY").rect(bay_x, bay_y).extrude(bay_depth).edges("|Z").fillet(2)
    base = base.cut(bay.translate((PAN_CASE_SHIFT_X, 0, -BASE_H)))
    # Through-port for the servo output and pan horn, aligned with the bearing centre.
    base = base.cut(cq.Workplane("XY").circle(9).extrude(4.4).translate((0, 0, -3.4)))
    # Flush pockets for the two underside retaining rails.
    for y in (-6, 6):
        pocket = rounded_plate(64, 10, -BASE_H, 4, 2).translate((PAN_CASE_SHIFT_X, y, 0))
        base = base.cut(pocket)
    # Four radial slots per race for unknown bearing screw pitch (37–51 mm).
    # Slots accept M4 hardware; match them to the purchased bearing before printing.
    for a in range(0, 360, 90):
        rad = math.radians(a)
        cx, cy = PAN_BEARING_OUTER_BOLT_R * math.cos(rad), PAN_BEARING_OUTER_BOLT_R * math.sin(rad)
        base = base.cut(slot_cutter(cx, cy, 14, M4_CLR, a, -1, 3))
    # Cable pass-through from servo bay to rear edge.
    cable = cq.Workplane("XY").rect(9, 18).extrude(13).translate((PAN_CASE_SHIFT_X, 0, -13))
    base = base.cut(cable)
    # Four M5 feet / desk attachment holes. Counterbore from underside.
    for x in (-72, 72):
        for y in (-72, 72):
            base = base.cut(cq.Workplane("XY").circle(M5_CLR / 2).extrude(BASE_H + 2).translate((x, y, -BASE_H - 1)))
            base = base.cut(cq.Workplane("XY").circle(9 / 2).extrude(3).translate((x, y, -BASE_H)))
    # M3 heat-set insert pilots for the two servo retaining rails, drilled from below.
    for x in (PAN_CASE_SHIFT_X - 30, PAN_CASE_SHIFT_X + 30):
        for y in (-6, 6):
            base = base.cut(cq.Workplane("XY").circle(2.1).extrude(7).translate((x, y, -BASE_H + 4)))
    return base


def make_pan_deck():
    # Rotating plate sits on a separate 100 mm lazy-Susan bearing. Its centre is
    # open so the servo horn can act coaxially without carrying axial weight.
    plate = cq.Workplane("XY").circle(PAN_DECK_D / 2).extrude(PAN_DECK_T)
    # Clearance for the M3 horn screw and its washer (servo horn purchased separately).
    plate = plate.cut(cq.Workplane("XY").circle(7).extrude(PAN_DECK_T + 2).translate((0, 0, -1)))
    for x in (-11, 11):
        for y in (-11, 11):
            plate = plate.cut(cq.Workplane("XY").circle(M3_CLR / 2).extrude(PAN_DECK_T + 2).translate((x, y, -1)))
    # Radial attachment slots for bearing upper ring.
    for a in range(0, 360, 90):
        rad = math.radians(a)
        cx, cy = PAN_BEARING_INNER_BOLT_R * math.cos(rad), PAN_BEARING_INNER_BOLT_R * math.sin(rad)
        plate = plate.cut(slot_cutter(cx, cy, 14, M4_CLR, a, -1, PAN_DECK_T + 2))
    # Yoke mounting holes, square pattern.
    for x in (-37, 37):
        for y in (-37, 37):
            plate = plate.cut(cq.Workplane("XY").circle(M5_CLR / 2).extrude(PAN_DECK_T + 2).translate((x, y, -1)))
    # Pan-yoke feet: two uprights at X=+/-52, each with four M5 holes.
    for x in (-YOKE_SPAN / 2, YOKE_SPAN / 2):
        for y in (-28, -9, 9, 28):
            plate = plate.cut(cq.Workplane("XY").circle(M5_CLR / 2).extrude(PAN_DECK_T + 2).translate((x, y, -1)))
    return plate


def make_yoke_side(sign=1):
    # Two mirrored gusseted uprights; print each flat on the build plate.
    # Coordinates local: XY is the print face, Z becomes assembly height.
    upright = cq.Workplane("XY").rect(14, 76).extrude(YOKE_HEIGHT)
    # Broad triangular web behind the bearing boss.
    web = (cq.Workplane("XY").polyline([(-7, -38), (7, -38), (7, 37), (-7, 37)])
           .close().extrude(YOKE_HEIGHT))
    # Taper the upper region by cutting two triangular side reliefs.
    upright = upright.union(web)
    # Bearing seat axis is X, at the nominal tilt axis height.
    # Local height is reduced by the 12 mm deck stack in the positioned assembly.
    # Positioned assembly: bearing + deck + foot flange place upright origin at 25 mm.
    local_axis_z = TILT_AXIS_Z - 25
    bore = x_cylinder(BEARING_608_OD / 2, 16, -8, 0, local_axis_z)
    upright = upright.cut(bore)
    shaft = x_cylinder(BEARING_608_ID / 2, 18, -9, 0, local_axis_z)
    upright = upright.cut(shaft)
    # Four M3 clearance holes attach the adjustable tilt-servo plate to this arm.
    # Hole positions mirror the provisional Y/Z pattern in make_tilt_servo_bracket().
    for yy in (-20, 20):
        for dz in (-17, 17):
            upright = upright.cut(x_cylinder(M3_CLR / 2, 16, -8, yy, local_axis_z + dz))
    # Four M5 fasteners attach each upright to the deck through a foot flange.
    foot = rounded_plate(54, 76, 0, 10, 4)
    for y in (-28, -9, 9, 28):
        foot = foot.cut(cq.Workplane("XY").circle(M5_CLR / 2).extrude(12).translate((0, y, -1)))
    part = upright.union(foot.translate((0, 0, -10)))
    if sign < 0:
        part = part.mirror("YZ")
    return part


def cross_profile_socket(x0, depth, clearance=0.25):
    """Provisional cross-shaped socket cut from the inboard end along +X."""
    overall = CROSS_PIN_OVERALL + 2 * clearance
    arm = CROSS_PIN_ARM + 2 * clearance
    a = cq.Workplane("YZ").rect(overall, arm).extrude(depth).translate((x0, 0, 0))
    b = cq.Workplane("YZ").rect(arm, overall).extrude(depth).translate((x0, 0, 0))
    return a.union(b)


def make_tilt_drive_socket():
    # Printable drive coupling: a 14 mm cardinal four-hole flange mates to a
    # Feetech-compatible 25T metal horn; a through cross-bore runs the full
    # journal length and opens inward to the telescope. The round journal runs
    # in the left 608 bearing.
    shaft_length = 15.5
    shaft = x_cylinder(3.9, shaft_length, -56.5, 0, 0)  # ends at -41
    flange = x_cylinder(DRIVE_FLANGE_OD / 2, DRIVE_FLANGE_T, -59.5, 0, 0)
    p = shaft.union(flange)
    # Female cross bore is centred on the tilt axis and passes through the
    # journal only; the flange remains intact as the horn attachment face.
    p = p.cut(cross_profile_socket(-56.5, shaft_length))
    for y, z in HORN_HOLE_POINTS:
        p = p.cut(x_cylinder(M3_CLR / 2, DRIVE_FLANGE_T + 0.2, -59.6, y, z))
    return p


def make_tilt_servo_horn_reference():
    """Simplified purchased 25T horn/plate envelope; not a printable part."""
    plate = x_cylinder(HORN_PLATE_OD / 2, HORN_PLATE_T, -2.5, 0, 0)
    hub = x_cylinder(4.0, 3.4, -5.9, 0, 0)
    horn = plate.union(hub)
    # Simplified round spline envelope and retaining-screw clearance.
    horn = horn.cut(x_cylinder(3.1, 3.5, -6.0, 0, 0))
    horn = horn.cut(x_cylinder(1.7, HORN_PLATE_T + 0.2, -2.6, 0, 0))
    for y, z in HORN_HOLE_POINTS:
        horn = horn.cut(x_cylinder(M3_CLR / 2, HORN_PLATE_T + 0.2, -2.6, y, z))
    return horn


def make_tilt_passive_printed_pivot():
    """Bearing-free passive pivot that rotates directly in the right yoke bore.

    The printed round journal replaces the 608 bearing on the passive side.
    Its flange retains the journal axially, and a blind female cross socket
    accepts the telescope's male LEGO cross feature. The nominal diametral
    clearance is 0.4 mm against the existing 22 mm yoke bore; tune after a fit
    test because both mating surfaces are printed plastic.
    """
    x0 = YOKE_SPAN / 2 - 7.0  # inner face of the 14 mm-thick right yoke upright
    journal_len = 14.3        # spans yoke, with 0.3 mm axial running clearance
    journal = x_cylinder(PASSIVE_PIVOT_OD / 2, journal_len, x0, 0, 0)
    flange_x = x0 + journal_len
    flange = x_cylinder(PASSIVE_PIVOT_FLANGE_OD / 2,
                        PASSIVE_PIVOT_FLANGE_T, flange_x, 0, 0)
    socket = cross_profile_socket(x0, PASSIVE_PIVOT_CROSS_DEPTH, clearance=0.35)
    lead_in = cross_profile_socket(x0 - 0.01, 1.5, clearance=0.60)
    return journal.union(flange).cut(socket.union(lead_in))


def make_servo_retainer():
    # Print two rails. Each bridges the underside bay, rises to support the
    # servo's lower case face, and screws into M3 inserts in the base.
    strap = rounded_plate(64, 10, 0, 4, 2)
    pad = rounded_plate(22, 10, 4, 5.5, 2)
    strap = strap.union(pad)
    for x in (-30, 30):
        strap = strap.cut(cq.Workplane("XY").circle(M3_CLR / 2).extrude(5).translate((x, 0, -0.5)))
        strap = strap.cut(cq.Workplane("XY").circle(6 / 2).extrude(2.5).translate((x, 0, 0)))
    return strap


def make_pan_drive_adapter():
    # Adapter bolts to the same 25T horn pattern as the tilt coupling.
    # The centre hole clears the horn retaining screw. Horn holes use the
    # Feetech STS3215 accessory drawing's four cardinal positions on Ø14 PCD.
    disk = cq.Workplane("XY").circle(22).extrude(4)
    disk = disk.cut(cq.Workplane("XY").circle(6.4).extrude(6).translate((0, 0, -1)))
    for x, y in HORN_HOLE_POINTS:
        disk = disk.cut(cq.Workplane("XY").circle(M3_CLR / 2).extrude(6).translate((x, y, -1)))
    # Four M3 screws attach adapter to rotating pan deck around its central bore.
    for x in (-11, 11):
        for y in (-11, 11):
            disk = disk.cut(cq.Workplane("XY").circle(M3_CLR / 2).extrude(6).translate((x, y, -1)))
    return disk


def make_tilt_servo_bracket():
    # Adjustable motor plate for the outside of either yoke arm. Axis is X;
    # the centre opening clears the Feetech 25T output boss. Fit slots to the
    # selected mounting screws after checking the supplied STEP against the unit.
    plate = cq.Workplane("YZ").rect(58, 52).extrude(6)
    # Clearance opening for the simplified 22 mm horn plate and drive flange.
    plate = plate.cut(cq.Workplane("YZ").circle(12.2).extrude(8).translate((-1, 0, 0)))
    for y in (-20, 20):
        for z in (-17, 17):
            slot = cq.Workplane("YZ").center(y, z).slot2D(12, M3_CLR, 0).extrude(8).translate((-1, 0, 0))
            plate = plate.cut(slot)
    return plate


def make_tilt_servo_retainer():
    """Open-top case cradle that bolts to the existing tilt-servo bracket.

    Local X=0 is the existing bracket's outboard face; the cradle extends in
    -X over the servo case. A rear stop and screw-on lid prevent the servo from
    sliding or twisting. Dimensions follow the supplied envelope with clearance.
    """
    case_w = SERVO_W + 2 * SERVO_CASE_CLEAR
    case_h = SERVO_L + 2 * SERVO_CASE_CLEAR
    outer_w = case_w + 11.0  # 5.5 mm side walls for M3 insert pilots
    shell_h = 49.0
    case_z = TILT_CASE_SHIFT_Z
    shell_z = case_z - 1.5    # bottom is 2.8 mm below the case; lid closes above it
    back_t = 2.5
    x0 = -SERVO_CAGE_LENGTH
    shell = (cq.Workplane("YZ").center(0, shell_z).rect(outer_w, shell_h)
             .extrude(SERVO_CAGE_LENGTH).translate((x0, 0, 0)))

    # Open-top U channel; leave a rear end wall to stop the case moving outboard.
    inner_bottom = case_z - case_h / 2
    shell_top = shell_z + shell_h / 2
    cavity_top = shell_top + 2.0
    cavity_h = cavity_top - inner_bottom
    cavity_z = (cavity_top + inner_bottom) / 2
    cavity = (cq.Workplane("YZ").center(0, cavity_z).rect(case_w, cavity_h)
              .extrude(SERVO_CAGE_LENGTH - back_t + 0.2)
              .translate((x0 + back_t, 0, 0)))
    shell = shell.cut(cavity)
    # Cable/connector exit through the rear stop. It is smaller than the case
    # envelope, so the case cannot pass through it.
    cable_window = (cq.Workplane("YZ").center(0, case_z).rect(20.0, 38.0).extrude(back_t + 0.2)
                    .translate((x0 - 0.1, 0, 0)))
    shell = shell.cut(cable_window)

    # The enlarged offset flange reaches around the lower case. Its four holes
    # stay at the already-printed bracket/yoke pattern; only the case opening
    # and cradle move down by 12.5 mm relative to the fixed tilt output axis.
    flange = cq.Workplane("YZ").rect(58.0, 80.0).extrude(4.0).translate((-4.0, 0, 0))
    flange = flange.cut(cq.Workplane("YZ").center(0, case_z).rect(case_w + 1.0, case_h + 1.0)
                        .extrude(4.2).translate((-4.1, 0, 0)))
    for y in (-20, 20):
        for z in (-17, 17):
            flange = flange.cut(x_cylinder(M3_CLR / 2, 4.2, -4.1, y, z))
    shell = shell.union(flange)

    # Blind M3 heat-set insert pilots in the side rails secure the lid.
    for x in (-9.0, -28.5):
        for y in (-15.5, 15.5):
            shell = shell.cut(z_cylinder(2.1, 5.5, x, y, shell_top - 5.5))
    return shell


def make_tilt_servo_retainer_lid():
    """Flat clamp lid; four M3 screws engage inserts in the cradle side rails."""
    outer_w = SERVO_W + 2 * SERVO_CASE_CLEAR + 11.0
    lid_length = SERVO_CAGE_LENGTH - 4.0
    lid_z = TILT_CASE_SHIFT_Z + 23.0
    lid = rounded_plate(lid_length, outer_w, lid_z, 3.0, 1.5).translate((-(SERVO_CAGE_LENGTH + 4.0) / 2, 0, 0))
    for x in (-9.0, -28.5):
        for y in (-15.5, 15.5):
            lid = lid.cut(z_cylinder(M3_CLR / 2, 4.0, x, y, lid_z - 0.5))
    return lid


PARTS = {
    "base": make_base(),
    "pan_deck": make_pan_deck(),
    "yoke_left": make_yoke_side(-1),
    "yoke_right": make_yoke_side(1),
    "tilt_drive_socket": make_tilt_drive_socket(),
    "tilt_passive_printed_pivot": make_tilt_passive_printed_pivot(),
    "servo_retainer": make_servo_retainer(),
    "pan_drive_adapter": make_pan_drive_adapter(),
    "tilt_servo_bracket": make_tilt_servo_bracket(),
    "tilt_servo_retainer": make_tilt_servo_retainer(),
    "tilt_servo_retainer_lid": make_tilt_servo_retainer_lid(),
}

def make_turntable_bearing_envelope():
    """Simplified bought-part envelope for assembly layout, not a bearing model."""
    return (cq.Workplane("XY").circle(PAN_BEARING_OD / 2).circle(76 / 2)
            .extrude(PAN_BEARING_T))


def make_servo_envelope():
    """Clean, simplified envelope for assembly layout; the supplied STEP is kept separately."""
    body_h = SERVO_H - 3.4
    body = (cq.Workplane("XY").rect(SERVO_L, SERVO_W).extrude(body_h)
            .edges("|Z").fillet(2).translate((0, 0, -SERVO_H)))
    output = (cq.Workplane("XY").center(SERVO_OUTPUT_OFFSET, 0).circle(2.95)
              .extrude(3.4).translate((0, 0, -3.4)))
    return body.union(output)


def make_608_envelope():
    """Simplified purchased 608 bearing envelope, axis along X."""
    return x_cylinder(11, 7, 0, 0, 0).cut(x_cylinder(4, 7, 0, 0, 0))


def export():
    for name, part in PARTS.items():
        cq.exporters.export(part, str(OUT / f"{name}.step"))
        cq.exporters.export(part, str(OUT / f"{name}.stl"), tolerance=0.15, angularTolerance=0.1)

    # A positioned illustrative assembly. Purchased servos/bearings/fasteners are
    # omitted; keep this assembly for envelope/layout review only.
    assy = cq.Assembly(name="Hubble_Display_Stand_RevA")
    assy.add(PARTS["base"], name="base", color=cq.Color(0.12, 0.13, 0.16))
    # Clean envelope solids are used in the STEP assembly. The supplied detailed
    # servo STEP is retained under reference/ because it contains invalid solids.
    servo_ref = make_servo_envelope()
    # Base top is z=0; output tip sits at the pan axis.
    # Keep the pan output boss at the fixed base port; the case shifts left by
    # the documented 12.5 mm offset. The retaining rails stay the same printed parts.
    pan_servo = servo_ref.translate((PAN_CASE_SHIFT_X, 0, 0))
    assy.add(pan_servo, name="pan_servo_reference", color=cq.Color(0.28, 0.29, 0.32))
    assy.add(PARTS["servo_retainer"].translate((PAN_CASE_SHIFT_X, -6, -BASE_H)), name="servo_retainer_A", color=cq.Color(0.2, 0.21, 0.24))
    assy.add(PARTS["servo_retainer"].translate((PAN_CASE_SHIFT_X, 6, -BASE_H)), name="servo_retainer_B", color=cq.Color(0.2, 0.21, 0.24))
    assy.add(make_turntable_bearing_envelope(), name="turntable_bearing_envelope", color=cq.Color(0.65, 0.66, 0.68))
    assy.add(PARTS["pan_deck"].translate((0, 0, PAN_BEARING_T)), name="pan_deck", color=cq.Color(0.22, 0.23, 0.27))
    assy.add(PARTS["pan_drive_adapter"].translate((0, 0, PAN_BEARING_T - 4)), name="pan_drive_adapter", color=cq.Color(0.72, 0.72, 0.74))
    # Same horn reference and 14 mm four-hole pattern as the tilt axis; the pan
    # horn sits below the adapter plate, coaxial with the vertical servo output.
    pan_horn = (make_tilt_servo_horn_reference()
                .rotate((0, 0, 0), (0, 1, 0), -90)
                .translate((0, 0, PAN_BEARING_T - 4)))
    assy.add(pan_horn, name="pan_servo_horn_reference", color=cq.Color(0.68, 0.70, 0.72))
    # Uprights installed at left/right, with bolt feet at pan-deck top.
    yoke_z = PAN_BEARING_T + PAN_DECK_T + 10
    left = PARTS["yoke_left"].translate((-YOKE_SPAN / 2, 0, yoke_z))
    right = PARTS["yoke_right"].translate((YOKE_SPAN / 2, 0, yoke_z))
    assy.add(left, name="yoke_left", color=cq.Color(0.18, 0.19, 0.22))
    assy.add(right, name="yoke_right", color=cq.Color(0.18, 0.19, 0.22))
    bearing608 = make_608_envelope()
    assy.add(bearing608.translate((-56, 0, TILT_AXIS_Z)), name="tilt_bearing_left", color=cq.Color(0.7, 0.71, 0.73))
    horn = make_tilt_servo_horn_reference().translate((-59.5, 0, TILT_AXIS_Z))
    assy.add(horn, name="tilt_servo_horn_reference", color=cq.Color(0.68, 0.70, 0.72))
    assy.add(PARTS["tilt_drive_socket"].translate((0, 0, TILT_AXIS_Z)), name="tilt_drive_socket", color=cq.Color(0.78, 0.45, 0.14))
    assy.add(PARTS["tilt_passive_printed_pivot"].translate((0, 0, TILT_AXIS_Z)), name="tilt_passive_printed_pivot", color=cq.Color(0.62, 0.64, 0.66))
    # Tilt servo is shown on the outside of the left upright; the actual horn
    # stack and coupling must be adjusted after the horn is selected.
    tilt_bracket = PARTS["tilt_servo_bracket"].translate((-65, 0, TILT_AXIS_Z))
    assy.add(tilt_bracket, name="tilt_servo_bracket", color=cq.Color(0.16, 0.17, 0.2))
    retainer = PARTS["tilt_servo_retainer"].translate((-65, 0, TILT_AXIS_Z))
    retainer_lid = PARTS["tilt_servo_retainer_lid"].translate((-65, 0, TILT_AXIS_Z))
    assy.add(retainer, name="tilt_servo_retainer", color=cq.Color(0.22, 0.24, 0.28))
    assy.add(retainer_lid, name="tilt_servo_retainer_lid", color=cq.Color(0.22, 0.24, 0.28))
    # The bracket sits between the case face and the yoke; a horn/coupler bridges
    # the remaining axial gap to the supported tilt shaft.
    # Flip the off-centre case orientation around the output axis so the case
    # sits 12.5 mm below the fixed output axis, as requested. Shaft axis remains
    # at the existing bracket aperture and trunnion centre.
    tilt_servo = (servo_ref.rotate((0, 0, 0), (0, 0, 1), 180)
                  .rotate((0, 0, 0), (0, 1, 0), 90)
                  .translate((-62, 0, TILT_AXIS_Z + TILT_CASE_SHIFT_Z)))
    assy.add(tilt_servo, name="tilt_servo_reference", color=cq.Color(0.28, 0.29, 0.32))
    assy.save(str(OUT / "assembly_layout.step"), exportType="STEP")
    assy.save(str(OUT / "assembly_layout.glb"))


if __name__ == "__main__":
    export()
    print(f"Wrote {len(PARTS)} component STEP/STL pairs and assembly layout to {OUT}")
