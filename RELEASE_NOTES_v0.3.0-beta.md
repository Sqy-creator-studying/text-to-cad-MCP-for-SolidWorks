# EmbodiedCAD v0.3.0-beta

`v0.3.0-beta` is the first release candidate backed by a reproducible local release gate and three presentation-ready golden workflows.

## Release evidence

- 48 Natural CAD regression tests pass.
- 36 backend integration and smoke tests pass.
- 70 CAD Explorer node tests pass.
- Chinese parameterized-part generation passes with STEP, STL, and GLB outputs.
- Multi-turn revision comparison, undo, and redo pass with measured geometry deltas.
- Drone and robot-arm assembly generation passes with STEP, GLB, and URDF evidence.
- CAD Explorer and Natural CAD web applications both produce successful production builds.
- Both frontend dependency trees report zero known npm vulnerabilities.

## Golden presentation paths

1. `生成一个100x60x4 mm、四角带M5孔的安装板`
2. `create a bushing 30x20x40 mm`, followed by `change length to 45 mm`
3. `create a new 3dof robot arm project`, followed by assembly and URDF export

Run all release checks:

```powershell
.\scripts\verify.ps1
```

## Scope

This beta demonstrates controlled and validated parametric CAD generation. It does not claim structural certification, GD&T validation, unrestricted freeform modeling, or production safety approval. See `PRODUCT_CAPABILITY_BOUNDARIES.md` for the complete support matrix.

## Known release warnings

- The Natural CAD web bundle remains larger than 500 kB and should be code-split in a later performance pass.
- External LLM connectivity is optional and is not part of the reproducible rule-mode baseline.
- Remote GitHub Actions status requires authenticated access because the target repository is private.
