# CATIA MCP Server

A Model Context Protocol (MCP) server that enables Claude to control CATIA via COM automation.

## Features

- 🔧 Direct CATIA V5/V6 API control via Python COM
- 📐 Create parts, sketches, pads, and pockets
- 🎯 Simple and intuitive API (millimeters by default)
- ✅ Compatible with CATIA V5 R20+ and CATIA V6

## Quick Start

### Prerequisites

- Windows OS
- CATIA V5 or V6 installed and running
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
    "catia": {
      "command": "python",
      "args": ["d:/text-to-cad/cad_module/mcp_servers/catia_mcp.py"]
    }
  }
}
```

### Usage

1. Open CATIA
2. Start Claude Code or Claude Desktop
3. Ask Claude to create CAD models:

```
Create a cylinder with 50mm diameter and 100mm height in CATIA
```

## Available Tools

### Document Management
- `catia_new_part` - Create a new part document
- `catia_update` - Update the part to apply all changes
- `catia_fit_all` - Fit all geometry in the view

### Sketching
- `catia_create_sketch` - Create a sketch on a reference plane (xy/yz/zx)
- `catia_draw_circle` - Draw a circle (radius in mm)
- `catia_draw_rectangle` - Draw a centered rectangle (width/height in mm)

### 3D Features
- `catia_pad` - Extrude a sketch (length in mm)
- `catia_pocket` - Cut through a sketch (depth in mm)

## Example Workflows

### Example 1: Simple Cylinder

```python
# Ask Claude:
"Create a cylinder: diameter 50mm, height 100mm"

# Claude will execute:
1. catia_new_part()
2. catia_create_sketch(plane="xy")
3. catia_draw_circle(radius=25)  # diameter/2
4. catia_pad(length=100)
5. catia_fit_all()
```

### Example 2: Box with Hole

```python
# Ask Claude:
"Create a 100x100x50mm box with a centered 30mm diameter hole through it"

# Claude will execute:
1. catia_new_part()
2. catia_create_sketch(plane="xy")
3. catia_draw_rectangle(width=100, height=100)
4. catia_pad(length=50)
5. catia_create_sketch(plane="xy")  # on top face
6. catia_draw_circle(radius=15)
7. catia_pocket(depth=50)
8. catia_fit_all()
```

### Example 3: Motor Mount Bracket

```python
# Ask Claude:
"Create a motor mount: 80x60mm base plate, 10mm thick, 
with four M4 mounting holes (5mm diameter) at corners (10mm from edges)"

# Claude will create the base and add holes automatically
```

## Technical Details

### Coordinate System

CATIA uses:
- **XY plane** - Top view (default)
- **YZ plane** - Right side view
- **ZX plane** - Front view

### Units

All dimensions use **MILLIMETERS** (CATIA's default unit).

### API Structure

```
CATIA.Application
  └─ Documents
      └─ PartDocument
          └─ Part
              ├─ Bodies
              │   └─ Sketches
              │       └─ Factory2D (2D geometry)
              └─ ShapeFactory (3D features)
```

### Key CATIA COM Objects

- **CATIA.Application** - Main application interface
- **PartDocument** - Part design document
- **Part.Bodies** - Collection of bodies
- **Sketches** - Collection of 2D sketches
- **Factory2D** - 2D geometry creation (circles, lines, etc.)
- **ShapeFactory** - 3D feature creation (Pad, Pocket, etc.)
- **OriginElements** - Reference planes (PlaneXY, PlaneYZ, PlaneZX)

## Comparison with SolidWorks MCP

| Feature | SolidWorks MCP | CATIA MCP |
|---------|---------------|-----------|
| Units | Meters (×0.001) | Millimeters (native) |
| Planes | Named (Top/Front/Right) | Coordinate (XY/YZ/ZX) |
| Extrusion | `sw_extrude` | `catia_pad` |
| Cut | `sw_cut_extrude` | `catia_pocket` |
| Localization | Auto-detected | Not needed |

## Troubleshooting

### "Cannot connect to CATIA"

1. Make sure CATIA is running
2. Try running Python as Administrator
3. Check if CATIA COM automation is enabled

### "No active sketch"

Create a sketch first using `catia_create_sketch` before drawing.

### Geometry not visible

Call `catia_update()` to refresh the part, then `catia_fit_all()` to zoom.

## License

See [LICENSE](LICENSE)

## Related Projects

- [SolidWorks MCP Server](README_MCP.md)
- [EmbodiedCAD](https://github.com/earthtojake/text-to-cad)
