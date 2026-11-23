# Contributing and design-change workflow

This is a personal engineering prototype repository. Changes must preserve the
distinction between measured inputs, datasheet values, assumptions and
illustrative geometry.

## Source and generated files

- The parametric mechanical source is src/hubble_stand.py. Change dimensions
  there rather than editing STL or STEP exports as the only design copy.
- Rebuild exports from the repository root with the CAD command in README.md.
  Commit source and regenerated exports together when geometry changes.
- The Hubble visualization is generated separately and is not printable or
  brick-accurate. Keep its geometry out of structural sizing.
- The interactive viewer is generated from the visual GLB. Regenerate it when
  the embedded model changes.
- Keep old designs only when they have traceable value; move superseded files
  to exports/archive and label them as historical.

## Engineering records

- Use millimetres in CAD and documents unless a source explicitly uses another
  unit; show conversions where they matter.
- Add a code comment and update engineering_notes.md whenever a dimension,
  interface or load assumption changes.
- Label every new dimension as measured, from a cited drawing/datasheet, or
  provisional. Do not infer a precise LEGO dimension from a perspective image.
- Update the BOM, assembly notes, project status and verification plan when a
  change affects fit, hardware, assembly sequence or safety.
- Add a dated entry to CHANGELOG.md and retain the relevant hardware-test history.
- Never present a rendering or nominal CAD clearance as a physical fit or
  load-validation result.

## Protected interfaces and review

The existing servo output-axis openings and their mating hole patterns are
protected interfaces. Do not move them when adjusting a case cradle or retainer.
Preserve the printed tilt-bracket/yoke mounting pattern unless the owner
explicitly changes that constraint. If a required change would alter one of
these interfaces, explain the impact and get direction before changing CAD.

Before committing a geometry change, review the affected assembly and compare
the exported part with the existing printed hardware it is intended to reuse.
Do not claim a design has passed a fit or load test unless the corresponding
physical test is recorded.

## Repository hygiene

Use focused commits with clear present-tense summaries. Keep source, docs and
generated outputs in sync. Do not commit machine-specific secrets, private
hardware logs from outside this project, slicer machine files, or temporary
render frames.
