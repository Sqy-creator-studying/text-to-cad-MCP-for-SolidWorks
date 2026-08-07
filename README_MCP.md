# SolidWorks MCP Server

A Model Context Protocol (MCP) server that enables Claude to control SolidWorks through COM automation.

## Features

- 🔧 Direct SolidWorks API control via Python COM
- 📐 Create parts, sketches, extrusions, and cuts
- 🌍 Multi-language support (auto-detects localized plane names)
- ✅ Tested with SolidWorks 2025 SP5

## Quick Start

### Prerequisites

- Windows OS
- SolidWorks installed and running
- Python 3.8+
- `pywin32` package

### Installation

```bash
pip install pywin32 mcp
```

### Configuration

Add to your Claude Desktop config (`claude_desktop_config.json` or `.claude/mcp.json`):

```json
{
  "mcpServers": {
    "solidworks": {
      "command": "python",
      "args": ["d:/text-to-cad/cad_module/mcp_servers/solidworks_mcp.py"]
    }
  }
}
```

### Usage

1. Open SolidWorks
2. Start Claude Code or Claude Desktop
3. Ask Claude to create CAD models:

```
Create a cylinder with radius 50mm and height 100mm in SolidWorks
```

## Available Tools

- `sw_new_part` - Create a new part document
- `sw_select_plane` - Select a reference plane (Top/Front/Right)
- `sw_create_sketch` - Insert a 2D sketch
- `sw_draw_circle` - Draw a circle
- `sw_draw_center_rect` - Draw a centered rectangle
- `sw_extrude` - Extrude a sketch
- `sw_cut_extrude` - Cut through a sketch
- `sw_select_face` - Select a face for secondary operations
- `sw_zoom_fit` - Fit the view

## Example: Creating a Motor Mount

See [MotorMount_Demo_Fixed.bas](MotorMount_Demo_Fixed.bas) for a complete VBA example.

## Technical Details

### Key Challenges Solved

1. **SelectByID2 Callout Parameter**: Uses raw `InvokeTypes` with `VT_DISPATCH` to properly pass `Nothing` (null pointer) for the Callout parameter
2. **Localized Plane Names**: Auto-detects plane names across different SolidWorks language versions
3. **Correct API Signatures**: 
   - `FeatureExtrusion2`: 24 arguments (SW 2025)
   - `FeatureCut`: 20 arguments (SW 2025)

### Units

All dimensions use **METERS** (multiply mm by 0.001).

## License

See [LICENSE](LICENSE)

## Related

Part of the [EmbodiedCAD](https://github.com/earthtojake/text-to-cad) project.
