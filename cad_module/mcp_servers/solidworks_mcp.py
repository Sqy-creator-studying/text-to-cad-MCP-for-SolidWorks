#!/usr/bin/env python
"""SolidWorks MCP Server — bridge Claude to SolidWorks via COM automation.

Key technical findings for SW 2025 SP5:
  - SelectByID2: MUST use raw InvokeTypes with VT_DISPATCH type for Callout
    (Python None maps to VT_EMPTY, but SW expects VT_DISPATCH null pointer)
  - FeatureExtrusion2: 23 args (NOT 14, NOT 25)
  - FeatureCut: 20 args (NOT 14, NOT 23, NOT 26)
  - Plane names are LOCALIZED (e.g., Chinese SW uses 上视基准面 not Top Plane)

Usage (Claude Code auto-launches this):
    python d:/text-to-cad/cad_module/mcp_servers/solidworks_mcp.py
"""

from __future__ import annotations

import asyncio
import sys
import traceback

# ── SolidWorks COM connection ──────────────────────────────────────────────
# Cached globals so we don't reconnect on every tool call.

_sw: object | None = None          # dynamic.Dispatch SldWorks.Application
_sw_ole: object | None = None      # raw PyIDispatch pointer
_plane_names: dict[str, str] = {}  # English → localized plane name mapping
_model: object | None = None       # Current active ModelDoc2


def _connect():
    """Return (sw_app, sw_ole, plane_names, model). Auto-detects plane names."""
    global _sw, _sw_ole, _plane_names, _model

    if _sw is not None:
        return _sw, _sw_ole, _plane_names, _model

    import pythoncom
    import win32com.client
    from win32com.client import dynamic

    try:
        _sw = dynamic.Dispatch("SldWorks.Application")
    except Exception as exc:
        raise RuntimeError(
            "Cannot connect to SolidWorks.\n\n"
            "  Make sure SolidWorks is OPEN and a part/assembly/doc is loaded.\n"
            "  If SW is running but the COM server isn't responding, try:\n"
            "    1. Close and reopen SolidWorks\n"
            "    2. Run as Administrator\n"
            f"\nOriginal error: {exc}"
        ) from exc

    _sw.Visible = True
    _sw_ole = _sw._oleobj_

    # Detect plane names from active doc or a new part
    try:
        _model = _sw.ActiveDoc
    except Exception:
        _model = None

    if _model is None:
        _model = _sw.NewPart
    else:
        # Active doc exists — use it directly
        pass

    _plane_names = _detect_plane_names()
    return _sw, _sw_ole, _plane_names, _model


def _detect_plane_names() -> dict[str, str]:
    """Scan feature tree for RefPlane features and map to English names.

    Default plane naming conventions across SW localizations:
      - English:   Top Plane / Front Plane / Right Plane
      - Chinese:   上视基准面 / 前视基准面 / 右视基准面
      - Japanese:  平面（上面）/ 平面（前面）/ 平面（右面）
      - German:    Oben / Vorne / Rechts
    """
    import pythoncom

    name_map: dict[str, str] = {}
    if _model is None:
        return name_map

    try:
        feat = _model.FirstFeature
    except Exception:
        return name_map

    ref_planes: list[str] = []
    while feat:
        try:
            tname = feat.GetTypeName
            if tname == "RefPlane":
                ref_planes.append(feat.Name)
        except Exception:
            pass
        try:
            feat = feat.GetNextFeature
        except Exception:
            break

    # Heuristic: assume feature order is Front, Top, Right (common in SW)
    # We try both position-based and substring-based matching.
    if len(ref_planes) >= 3:
        # Position-based (most SW versions list them Front/Top/Right)
        name_map["front plane"] = ref_planes[0]
        name_map["top plane"] = ref_planes[1]
        name_map["right plane"] = ref_planes[2]

    # Keyword-based fallback (overwrites position-based if ambiguous)
    for p in ref_planes:
        lower = p.lower()
        if "top" in lower or "上" in p or "上面" in p or "oben" in p:
            name_map["top plane"] = p
        elif "front" in lower or "前" in p or "前面" in p or "vorne" in p:
            name_map["front plane"] = p
        elif "right" in lower or "右" in p or "右面" in p or "rechts" in p:
            name_map["right plane"] = p

    return name_map


def _resolve_plane(name: str) -> str:
    """Resolve a plane name: try exact match, then English→localized map."""
    key = name.strip().lower()
    if key in _plane_names:
        return _plane_names[key]
    # If already localized name
    return name


# ── Low-level SolidWorks helpers ──────────────────────────────────────────

def _sw_select(name: str, seltype: str, x: float = 0.0, y: float = 0.0,
               z: float = 0.0, append: bool = False, mark: int = 0) -> bool:
    """Select geometry via raw InvokeTypes (handles Callout=Nothing properly).

    This is THE critical workaround: Python's COM bridge maps None → VT_EMPTY,
    but SolidWorks SelectByID2 expects VT_DISPATCH with null pointer (VBA Nothing).
    By using raw InvokeTypes with explicit type annotation (VT_DISPATCH, PARAMFLAG_FIN),
    the pywin32 C++ layer creates the correct VARIANT.
    """
    import pythoncom

    _, _, _, model = _connect()
    ext = model.Extension._oleobj_

    dispid = ext.GetIDsOfNames('SelectByID2')
    arg_types = (
        (pythoncom.VT_BSTR, pythoncom.PARAMFLAG_FIN),      # Name
        (pythoncom.VT_BSTR, pythoncom.PARAMFLAG_FIN),      # Type
        (pythoncom.VT_R8, pythoncom.PARAMFLAG_FIN),        # X
        (pythoncom.VT_R8, pythoncom.PARAMFLAG_FIN),        # Y
        (pythoncom.VT_R8, pythoncom.PARAMFLAG_FIN),        # Z
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),      # Append
        (pythoncom.VT_I4, pythoncom.PARAMFLAG_FIN),        # Mark
        (pythoncom.VT_DISPATCH, pythoncom.PARAMFLAG_FIN),  # Callout ← KEY!
        (pythoncom.VT_I4, pythoncom.PARAMFLAG_FIN),        # SelectOption
    )

    result = ext.InvokeTypes(
        dispid, 0, pythoncom.DISPATCH_METHOD,
        (pythoncom.VT_BOOL, 0), arg_types,
        name, seltype, x, y, z, append, mark, None, 0,
    )
    return bool(result)


def _sw_extrude(depth: float) -> object:
    """Blind extrude via FeatureExtrusion2 (24 args for SW 2025)."""
    _, _, _, model = _connect()
    d = float(depth)
    return model.FeatureManager.FeatureExtrusion2(
        True,   # Sd — single direction
        False,  # Flip
        False,  # Dir
        0,      # T1 (0=Blind)
        0,      # T2
        d,      # D1 — blind depth
        d,      # D2
        False,  # DraftOutward
        False,  # DraftOutward2
        False,  # DraftDir
        False,  # DraftDir2
        0.0,    # T3
        0.0,    # D3
        False,  # T4  ← NOTE: bool in this position per SW 2025 24-arg sig
        False,  # D4
        False,  # ...
        False,  # ...
        True,   # Merge
        True,   # UseFeatScope
        True,   # UseAutoSelect
        0.0,    # StartOffset
        0.0,    # EndOffset
        False,  # UseDirection2
    )


def _sw_cut(depth: float) -> object:
    """Blind cut-extrude via FeatureCut (20 args for SW 2025).

    Uses raw InvokeTypes because dynamic Dispatch can't handle the exact
    20-arg signature — it would try different overloads and fail.
    """
    import pythoncom

    _, _, _, model = _connect()
    d = float(depth)
    fmgr_ole = model.FeatureManager._oleobj_

    dispid = fmgr_ole.GetIDsOfNames('FeatureCut')
    arg_types = (
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 1: Sd
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 2: Flip
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 3: Dir
        (pythoncom.VT_I4, pythoncom.PARAMFLAG_FIN),    # 4: T1
        (pythoncom.VT_I4, pythoncom.PARAMFLAG_FIN),    # 5: T2
        (pythoncom.VT_R8, pythoncom.PARAMFLAG_FIN),    # 6: D1
        (pythoncom.VT_R8, pythoncom.PARAMFLAG_FIN),    # 7: D2
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 8: DraftOutward
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 9: DraftOutward2
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 10: DraftDir
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 11: DraftDir2
        (pythoncom.VT_R8, pythoncom.PARAMFLAG_FIN),    # 12: T3
        (pythoncom.VT_R8, pythoncom.PARAMFLAG_FIN),    # 13: D3
        (pythoncom.VT_R8, pythoncom.PARAMFLAG_FIN),    # 14: T4
        (pythoncom.VT_R8, pythoncom.PARAMFLAG_FIN),    # 15: D4
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 16: Flip2
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 17: DraftOutward3
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 18: DraftOutward4
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 19: Merge
        (pythoncom.VT_BOOL, pythoncom.PARAMFLAG_FIN),  # 20: UseFeatScope
    )
    vals = (
        True,   # Sd
        False,  # Flip
        False,  # Dir
        0,      # T1 = Blind
        0,      # T2 = Blind
        d,      # D1
        d,      # D2
        False,  # DraftOutward
        False,  # DraftOutward2
        False,  # DraftDir
        False,  # DraftDir2
        0.0,    # T3
        0.0,    # D3
        0.0,    # T4
        0.0,    # D4
        False,  # Flip2
        False,  # DraftOutward3
        False,  # DraftOutward4
        True,   # Merge
        True,   # UseFeatScope
    )

    result = fmgr_ole.InvokeTypes(
        dispid, 0, pythoncom.DISPATCH_METHOD,
        (pythoncom.VT_DISPATCH, 0), arg_types,
        *vals,
    )
    return result


# ── MCP Server definition ──────────────────────────────────────────────────

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("solidworks")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="sw_get_version",
            description="Get SolidWorks version, service pack, and revision number.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="sw_new_part",
            description="Create a fresh part document. Always call this first.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="sw_select_plane",
            description="Select a named reference plane. Use English names: 'Top Plane', 'Front Plane', 'Right Plane' (auto-mapped to localized names).",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Plane name in English: 'Top Plane', 'Front Plane', 'Right Plane'",
                    }
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="sw_create_sketch",
            description="Insert a new 2D sketch on the currently-selected plane or face.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="sw_draw_circle",
            description="Draw a circle in the active sketch. Units: METERS (multiply mm by 0.001).",
            inputSchema={
                "type": "object",
                "properties": {
                    "radius": {
                        "type": "number",
                        "description": "Circle radius in METERS (mm * 0.001)",
                    }
                },
                "required": ["radius"],
            },
        ),
        Tool(
            name="sw_draw_center_rect",
            description="Draw a center-point rectangle. Pass half-width and half-height in METERS.",
            inputSchema={
                "type": "object",
                "properties": {
                    "hw": {"type": "number", "description": "Half-width in METERS"},
                    "hh": {"type": "number", "description": "Half-height in METERS"},
                },
                "required": ["hw", "hh"],
            },
        ),
        Tool(
            name="sw_extrude",
            description="Blind extrude the active sketch. depth in METERS. Uses FeatureExtrusion2 (23 args, SW 2025 verified).",
            inputSchema={
                "type": "object",
                "properties": {
                    "depth": {"type": "number", "description": "Extrusion depth in METERS"},
                },
                "required": ["depth"],
            },
        ),
        Tool(
            name="sw_cut_extrude",
            description="Blind cut-extrude through the active sketch. depth in METERS. Uses FeatureCut (20 args, SW 2025 correct).",
            inputSchema={
                "type": "object",
                "properties": {
                    "depth": {"type": "number", "description": "Cut depth in METERS"},
                },
                "required": ["depth"],
            },
        ),
        Tool(
            name="sw_select_face",
            description="Select a face near the given XYZ point. Use before sw_create_sketch for cuts/holes on a surface. XYZ in METERS.",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "X in METERS"},
                    "y": {"type": "number", "description": "Y in METERS"},
                    "z": {"type": "number", "description": "Z in METERS"},
                },
                "required": ["x", "y", "z"],
            },
        ),
        Tool(
            name="sw_clear_selection",
            description="Clear all current selections.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="sw_zoom_fit",
            description="Zoom-to-fit the model in the graphics area.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="sw_get_plane_names",
            description="Return the localized plane names detected in this SW installation.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="sw_list_features",
            description="List all features in the active document tree (useful for debugging plane names).",
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
    sw, sw_ole, planes, model = _connect()

    # ── sw_get_version ──────────────────────────────────────────────────
    if name == "sw_get_version":
        rev = sw.RevisionNumber
        major = int(rev) // 10000
        minor = (int(rev) % 10000) // 100
        sp = int(rev) % 100
        return [TextContent(
            type="text",
            text=f"Version: SolidWorks {major}.{minor} SP{sp}  (revision={rev})"
        )]

    # ── sw_new_part ─────────────────────────────────────────────────────
    if name == "sw_new_part":
        global _model, _plane_names
        _model = sw.NewPart
        # Re-detect plane names for the new part
        _plane_names = _detect_plane_names()
        if _model is None:
            return [TextContent(type="text", text="ERROR: NewPart succeeded but ActiveDoc is None!")]
        return [TextContent(type="text",
            text=f"New part created. Planes: {_plane_names}"
        )]

    # ── sw_get_plane_names ──────────────────────────────────────────────
    if name == "sw_get_plane_names":
        return [TextContent(
            type="text",
            text=f"Localized plane names: {planes}\n"
                 f"Use English names when calling sw_select_plane."
        )]

    # ── sw_list_features ────────────────────────────────────────────────
    if name == "sw_list_features":
        lines = []
        try:
            feat = model.FirstFeature
            while feat:
                try:
                    lines.append(f"  [{feat.GetTypeName}] \"{feat.Name}\"")
                except Exception:
                    pass
                feat = feat.GetNextFeature
        except Exception as e:
            lines.append(f"ERROR: {e}")
        return [TextContent(type="text", text="\n".join(lines))]

    # ── sw_select_plane ─────────────────────────────────────────────────
    if name == "sw_select_plane":
        plane = _resolve_plane(args["name"])
        ok = _sw_select(plane, "PLANE")
        return [TextContent(type="text",
            text=f"SelectByID2('{plane}', PLANE) -> {'SELECTED' if ok else 'FAILED'}"
        )]

    # ── sw_create_sketch ────────────────────────────────────────────────
    if name == "sw_create_sketch":
        model.SketchManager.InsertSketch(True)
        return [TextContent(type="text", text="Sketch inserted.")]

    # ── sw_draw_circle ──────────────────────────────────────────────────
    if name == "sw_draw_circle":
        r = float(args["radius"])
        model.SketchManager.CreateCircleByRadius(0.0, 0.0, 0.0, r)
        return [TextContent(type="text", text=f"Circle r={r}m ({r*1000}mm) drawn.")]

    # ── sw_draw_center_rect ─────────────────────────────────────────────
    if name == "sw_draw_center_rect":
        hw = float(args["hw"]); hh = float(args["hh"])
        model.SketchManager.CreateCenterRectangle(0.0, 0.0, 0.0, hw, hh, 0.0)
        return [TextContent(type="text", text=f"CenterRect hw={hw}m hh={hh}m drawn.")]

    # ── sw_extrude ──────────────────────────────────────────────────────
    if name == "sw_extrude":
        d = float(args["depth"])
        feat = _sw_extrude(d)
        return [TextContent(type="text",
            text=f"Extruded {d}m ({d*1000}mm) via FeatureExtrusion2(24 args)."
        )]

    # ── sw_cut_extrude ──────────────────────────────────────────────────
    if name == "sw_cut_extrude":
        d = float(args["depth"])
        feat = _sw_cut(d)
        return [TextContent(type="text",
            text=f"Cut {d}m ({d*1000}mm) via FeatureCut(20 args)."
        )]

    # ── sw_select_face ──────────────────────────────────────────────────
    if name == "sw_select_face":
        x = float(args["x"]); y = float(args["y"]); z = float(args["z"])
        ok = _sw_select("", "FACE", x, y, z)
        return [TextContent(type="text",
            text=f"SelectByID2(FACE, {x},{y},{z}) -> {'SELECTED' if ok else 'FAILED'}"
        )]

    # ── sw_clear_selection ──────────────────────────────────────────────
    if name == "sw_clear_selection":
        model.ClearSelection2(True)
        return [TextContent(type="text", text="Selection cleared.")]

    # ── sw_zoom_fit ─────────────────────────────────────────────────────
    if name == "sw_zoom_fit":
        model.ViewZoomtofit2()
        return [TextContent(type="text", text="Zoomed to fit.")]

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
