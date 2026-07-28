import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"
layout = pya.Layout()
layout.read(PDK_GDS)

cell_idx = layout.cell_by_name("SVaricap")
cell = layout.cell(cell_idx)

print(f"SVaricap cell: {cell.name}")
print(f"Bbox: {cell.bbox()}")
print(f"\nLayers with shapes:")
for li in layout.layer_indices():
    info = layout.get_info(li)
    count = cell.shapes(li).size()
    if count > 0:
        print(f"  Layer {info.layer}/{info.datatype}: {count} shapes")
        for shape in cell.shapes(li).each():
            if shape.is_box():
                b = shape.box
                print(f"    BOX ({b.left*0.001:.3f}, {b.bottom*0.001:.3f}) to ({b.right*0.001:.3f}, {b.top*0.001:.3f})")
            elif shape.is_polygon():
                print(f"    POLY area={shape.polygon.area()*1e-6:.3f} um2")
            elif shape.is_path():
                print(f"    PATH")
            elif shape.is_text():
                print(f"    TEXT: {shape.text.string} at ({shape.text.x*0.001:.3f},{shape.text.y*0.001:.3f})")
