<div align="center">

<img src="skills/cad/assets/text-to-cad-demo.gif" alt="Demo of the text-to-cad harness generating and previewing CAD geometry" width="100%">

<br>

# ⚙ Text-to-CAD with SolidWorks Integration ⚙

An open source harness for generating 3D models with AI coding agents — now with direct SolidWorks COM automation.

[![GitHub stars](https://img.shields.io/github/stars/Sqy-creator-studying/text-to-cad?style=for-the-badge&logo=github&label=Stars)](https://github.com/Sqy-creator-studying/text-to-cad/stargazers)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](requirements-cad.txt)
[![SolidWorks](https://img.shields.io/badge/SolidWorks-2025-DA291C?style=for-the-badge)](cad_module/mcp_servers/solidworks_mcp.py)
[![MCP](https://img.shields.io/badge/MCP-Server-6B46C1?style=for-the-badge)](cad_module/mcp_servers/solidworks_mcp.py)
[![build123d](https://img.shields.io/badge/build123d-CAD-00A676?style=for-the-badge)](https://github.com/gumyr/build123d)
[![STEP](https://img.shields.io/badge/STEP-Export-4A5568?style=for-the-badge)](skills/cad/SKILL.md)
[![STL](https://img.shields.io/badge/STL-Export-4A5568?style=for-the-badge)](skills/cad/SKILL.md)

</div>

## 🆕 SolidWorks Integration (NEW)

This fork adds **direct SolidWorks COM automation** — AI agents can now create real SolidWorks parts through natural language commands.

### Key Features

- **MCP Server** — 13 Claude Code tools bridging natural language → SolidWorks COM API
- **VBA Macro Generator** — Export any model as a standalone `.bas` macro for SolidWorks
- **Localized Plane Detection** — Auto-detects Chinese/English/Japanese/German reference plane names
- **SW 2025 Verified** — All API signatures tested against SolidWorks 2025 SP5

### Technical Breakthroughs

| Challenge | Solution |
|---|---|
| Python `None` → COM `VT_EMPTY` causes `SelectByID2` type mismatch | Raw `InvokeTypes` with explicit `VT_DISPATCH` null pointer |
| SW 2025 API parameter counts differ from docs | Empirically verified: `FeatureExtrusion2`=23 args, `FeatureCut`=20 args |
| Chinese SW has localized plane names | Auto-scan feature tree on connect, build English→localized map |

### MCP Server Tools

| Tool | Description |
|---|---|
| `sw_get_version` | Get SolidWorks version and revision |
| `sw_new_part` | Create a fresh part document |
| `sw_select_plane` | Select a reference plane (auto-maps English→localized names) |
| `sw_create_sketch` | Insert a 2D sketch on the selected plane/face |
| `sw_draw_circle` | Draw a circle (input: meters) |
| `sw_draw_center_rect` | Draw a center-point rectangle (input: half-dimensions, meters) |
| `sw_extrude` | Blind extrude using `FeatureExtrusion2` (23 args, SW 2025) |
| `sw_cut_extrude` | Blind cut-extrude using `FeatureCut` (20 args, SW 2025) |
| `sw_select_face` | Select a face near XYZ coordinates |
| `sw_clear_selection` | Clear all current selections |
| `sw_zoom_fit` | Zoom-to-fit the model |
| `sw_get_plane_names` | Show detected localized plane names |
| `sw_list_features` | List all features in the active document |

### Quick Start — SolidWorks MCP

```bash
# Install dependencies
pip install pywin32 mcp

# Start SolidWorks (must be running with a part open)

# Configure Claude Code (.claude/mcp.json):
{
  "mcpServers": {
    "solidworks": {
      "command": "python",
      "args": ["cad_module/mcp_servers/solidworks_mcp.py"]
    }
  }
}
```

### Quick Start — VBA Macro Export

```python
from cad_module.exporters.sw_macro import generate_sw_macro

macro = generate_sw_macro('motor_mount', {
    'plate_diameter': 52,      # mm
    'thickness': 5,
    'center_hole_diameter': 12,
    'bolt_circle_diameter': 32,
    'bolt_hole_diameter': 3.2,
    'bolt_count': 4,
})

with open('MotorMount.bas', 'w', encoding='utf-8') as f:
    f.write(macro)
# Import into SW: Alt+F11 → File → Import File → select .bas → F5
```

**Supported templates:** `box`, `cylinder`, `generic_plate`, `motor_mount`, `bracket_simple`, `bushing`, `flange`

**Supported features:** `hole`, `circular_user_hole_pattern`, `linear_hole_pattern`, `rectangular_pocket`, `obround_slot`, `fillet`, `chamfer`

---

## ✨ Original text-to-cad Features

- **Generate** - Create source-controlled CAD models with coding agents like Codex and Claude Code.
- **Export** - Produce STEP, STL, DXF, GLB, topology data, and URDF robot descriptions.
- **Browse** - Inspect generated geometry in a local CAD Explorer viewer.
- **Reference** - Copy stable `@cad[...]` references so agents can make precise follow-up edits.
- **Review** - Render quick snapshots for fast checks during an iteration loop.
- **Reproduce** - Edit source files first, then regenerate explicit targets.
- **Local** - Run the harness and viewer locally with no backend to host.

## 🧰 Bundled Skills

- **CAD Skill** - STEP, STL, DXF, GLB/topology, snapshots, and `@cad[...]` geometry references. [Bundled docs](skills/cad/README.md) · [Standalone repo](https://github.com/earthtojake/cad-skill)
- **URDF Skill** - Generated URDF XML, robot links, joints, limits, validation, and mesh references. [Bundled docs](skills/urdf/README.md) · [Standalone repo](https://github.com/earthtojake/urdf-skill)

## 🔁 Workflow

1. **Describe** - Tell your agent about the part, assembly, fixture, robot, or mechanism you want.
2. **Edit** - Let your coding agent update CAD source files under `models/`.
3. **Regenerate** - Create explicit STEP, STL, DXF, GLB, or URDF targets.
4. **Inspect** - Open the CAD Explorer viewer to review the generated model.
5. **Reference** - Copy `@cad[...]` handles when you want geometry-aware edits.
6. **Commit** - Save the source and generated artifacts together once the model is ready.

## 🚀 Quick Start

Clone the repo:

```bash
git clone https://github.com/Sqy-creator-studying/text-to-cad.git
cd text-to-cad
```

Install Python CAD dependencies:

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/pip install -r requirements-cad.txt
```

Install viewer dependencies:

```bash
cd viewer
npm install
```

Run the local CAD Explorer:

```bash
npm run dev
```

Then open [http://localhost:4178](http://localhost:4178).

## Reproducible development baseline

- CI runtime: Python 3.11 and Node.js 22.
- Supported local runtime: Python 3.11-3.13 and Node.js 22-25.
- Version hints are stored in `.python-version` and `.nvmrc`.

On Windows, run the complete backend, viewer-test, and production-build verification:

```powershell
.\scripts\verify.ps1
```

To inspect repository disk usage without deleting files:

```powershell
.\scripts\space-report.ps1
```

The release-ready product scope and explicit non-claims are documented in
[`PRODUCT_CAPABILITY_BOUNDARIES.md`](PRODUCT_CAPABILITY_BOUNDARIES.md). The
three reproducible presentation paths are defined in
`cad_module/examples/golden_demo_paths.json` and verified by the main release
check. The independent holdout quality suite and non-regression thresholds live
in `cad_module/examples/blind_quality_cases.json` and
`cad_module/examples/blind_quality_baseline.json`.

## 📜 License

This project is licensed under the **Apache License 2.0** — see [LICENSE](LICENSE) for the full text.

**What Apache 2.0 means for you:**

- ✅ 自由使用、修改、分发，商业用途也可以
- ✅ 明确授予专利权，不用担心专利被诉
- ✅ 修改后的代码可以闭源，不需要强制开源
- ⚠️ 分发时必须保留版权声明和 LICENSE 文件
- ⚠️ 修改过的文件需要标注变更

Portions derived from [text-to-cad](https://github.com/earthtojake/text-to-cad) by Thompson Labs, originally MIT-licensed. The original MIT notice is preserved in [LICENSE](LICENSE).

---

**Author:** Sqy-creator-studying  
**Based on:** [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad)  
**Copyright:** © 2026 Sqy-creator-studying
