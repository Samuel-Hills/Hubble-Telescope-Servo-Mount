# Generated models and previews

All files here are generated from `src/hubble_stand.py` or the companion
visualization scripts. CAD units are millimetres.

## Current printable parts

Each current part is provided as both `.stl` and `.step`:

`base`, `pan_deck`, `yoke_left`, `yoke_right`, `servo_retainer`,
`pan_drive_adapter`, `tilt_drive_socket`, `tilt_passive_printed_pivot`,
`tilt_servo_bracket`, `tilt_servo_retainer`, and
`tilt_servo_retainer_lid`.

Use STEP for CAD editing and STL for slicing. The passive printed pivot is a
plain sliding interface in a printed yoke bore; do a fit check before printing
the full set or attaching the telescope.

## Assemblies and visual assets

- `assembly_layout.step` — CAD assembly layout with servo/bearing envelopes.
- `assembly_layout.glb` — interactive-capable stand layout for 3D viewers.
- `visual_model.glb`, `visual_model.blend` — stand plus approximate Hubble
  visualization; the telescope mock-up is not printable or brick-accurate.
- `visual_360.mp4` — current camera orbit of the visualization.
- `holder_overview.png`, `holder_interface_detail.png` — current renders.

Generated binary files are intentionally tracked so the repo is immediately
useful without requiring a local CAD toolchain. Regenerate after editing the
parametric source; do not edit an STL as the only copy of a design change.

Earlier passive sleeve variants are preserved in `archive/` for reference and
are not included in the current assembly.
