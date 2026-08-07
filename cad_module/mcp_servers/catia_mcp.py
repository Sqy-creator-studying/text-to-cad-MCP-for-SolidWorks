#!/usr/bin/env python
"""CATIA MCP Server — bridge Claude to CATIA via COM automation.

CATIA V5/V6 COM API key objects:
  - CATIA.Application: Main application interface
  - PartDocument: Part design document
  - Sketcher: 2D sketch creation
  - Part.ShapeFactory: 3D feature creation (Pad, Pocket, etc.)
  - HybridShapeFactory: Hybrid/surface features

Usage (Claude Code auto-launches this):
    python d:/text-to-cad/cad_module/mcp_servers/catia_mcp.py
"""

from __future__ import annotations

import asyncio
import sys
import traceback

# ── CATIA COM connection ──────────────────────────────────────────────────
# Cached globals so we don't reconnect on every tool call.

_catia: object | None = None       # CATIA.Application
_doc: object | None = None         # Active PartDocument
_part: object | None = None        # Part from PartDocument


def _connect():
    """Return (catia_app, document, part). Connects to running CATIA instance."""
    global _catia, _doc, _part

    if _catia is not None:
        return _catia, _doc, _part

    import win32com.client

    try:
        _catia = win32com.client.Dispatch("CATIA.Application")
    except Exception as exc:
        raise RuntimeError(
            "Cannot connect to CATIA.\n\n"
            "  Make sure CATIA is OPEN and running.\n"
            "  If CATIA is running but COM isn't responding, try:\n"
            "    1. Close and reopen CATIA\n"
            "    2. Run as Administrator\n"
            f"\nOriginal error: {exc}"
        ) from exc

    _catia.Visible = True

    # Get active document or create new part
    try:
        _doc = _catia.ActiveDocument
        if _doc is None:
            raise RuntimeError("No active document")
    except Exception:
        # No active document, we'll create one when needed
        _doc = None
        _part = None
        return _catia, _doc, _part

    # Get the part from the document
    try:
        _part = _doc.Part
    except Exception:
        _part = None

    return _catia, _doc, _part


def _ensure_part_document():
    """Ensure we have an active part document."""
    global _doc, _part
    catia, doc, part = _connect()

    if doc is None or part is None:
        # Create new part document
        docs = catia.Documents
        _doc = docs.Add("Part")
        _part = _doc.Part
        return _catia, _doc, _part

    return catia, doc, part


# ── CATIA Helper Functions ────────────────────────────────────────────────

def _catia_new_part():
    """Create a new part document."""
    global _doc, _part
    catia, _, _ = _connect()

    docs = catia.Documents
    _doc = docs.Add("Part")
    _part = _doc.Part

    return f"New part document created: {_doc.Name}"


def _catia_create_sketch(plane_name: str = "xy"):
    """Create a sketch on a reference plane.

    Args:
        plane_name: "xy", "yz", or "zx" plane
    """
    catia, doc, part = _ensure_part_document()

    # Get the reference planes
    # CATIA planes: xy, yz, zx
    plane_map = {
        "xy": 1,  # XY plane
        "yz": 2,  # YZ plane
        "zx": 3,  # ZX plane
        "xz": 3,  # XZ plane (alias)
    }

    plane_idx = plane_map.get(plane_name.lower(), 1)

    # Get the part body
    bodies = part.Bodies
    if bodies.Count == 0:
        body = bodies.Add()
    else:
        body = bodies.Item(1)

    # Get sketches collection
    sketches = body.Sketches

    # Get the reference plane
    # Access through HybridBodies or OriginElements
    try:
        # Try to get plane from OriginElements (standard CATIA V5 approach)
        origin_elements = part.OriginElements
        plane = origin_elements.PlaneXY if plane_idx == 1 else \
                origin_elements.PlaneYZ if plane_idx == 2 else \
                origin_elements.PlaneZX
    except Exception:
        # Fallback: try HybridBodies
        hybrid_bodies = part.HybridBodies
        if hybrid_bodies.Count > 0:
            hybrid_body = hybrid_bodies.Item(1)
            hybrid_shapes = hybrid_body.HybridShapes
            plane = hybrid_shapes.Item(plane_idx)
        else:
            raise RuntimeError("Cannot find reference planes")

    # Create sketch
    sketch = sketches.Add(plane)

    return sketch, f"Sketch created on {plane_name.upper()} plane"


def _catia_draw_circle(radius_mm: float, center_x: float = 0, center_y: float = 0):
    """Draw a circle in the active sketch.

    Args:
        radius_mm: Circle radius in millimeters
        center_x: X coordinate of center in mm
        center_y: Y coordinate of center in mm
    """
    catia, doc, part = _ensure_part_document()

    # Get the active sketch (last created)
    bodies = part.Bodies
    body = bodies.Item(1)
    sketches = body.Sketches

    if sketches.Count == 0:
        raise RuntimeError("No active sketch. Create a sketch first.")

    sketch = sketches.Item(sketches.Count)

    # Open sketch for editing
    sketch.OpenEdition()

    # Get factory for 2D elements
    factory = sketch.Factory2D

    # Create circle (coordinates in mm)
    circle = factory.CreateClosedCircle(center_x, center_y, radius_mm)

    # Close sketch edition
    sketch.CloseEdition()

    return f"Circle drawn: radius={radius_mm}mm at ({center_x}, {center_y})"


def _catia_draw_rectangle(width_mm: float, height_mm: float,
                         center_x: float = 0, center_y: float = 0):
    """Draw a centered rectangle in the active sketch.

    Args:
        width_mm: Rectangle width in millimeters
        height_mm: Rectangle height in millimeters
        center_x: X coordinate of center in mm
        center_y: Y coordinate of center in mm
    """
    catia, doc, part = _ensure_part_document()

    # Get the active sketch
    bodies = part.Bodies
    body = bodies.Item(1)
    sketches = body.Sketches

    if sketches.Count == 0:
        raise RuntimeError("No active sketch. Create a sketch first.")

    sketch = sketches.Item(sketches.Count)

    # Open sketch for editing
    sketch.OpenEdition()

    # Get factory for 2D elements
    factory = sketch.Factory2D

    # Calculate corner coordinates
    x1 = center_x - width_mm / 2
    y1 = center_y - height_mm / 2
    x2 = center_x + width_mm / 2
    y2 = center_y + height_mm / 2

    # Create four lines to form rectangle
    factory.CreateLine(x1, y1, x2, y1)  # Bottom
    factory.CreateLine(x2, y1, x2, y2)  # Right
    factory.CreateLine(x2, y2, x1, y2)  # Top
    factory.CreateLine(x1, y2, x1, y1)  # Left

    # Close sketch edition
    sketch.CloseEdition()

    return f"Rectangle drawn: {width_mm}x{height_mm}mm at ({center_x}, {center_y})"


def _catia_pad(length_mm: float):
    """Extrude (Pad) the active sketch.

    Args:
        length_mm: Extrusion length in millimeters
    """
    catia, doc, part = _ensure_part_document()

    # Get the active sketch
    bodies = part.Bodies
    body = bodies.Item(1)
    sketches = body.Sketches

    if sketches.Count == 0:
        raise RuntimeError("No sketch to extrude")

    sketch = sketches.Item(sketches.Count)

    # Get ShapeFactory for 3D operations
    shape_factory = part.ShapeFactory

    # Create Pad (extrusion)
    pad = shape_factory.AddNewPad(sketch, length_mm)

    # Update the part
    part.Update()

    return f"Pad created: {length_mm}mm extrusion"


def _catia_pocket(depth_mm: float):
    """Create a pocket (cut) from the active sketch.

    Args:
        depth_mm: Pocket depth in millimeters
    """
    catia, doc, part = _ensure_part_document()

    # Get the active sketch
    bodies = part.Bodies
    body = bodies.Item(1)
    sketches = body.Sketches

    if sketches.Count == 0:
        raise RuntimeError("No sketch to cut")

    sketch = sketches.Item(sketches.Count)

    # Get ShapeFactory
    shape_factory = part.ShapeFactory

    # Create Pocket (cut)
    pocket = shape_factory.AddNewPocket(sketch, depth_mm)

    # Update the part
    part.Update()

    return f"Pocket created: {depth_mm}mm cut"


# ── MCP Server definition ──────────────────────────────────────────────────

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("catia")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="catia_get_version",
            description="Get CATIA version and build information.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="catia_new_part",
            description="Create a new part document. Call this first.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="catia_create_sketch",
            description="Create a new sketch on a reference plane.",
            inputSchema={
                "type": "object",
                "properties": {
                    "plane": {
                        "type": "string",
                        "description": "Reference plane: 'xy', 'yz', or 'zx'",
                        "enum": ["xy", "yz", "zx", "xz"],
                        "default": "xy"
                    }
                },
            },
        ),
        Tool(
            name="catia_draw_circle",
            description="Draw a circle in the active sketch. Units in millimeters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "radius": {
                        "type": "number",
                        "description": "Circle radius in millimeters",
                    },
                    "center_x": {
                        "type": "number",
                        "description": "X coordinate of center in mm (default 0)",
                        "default": 0
                    },
                    "center_y": {
                        "type": "number",
                        "description": "Y coordinate of center in mm (default 0)",
                        "default": 0
                    }
                },
                "required": ["radius"],
            },
        ),
        Tool(
            name="catia_draw_rectangle",
            description="Draw a centered rectangle in the active sketch. Units in millimeters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "width": {
                        "type": "number",
                        "description": "Rectangle width in millimeters",
                    },
                    "height": {
                        "type": "number",
                        "description": "Rectangle height in millimeters",
                    },
                    "center_x": {
                        "type": "number",
                        "description": "X coordinate of center in mm (default 0)",
                        "default": 0
                    },
                    "center_y": {
                        "type": "number",
                        "description": "Y coordinate of center in mm (default 0)",
                        "default": 0
                    }
                },
                "required": ["width", "height"],
            },
        ),
        Tool(
            name="catia_pad",
            description="Extrude (Pad) the active sketch. Units in millimeters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "length": {
                        "type": "number",
                        "description": "Extrusion length in millimeters",
                    }
                },
                "required": ["length"],
            },
        ),
        Tool(
            name="catia_pocket",
            description="Create a pocket (cut) from the active sketch. Units in millimeters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "depth": {
                        "type": "number",
                        "description": "Pocket depth in millimeters",
                    }
                },
                "required": ["depth"],
            },
        ),
        Tool(
            name="catia_update",
            description="Update the part to apply all changes.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="catia_fit_all",
            description="Fit all geometry in the view.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        return _dispatch(name, arguments)
    except Exception as exc:
        tb = traceback.format_exc()
        return [TextContent(type="text", text=f"ERROR: {exc}\n\nTraceback:\n{tb}")]


def _dispatch(name: str, args: dict) -> list[TextContent]:
    catia, doc, part = _connect()

    # ── catia_get_version ───────────────────────────────────────────────
    if name == "catia_get_version":
        version = catia.SystemConfiguration.Version
        build = catia.SystemConfiguration.Build
        return [TextContent(
            type="text",
            text=f"CATIA Version: {version}, Build: {build}"
        )]

    # ── catia_new_part ──────────────────────────────────────────────────
    if name == "catia_new_part":
        result = _catia_new_part()
        return [TextContent(type="text", text=result)]

    # ── catia_create_sketch ─────────────────────────────────────────────
    if name == "catia_create_sketch":
        plane = args.get("plane", "xy")
        _, result = _catia_create_sketch(plane)
        return [TextContent(type="text", text=result)]

    # ── catia_draw_circle ───────────────────────────────────────────────
    if name == "catia_draw_circle":
        radius = float(args["radius"])
        cx = float(args.get("center_x", 0))
        cy = float(args.get("center_y", 0))
        result = _catia_draw_circle(radius, cx, cy)
        return [TextContent(type="text", text=result)]

    # ── catia_draw_rectangle ────────────────────────────────────────────
    if name == "catia_draw_rectangle":
        width = float(args["width"])
        height = float(args["height"])
        cx = float(args.get("center_x", 0))
        cy = float(args.get("center_y", 0))
        result = _catia_draw_rectangle(width, height, cx, cy)
        return [TextContent(type="text", text=result)]

    # ── catia_pad ───────────────────────────────────────────────────────
    if name == "catia_pad":
        length = float(args["length"])
        result = _catia_pad(length)
        return [TextContent(type="text", text=result)]

    # ── catia_pocket ────────────────────────────────────────────────────
    if name == "catia_pocket":
        depth = float(args["depth"])
        result = _catia_pocket(depth)
        return [TextContent(type="text", text=result)]

    # ── catia_update ────────────────────────────────────────────────────
    if name == "catia_update":
        catia, doc, part = _ensure_part_document()
        part.Update()
        return [TextContent(type="text", text="Part updated")]

    # ── catia_fit_all ───────────────────────────────────────────────────
    if name == "catia_fit_all":
        window = catia.ActiveWindow
        viewer = window.ActiveViewer
        viewer.Reframe()
        return [TextContent(type="text", text="View fitted to all geometry")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


# ── Entry point ────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
