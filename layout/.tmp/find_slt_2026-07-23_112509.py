import pya

layout = pya.Layout()
layout.read("/home/bthomas3/Videos/77GHz_phased_array/layout/PHASED_ARRAY_77G_XTOR.gds")
top = [c for c in layout.each_cell() if c.name == "PHASED_ARRAY_77G_XTOR"][0]

for lname, lnum in [("TM1", 126), ("TM2", 134)]:
    li = layout.layer(lnum, 0)
    print(f"\n=== {lname} shapes > 30µm in any dimension ===")
    ri = pya.RecursiveShapeIterator(layout, top, li)
    count = 0
    while not ri.at_end():
        shape = ri.shape()
        trans = ri.trans()
        if shape.is_box():
            b = trans * shape.box
            w = b.width() * 0.001
            h = b.height() * 0.001
            if w > 30 or h > 30:
                count += 1
                if count <= 5:
                    print(f"  {w:.1f}×{h:.1f}µm at ({b.left*0.001:.1f},{b.bottom*0.001:.1f}) cell={ri.cell().name}")
        ri.next()
    print(f"  Total: {count} shapes > 30µm")
