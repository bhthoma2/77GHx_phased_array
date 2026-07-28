import pya

layout = pya.Layout()
layout.read("/home/bthomas3/Videos/77GHz_phased_array/layout/PHASED_ARRAY_77G_XTOR.gds")
top = [c for c in layout.each_cell() if c.name == "PHASED_ARRAY_77G_XTOR"][0]

li = layout.layer(126, 0)
search = pya.Box(1100000, 370000, 1425000, 970000)
ri = pya.RecursiveShapeIterator(layout, top, li, pya.Region(search))
sizes = {}
while not ri.at_end():
    shape = ri.shape()
    trans = ri.trans()
    if shape.is_box():
        b = trans * shape.box
        w = round(b.width() * 0.001, 1)
        h = round(b.height() * 0.001, 1)
        key = f"{w}x{h}"
        sizes[key] = sizes.get(key, 0) + 1
    elif shape.is_polygon():
        p = shape.polygon
        bb = p.bbox()
        w = round(bb.width() * 0.001, 1)
        h = round(bb.height() * 0.001, 1)
        print(f"  POLYGON {w}x{h}um cell={ri.cell().name}")
    ri.next()
for k, v in sorted(sizes.items(), key=lambda x: -x[1]):
    print(f"  Box {k}: {v} instances")
