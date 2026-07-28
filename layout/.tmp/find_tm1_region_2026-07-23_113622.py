import pya

layout = pya.Layout()
layout.read("/home/bthomas3/Videos/77GHz_phased_array/layout/PHASED_ARRAY_77G_XTOR.gds")
top = [c for c in layout.each_cell() if c.name == "PHASED_ARRAY_77G_XTOR"][0]

li = layout.layer(126, 0)
search = pya.Box(1125000, 455000, 1190000, 696000)
ri = pya.RecursiveShapeIterator(layout, top, li, pya.Region(search))
count = 0
while not ri.at_end():
    shape = ri.shape()
    trans = ri.trans()
    if shape.is_box():
        b = trans * shape.box
        w = b.width() * 0.001
        h = b.height() * 0.001
        count += 1
        if count <= 20:
            print(f"  {w:.2f}x{h:.2f}um at ({b.left*0.001:.2f},{b.bottom*0.001:.2f}) cell={ri.cell().name}")
    ri.next()
print(f"Total TM1 shapes in region: {count}")
