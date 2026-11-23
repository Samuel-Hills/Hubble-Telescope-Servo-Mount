"""Build a presentation mock-up around the Rev A mechanical layout.

The Hubble body and solar arrays here are deliberately simplified envelope
geometry for viewing only. They are not LEGO-accurate, printable or load-bearing.
Run with Blender 5.x: blender -b --python src/make_visual_model.py
"""
from pathlib import Path
import math
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exports"
OUT.mkdir(exist_ok=True)
CONNECTOR_SPACING = 105.0

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(OUT / "assembly_layout.glb"))


def material(name, color, metallic=0.0, roughness=0.35):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return m


ivory = material("Telescope | warm white", (0.82, 0.83, 0.79), 0.08)
dark = material("Telescope | graphite", (0.08, 0.10, 0.12), 0.35)
gold = material("Telescope | thermal foil", (0.88, 0.45, 0.12), 0.45)
blue = material("Solar cells | deep blue", (0.035, 0.13, 0.34), 0.35, 0.26)
grid = material("Solar cells | grid lines", (0.28, 0.58, 0.78), 0.45)
metal = material("Structural metal", (0.46, 0.50, 0.52), 0.62)
stand_mat = material("Stand | graphite polymer", (0.22, 0.25, 0.30), 0.18, 0.34)
servo_mat = material("Servo cases", (0.38, 0.40, 0.43), 0.28, 0.38)
bearing_mat = material("Bearings and shaft", (0.62, 0.65, 0.68), 0.72, 0.22)
holder_mat = material("Side pivot parts | highlighted", (0.95, 0.48, 0.08), 0.25, 0.3)


def finish(obj, name, mat):
    obj.name = name
    if obj.type == "MESH":
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    return obj


for obj in bpy.context.scene.objects:
    if obj.type != "MESH":
        continue
    name = obj.name.lower()
    if any(k in name for k in ("tilt_drive_socket", "tilt_passive_printed_pivot", "tilt_servo_retainer")):
        finish(obj, obj.name, holder_mat)
    elif "tilt_servo_horn" in name:
        finish(obj, obj.name, metal)
    elif any(k in name for k in ("servo", "bearing", "shaft")):
        finish(obj, obj.name, servo_mat if "servo" in name else bearing_mat)
    else:
        finish(obj, obj.name, stand_mat)
def cube(name, loc, dims, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    finish(o, name, mat)
    if bevel:
        mod = o.modifiers.new("Soft printed edges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        o.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    return o


def cylinder_y(name, y_center, z_center, radius, length, mat, vertices=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length,
                                        location=(0, y_center, z_center), rotation=(math.pi / 2, 0, 0))
    return finish(bpy.context.object, name, mat)


def rod(name, a, b, radius, mat):
    a, b = Vector(a), Vector(b)
    d = b - a
    mid = (a + b) * 0.5
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=d.length, location=mid)
    o = bpy.context.object
    o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    return finish(o, name, mat)


# Approximate telescope body: optical axis is Y, transverse tilt axis is X.
# The tube underside meets the adapter plate at nominal z=105 mm.
cylinder_y("Approx Hubble body | 260 mm envelope", 0, 140, 35, 260, ivory)
cylinder_y("Rear equipment collar", 126, 140, 39, 14, dark)
cylinder_y("Aperture rim", -132, 140, 40, 8, dark)
cylinder_y("Aperture door rim", -137, 140, 33, 3, gold)
cylinder_y("Primary mirror | visual only", -139.5, 140, 27, 1.5, grid)

# Side-mounted LEGO cross features, 105 mm centre-to-centre across X.
# Provisional visual analogue: small connector shoulders and male cross axles.
for sign, side in ((-1, "drive"), (1, "idler")):
    xc = sign * 52.5
    cube(f"LEGO side connector shoulder | {side}", (sign * 42, 0, 140), (12, 12, 12), ivory, 1.1)
    # Cross axle projects outward from each side shoulder.
    start = xc - 4 if sign > 0 else xc - 4
    cross_a = cube(f"LEGO side cross axle | {side} horizontal", (xc, 0, 140), (8, 4.8, 1.8), gold, 0.25)
    cross_b = cube(f"LEGO side cross axle | {side} vertical", (xc, 0, 140), (8, 1.8, 4.8), gold, 0.25)

# A few longitudinal thermal blankets / rails suggest the LEGO assembly without
# claiming exact brick geometry.
for angle in (0, 90, 180, 270):
    theta = math.radians(angle)
    x = 32 * math.cos(theta)
    z = 140 + 32 * math.sin(theta)
    rail = cylinder_y(f"Thermal rail {angle}", 0, 0, 2.0, 210, gold, 20)
    rail.location = (x, 0, z)

# Four thin blue panel segments, two on each side, extending the mock-up to a
# roughly 380 mm lateral envelope. Panels are a visual approximation only.
panel_z = 185
panel_y = 142
panel_dx = 64
for sign, side in ((-1, "port"), (1, "starboard")):
    for seg, center_abs_x in enumerate((91.0, 155.0), start=1):
        x = sign * center_abs_x
        cube(f"{side} solar panel {seg} | blue face", (x, 0, panel_z),
             (panel_dx, panel_y, 4), blue, 1.2)
        # perimeter frame
        for xx in (x - panel_dx / 2 + 1.5, x + panel_dx / 2 - 1.5):
            cube(f"{side} panel {seg} frame rail", (xx, 0, panel_z + 2.6),
                 (2.2, panel_y, 1.2), metal, 0.25)
        for yy in (-panel_y / 2 + 1.5, panel_y / 2 - 1.5):
            cube(f"{side} panel {seg} frame rail", (x, yy, panel_z + 2.6),
                 (panel_dx, 2.2, 1.2), metal, 0.25)
        # cell grid
        for n in range(1, 5):
            xx = x - panel_dx / 2 + n * panel_dx / 5
            cube(f"{side} panel {seg} cell divider", (xx, 0, panel_z + 2.25),
                 (0.65, panel_y - 4, 0.35), grid)
        for n in range(1, 8):
            yy = -panel_y / 2 + n * panel_y / 8
            cube(f"{side} panel {seg} cell divider", (x, yy, panel_z + 2.25),
                 (panel_dx - 4, 0.65, 0.35), grid)

# Bracing from the telescope body to each wing's root.
for sign in (-1, 1):
    for y in (-48, 48):
        rod("Solar wing support", (sign * 31, y, 158), (sign * 60, y, 182), 2.6, metal)
        rod("Solar wing support", (sign * 31, y, 158), (sign * 60, y, 182), 1.0, gold)

# Soft ground and studio setup.
ground_mat = material("Backdrop | slate", (0.055, 0.07, 0.09), 0.05, 0.58)
cube("Ground", (0, 0, -48), (1200, 1200, 3), ground_mat)

world = bpy.context.scene.world or bpy.data.worlds.new("Studio")
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.055, 0.07, 0.09, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.75

def area(name, loc, power, size, color):
    bpy.ops.object.light_add(type="AREA", location=loc)
    o = bpy.context.object
    o.name = name
    o.data.energy = power
    o.data.shape = "DISK"
    o.data.size = size
    o.data.color = color
    o.rotation_euler = (Vector((0, 0, 85)) - o.location).to_track_quat("-Z", "Y").to_euler()

area("Key softbox", (300, -300, 430), 320000, 260, (0.78, 0.86, 1.0))
area("Warm fill", (-320, -80, 250), 230000, 230, (1.0, 0.68, 0.42))
area("Rim light", (30, 300, 350), 320000, 220, (0.4, 0.63, 1.0))

bpy.ops.object.camera_add(location=(-470, -590, 390))
camera = bpy.context.object
camera.name = "Preview camera"
camera.rotation_euler = (Vector((0, 0, 72)) - camera.location).to_track_quat("-Z", "Y").to_euler()
camera.data.type = "ORTHO"
camera.data.ortho_scale = 680
camera.data.lens = 50
scene = bpy.context.scene
scene.camera = camera
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1500
scene.render.resolution_y = 1250
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(OUT / "holder_overview.png")
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = 1.0
scene.render.image_settings.color_mode = "RGBA"
scene.camera.data.lens = 45

# Save a native Blender scene and an easy-to-open GLB, with no camera/light objects
# in the GLB. The scene remains editable in the .blend project.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "visual_model.blend"))
mesh_objects = [o for o in scene.objects if o.type == "MESH"]
bpy.ops.object.select_all(action="DESELECT")
for o in mesh_objects:
    o.select_set(True)
bpy.context.view_layer.objects.active = mesh_objects[0]
bpy.ops.export_scene.gltf(filepath=str(OUT / "visual_model.glb"), export_format="GLB", use_selection=True)
scene.render.filepath = str(OUT / "holder_overview.png")
bpy.ops.render.render(write_still=True)

# Second render: close-up that clearly shows the driven and free pivot sides.
for obj in scene.objects:
    n = obj.name.lower()
    keep = any(k in n for k in ("yoke", "tilt_bearing", "tilt_drive_socket", "tilt_passive_printed_pivot", "tilt_servo", "lego side connector", "lego side cross axle"))
    if not keep:
        obj.hide_render = True
measure_mat = material("Dimension annotation", (1.0, 0.58, 0.12), 0.15, 0.28)
# A fine dimension bar between the cross-axis centres.
rod("105 mm centre spacing dimension", (-52.5, -30, 172), (52.5, -30, 172), 0.8, measure_mat)
for x in (-52.5, 52.5):
    rod("Dimension witness", (x, -30, 169), (x, -30, 175), 0.7, measure_mat)
camera.location = (-260, -220, 235)
camera.rotation_euler = (Vector((0, 0, 140)) - camera.location).to_track_quat("-Z", "Y").to_euler()
camera.data.ortho_scale = 280
scene.render.resolution_x = 1400
scene.render.resolution_y = 1000
scene.view_settings.exposure = 2.0
# Camera-facing callouts make the one driven side and one free support explicit.
for name, body, loc in (("Driven side callout", "MOTOR SIDE", (-118, -20, 194)),
                        ("Passive side callout", "PASSIVE | PRINTED PIVOT", (20, -20, 174))):
    bpy.ops.object.text_add(location=loc)
    label = bpy.context.object
    label.name = name
    label.data.body = body
    label.data.size = 8
    label.data.extrude = 0.05
    label.data.materials.append(measure_mat)
    label.rotation_euler = camera.rotation_euler
scene.render.filepath = str(OUT / "holder_interface_detail.png")
bpy.ops.render.render(write_still=True)
print("Wrote visual_model.blend, visual_model.glb, holder_overview.png and holder_interface_detail.png")
