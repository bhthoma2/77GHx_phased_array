import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"
layout = pya.Layout()
layout.read(PDK_GDS)

names = [c.name for c in layout.each_cell() if 'npn13' in c.name.lower()]
print(f"NPN cells: {names}")
cell_idx = layout.cell_by_name(names[0])
cell = layout.cell(cell_idx)

print(f"npn13G2l cell bbox: {cell.bbox()}")
print(f"Child cells: {[layout.cell(i).name for i in cell.each_child_cell()]}")
print(f"\nAll metal layers (flat) on M3/M4/Via3:")
ri = pya.RecursiveShapeIterator(layout, cell, [layout.layer(30,0), layout.layer(49,0), layout.layer(50,0)])
count = 0
while not ri.at_end():
    count += 1
    ri.next()
print(f"  Total M3/Via3/M4 shapes (recursive): {count}")
print(f"\nLayers with shapes:")
for li in layout.layer_indices():
    info = layout.get_info(li)
    count = cell.shapes(li).size()
    if count > 0:
        layer_name = f"{info.layer}/{info.datatype}"
        if info.layer in [8, 10, 19, 29, 30, 49, 50, 66, 67]:
            print(f"  Layer {layer_name}: {count} shapes")
            for shape in cell.shapes(li).each():
                if shape.is_box():
                    b = shape.box
                    print(f"    BOX ({b.left*0.001:.3f}, {b.bottom*0.001:.3f}) to ({b.right*0.001:.3f}, {b.top*0.001:.3f})")
                elif shape.is_polygon():
                    p = shape.polygon
                    bb = p.bbox()
                    print(f"    POLY bbox ({bb.left*0.001:.3f}, {bb.bottom*0.001:.3f}) to ({bb.right*0.001:.3f}, {bb.top*0.001:.3f})")
