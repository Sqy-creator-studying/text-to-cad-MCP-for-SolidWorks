# EmbodiedCAD v0.4.0-alpha.4

## Third-phase manufacturing evidence

- Added a reproducible motor-mount simulation evidence package for the 52 mm
  PLA validation coupon.
- Added conservative PLA material envelopes and axial, torque, lateral, and
  combined load cases.
- Added a closed-form screening script that emits `simulation_evidence.json`
  and keeps the status explicitly marked as simulation-only with physical
  validation pending.
- Updated the manufacturing handoff builder so the ZIP package includes current
  simulation evidence, load cases, and rebuild instructions.
- Added regression tests for the simulation evidence labels and packaged
  handoff contents.

## Verification

- `scripts/verify.ps1` passed all seven stages:
  Natural CAD regression tests, backend smoke tests, golden demo paths,
  blind-quality benchmark, CAD Explorer node tests, CAD Explorer production
  build, and Natural CAD web application build.

## Validation boundary

This release does not claim real-world validation. CAD, mesh, software, and
simulation evidence pass; printer-specific dimensional accuracy, layer quality,
fatigue life, and operating safety remain physically unvalidated.
