# Changelog

## 2026-11-23 — repository baseline

- Organized the parametric CAD, printable exports, interactive assembly viewer,
  controller and project references into a single repository.
- Shifted the pan servo case seat to respect the C044 12.5 mm output-axis offset
  while preserving the base's central output port.
- Lowered the tilt servo case cradle relative to its fixed output axis while
  preserving the existing bracket/yoke hole pattern.
- Replaced the passive-side tilt bearing in the assembly with a printed
  21.6 mm pivot for the nominal 22 mm yoke bore; archived older sleeve variants.
- Recorded the observed ID 1 servo fault and outstanding physical checks.

## 2026-11-23 — documentation and repository controls

- Added a preliminary procurement BOM and staged verification plan with explicit
  fit, balance, motion and release gates.
- Added contribution rules protecting the existing servo output-axis interfaces.
- Pinned the direct Python dependency versions used for the current CAD export.
- Recorded the lack of CI, automated mechanical regression coverage and a
  selected reuse license so repository maturity is explicit.

## 2026-11-23 — portable Windows setup

- Added a one-time setup script that creates a repository-local Python 3.13
  environment and installs the pinned dependencies.
- Updated the motor-control launcher and setup guide to use that environment
  after cloning or copying the repository to another Windows PC.