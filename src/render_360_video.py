"""Render a one-turn camera orbit around the visual Hubble stand model.

Run with Blender 5.x from the project root:
  blender -b --python src/render_360_video.py
"""
from pathlib import Path
import bpy
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exports"
scene_file = OUT / "visual_model.blend"
bpy.ops.wm.open_mainfile(filepath=str(scene_file))
scene = bpy.context.scene
camera = scene.camera
if camera is None:
    raise RuntimeError("The visual scene has no camera")

# Keep the camera aimed at the scene centre while rotating its view through 360°.
pivot = bpy.data.objects.new("360 degree orbit pivot", None)
scene.collection.objects.link(pivot)
pivot.location = (0, 0, 72)
camera_world = camera.matrix_world.copy()
camera.parent = pivot
camera.matrix_world = camera_world
pivot.rotation_mode = "XYZ"

scene.frame_start = 1
scene.frame_end = 120
scene.render.fps = 24
pivot.rotation_euler.z = 0.0
pivot.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
pivot.rotation_euler.z = 6.283185307179586
pivot.keyframe_insert(data_path="rotation_euler", index=2, frame=120)
action = pivot.animation_data.action
channelbag = action.layers[0].strips[0].channelbag(action.slots[0])
for curve in channelbag.fcurves:
    for key in curve.keyframe_points:
        key.interpolation = "LINEAR"

scene.render.resolution_x = 1000
scene.render.resolution_y = 834
scene.render.resolution_percentage = 100
frame_dir = OUT / "visual_360_frames"
frame_dir.mkdir(exist_ok=True)
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(frame_dir / "turn_")
scene.render.use_file_extension = True

bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "visual_model_360.blend"))
bpy.ops.render.render(animation=True)

ffmpeg = shutil.which("ffmpeg")
if not ffmpeg:
    raise RuntimeError(f"Frames are in {frame_dir}; install ffmpeg to encode the MP4")
video_path = OUT / "visual_360.mp4"
subprocess.run([
    ffmpeg, "-y", "-framerate", "24", "-start_number", "1",
    "-i", str(frame_dir / "turn_%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
    "-preset", "medium", "-movflags", "+faststart", str(video_path),
], check=True)
shutil.rmtree(frame_dir)
print(f"Rendered 360 orbit video to {video_path}")
