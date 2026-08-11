#!/usr/bin/env python
"""CATIA Cylinder Demo - creates a simple cylinder using CATIA COM API.

This demonstrates the same operations that the MCP server performs.
Run this with CATIA open to see it work.
"""

import win32com.client

def create_cylinder_demo():
    """Create a cylinder: 50mm diameter, 100mm height."""

    # Connect to CATIA
    print("Connecting to CATIA...")
    catia = win32com.client.Dispatch("CATIA.Application")
    catia.Visible = True

    # Create new part document
    print("Creating new part document...")
    docs = catia.Documents
    doc = docs.Add("Part")
    part = doc.Part

    # Get the body
    bodies = part.Bodies
    body = bodies.Item(1)

    # Get origin elements (reference planes)
    origin = part.OriginElements
    plane_xy = origin.PlaneXY

    # Create sketch on XY plane
    print("Creating sketch on XY plane...")
    sketches = body.Sketches
    sketch = sketches.Add(plane_xy)

    # Open sketch for editing
    sketch.OpenEdition()

    # Draw circle (radius = 25mm for 50mm diameter)
    print("Drawing circle (radius 25mm)...")
    factory = sketch.Factory2D
    circle = factory.CreateClosedCircle(0, 0, 25)

    # Close sketch
    sketch.CloseEdition()

    # Create pad (extrusion) - 100mm height
    print("Creating pad (100mm)...")
    shape_factory = part.ShapeFactory
    pad = shape_factory.AddNewPad(sketch, 100)

    # Update part
    print("Updating part...")
    part.Update()

    # Fit view
    print("Fitting view...")
    window = catia.ActiveWindow
    viewer = window.ActiveViewer
    viewer.Reframe()

    print("\n[SUCCESS] Cylinder created successfully!")
    print("  - Diameter: 50mm")
    print("  - Height: 100mm")

if __name__ == "__main__":
    try:
        create_cylinder_demo()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        print("\nMake sure:")
        print("  1. CATIA is running")
        print("  2. You have pywin32 installed: pip install pywin32")
        print("  3. Python is running as Administrator (if needed)")
