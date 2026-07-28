import pya

layout = pya.Layout()
layout.read("/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G_XTOR.gds")

top = [c for c in layout.each_cell() if c.name == "VCO_77G_XTOR"][0]
m4_li = layout.layer(50, 0)
m3_li = layout.layer(30, 0)
via3_li = layout.layer(49, 0)

print("=== ALL M4 shapes (flat) ===")
ri = pya.RecursiveShapeIterator(layout, top, m4_li)
m4_boxes = []
while not ri.at_end():
    shape = ri.shape()
    trans = ri.trans()
    if shape.is_box():
        b = trans * shape.box
        m4_boxes.append(b)
        print(f"  M4 BOX ({b.left*0.001:.3f}, {b.bottom*0.001:.3f}) to ({b.right*0.001:.3f}, {b.top*0.001:.3f})")
    elif shape.is_polygon():
        b = (trans * shape.polygon).bbox()
        m4_boxes.append(b)
        print(f"  M4 POLY bbox ({b.left*0.001:.3f}, {b.bottom*0.001:.3f}) to ({b.right*0.001:.3f}, {b.top*0.001:.3f})")
    ri.next()

print(f"\n=== ALL Via3 shapes (flat) ===")
ri = pya.RecursiveShapeIterator(layout, top, via3_li)
while not ri.at_end():
    shape = ri.shape()
    trans = ri.trans()
    if shape.is_box():
        b = trans * shape.box
        print(f"  Via3 BOX ({b.left*0.001:.3f}, {b.bottom*0.001:.3f}) to ({b.right*0.001:.3f}, {b.top*0.001:.3f})")
    ri.next()

print(f"\n=== M4 overlap check ===")
for i in range(len(m4_boxes)):
    for j in range(i+1, len(m4_boxes)):
        inter = m4_boxes[i] & m4_boxes[j]
        if not inter.empty():
            print(f"  OVERLAP [{i}] and [{j}]: ({inter.left*0.001:.3f},{inter.bottom*0.001:.3f})-({inter.right*0.001:.3f},{inter.top*0.001:.3f})")
