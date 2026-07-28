import pya

layout = pya.Layout()
layout.read("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds")

cell = layout.cell_by_name("rppd")
c = layout.cell(cell)
for li in layout.layer_indices():
    info = layout.get_info(li)
    shapes = c.shapes(li)
    if shapes.size() > 0:
        print(f"  Layer ({info.layer},{info.datatype}): {shapes.size()} shapes")
        for s in shapes.each():
            print(f"    {s.to_s()}")
