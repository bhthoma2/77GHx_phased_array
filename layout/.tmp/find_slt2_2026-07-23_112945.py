import pya

layout = pya.Layout()
layout.read("/home/bthomas3/Videos/77GHz_phased_array/layout/PHASED_ARRAY_77G_XTOR.gds")
top = [c for c in layout.each_cell() if c.name == "PHASED_ARRAY_77G_XTOR"][0]

li = layout.layer(126, 0)
region = pya.Region()
ri = pya.RecursiveShapeIterator(layout, top, li)
while not ri.at_end():
    p = ri.shape().polygon
    if p is not None:
        region.insert(p.transformed(ri.trans()))
    ri.next()
for p in region.each():
    bb = p.bbox()
    w = bb.width() * 0.001
    h = bb.height() * 0.001
    if w > 30 or h > 30:
        print(f"  TM1 polygon bbox: {w:.1f}x{h:.1f}um at ({bb.left*0.001:.1f},{bb.bottom*0.001:.1f})")
print("Done")
