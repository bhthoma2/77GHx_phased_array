import pya

layout = pya.Layout()
layout.read("/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G_XTOR.gds")

top = [c for c in layout.each_cell() if c.name == "VCO_77G_XTOR"][0]

# Region around Q2a: x=135-145, y=219-230
region_x = (135000, 145000)
region_y = (219000, 230000)

for layer_num, layer_name in [(8, "M1"), (19, "Via1"), (10, "M2"), (29, "Via2"), (30, "M3")]:
    li = layout.layer(layer_num, 0)
    print(f"\n=== {layer_name} (layer {layer_num}/0) in Q2a region ===")
    ri = pya.RecursiveShapeIterator(layout, top, li)
    while not ri.at_end():
        shape = ri.shape()
        trans = ri.trans()
        if shape.is_box():
            b = trans * shape.box
            if b.right > region_x[0] and b.left < region_x[1] and b.top > region_y[0] and b.bottom < region_y[1]:
                print(f"  ({b.left*0.001:.3f}, {b.bottom*0.001:.3f}) to ({b.right*0.001:.3f}, {b.top*0.001:.3f})")
        ri.next()
