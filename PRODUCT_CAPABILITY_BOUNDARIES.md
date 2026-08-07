# EmbodiedCAD Capability Boundaries

This document defines what the current `v0.3` engineering prototype proves and what it does not claim.

## Supported and validated

| Area | Current support | Validation evidence |
| --- | --- | --- |
| Natural-language input | Controlled Chinese and English parameter extraction | 100 initial-language acceptance cases |
| Multi-turn editing | Parameter changes, controlled features, undo, redo, and revision comparison | 50 conversation cases and golden revision path |
| Part families | 10 controlled parametric families | Generation matrix and STEP measurement checks |
| Controlled features | Holes, rectangular/circular patterns, rectangular pockets, axis-aware obround slots, deletion, fillet, and chamfer within family limits | Cross-family feature geometry validation tests |
| Part exports | STEP, STL, and GLB | File checks, STEP solid/topology measurement, and viewer builds |
| Assembly planning | Drone and 3-DOF robot-arm baseline assemblies | Assembly constraint and engineering-check matrix |
| Robot export | URDF links, joints, limits, meshes, and viewer joint animation | URDF tree checks and CAD Explorer node tests |
| Engineering estimates | Bounding box, volume, center of mass, estimated mass, basic manufacturing readiness | Automated regression and acceptance reports |
| Interfaces | Python API, FastAPI endpoints, CLI, MCP tools, and two local web viewers | Backend smoke, MCP smoke, node tests, and production builds |

## Independent quality baseline

The third-stage holdout suite is authored independently from the main acceptance
cases. Its release thresholds currently require 100% for intent accuracy,
parameter accuracy, clarification behavior, controlled-feature generation,
invalid-design rejection, and overall case success.

```powershell
.\.venv\Scripts\python.exe cad_module\examples\blind_quality_benchmark.py `
  --output cad_module\reports\ci\blind_quality_report.json
```

## Controlled limitations

- Requests outside the registered part families may require clarification or be rejected.
- The system does not execute arbitrary model-generated CAD code.
- External LLM interpretation is optional. Rule-mode behavior is the reproducible baseline.
- Assembly collision and clearance checks are planning-level checks, not full motion-planning certification.
- Manufacturing readiness uses explicit rule thresholds and material/process compatibility tables.
- Generated dimensions use millimeters unless a supported request explicitly establishes another unit.

## Not currently claimed

- Structural strength, fatigue life, vibration durability, thermal certification, or solver convergence guarantees.
- GD&T, tolerance-stack analysis, surface-finish validation, or machining setup planning.
- Watertightness, ingress-protection certification, electrical safety, or regulatory compliance.
- Drop-in compatibility with every CAD kernel or proprietary CAD feature history.
- Unrestricted generation of arbitrary freeform surfaces or novel mechanical topology.
- Production safety approval for aircraft, robots, medical devices, vehicles, or other regulated products.

## Release evidence

Run the complete local release check:

```powershell
.\scripts\verify.ps1
```

Run only the three presentation-ready golden paths:

```powershell
.\.venv\Scripts\python.exe cad_module\examples\golden_demo_paths.py `
  --output cad_module\reports\ci\golden_demo_report.json
```

The golden paths validate:

1. A Chinese mounting-plate request producing validated STEP, STL, and GLB files.
2. A two-revision bushing workflow with expected geometry delta plus undo and redo.
3. Drone and robot-arm assemblies producing validated STEP/GLB artifacts and URDF trees.
