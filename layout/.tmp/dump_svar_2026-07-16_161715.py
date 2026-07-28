import pya
layout = pya.Layout()
layout.read("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds")
cell = layout.cell("SVaricap")
m1_idx = layout.layer(8, 0)
m2_idx = layout.layer(10, 0)
via1_idx = layout.layer(19, 0)
print("=== SVaricap M1 (8/0) ===")
for s in cell.shapes(m1_idx).each():
    if s.is_box():
        b = s.box
        print(f"  ({b.left*0.001:.3f}, {b.bottom*0.001:.3f})-({b.right*0.001:.3f}, {b.top*0.001:.3f})")
    elif s.is_polygon():
        bb = s.polygon.bbox()
        print(f"  poly bbox: ({bb.left*0.001:.3f}, {bb.bottom*0.001:.3f})-({bb.right*0.001:.3f}, {bb.top*0.001:.3f})")
print("\n=== SVaricap M2 (10/0) ===")
for s in cell.shapes(m2_idx).each():
    if s.is_box():
        b = s.box
        print(f"  ({b.left*0.001:.3f}, {b.bottom*0.001:.3f})-({b.right*0.001:.3f}, {b.top*0.001:.3f})")
print("\n=== SVaricap Via1 (19/0) ===")
for s in cell.shapes(via1_idx).each():
    if s.is_box():
        b = s.box
        print(f"  ({b.left*0.001:.3f}, {b.bottom*0.001:.3f})-({b.right*0.001:.3f}, {b.top*0.001:.3f})")