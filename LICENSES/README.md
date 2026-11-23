# License map

The project offers separate licenses for the original hardware design and the
software. The complete license texts are in [`../LICENSE`](../LICENSE) and
[`MIT.txt`](MIT.txt).

Copyright (c) 2026 Samuel Hills, except where another rights holder or license
is identified.

## CERN-OHL-P-2.0

The original mechanical design and its engineering documentation are covered
by CERN-OHL-P-2.0:

- `src/hubble_stand.py`
- Original project artifacts under `exports/`, including CAD and assembly
  files (STEP, STL, GLB and Blender project files), renders and video
- `docs/`, `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, and
  `exports/README.md`, `reference/README.md`, and this license map

The `P` variant is permissive. Modified design files may use different license
terms, subject to the notices and license-copy requirements in the license.

## MIT

The original software is covered by MIT:

- `src/make_html_viewer.py`
- `src/make_visual_model.py`
- `src/motor_control_web.py`
- `src/render_360_video.py`
- `src/test_servos.py`
- `web/`, `Hubble_Assembly_Viewer.html`, `requirements.txt`,
  `setup_windows.bat`, and `run_motor_control.bat`

For `Hubble_Assembly_Viewer.html`, MIT applies to the viewer software; the
embedded 3D model data is covered as an `exports/` visualization artifact.

## Third-party material

`reference/Feetech_STS3215-C044_Datasheet.pdf`, `reference/ST3215-3D.zip`, and
`reference/ST3215.step` are third-party vendor reference materials and are not
covered by either project license. See [`reference/README.md`](../reference/README.md)
for their role and provenance. The project licenses also do not grant rights
to LEGO names, trademarks, or other third-party material depicted in the
approximate visualization. A license applies only to rights held by the
project contributors or otherwise authorized for licensing.

The MIT license text is reproduced from the SPDX License List. CERN-OHL-P-2.0
is reproduced in `../LICENSE` in its unmodified form. See
[CERN's definitive license page](https://cern-ohl.web.cern.ch/) and the
[SPDX entry for MIT](https://spdx.org/licenses/MIT.html).
