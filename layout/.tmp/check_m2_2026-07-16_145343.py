import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"
layout = pya.Layout()
layout.read(PDK_GDS)

for cell_name in ["npn13G2L", "SVaricap", "rppd"]:
    if not layout.has_cell(cell_name):
        continue
    cell = layout.cell(layout.cell_by_name(cell_name))
    print(f"\n=== {cell_name} ===")
    for li in layout.layer_indices():
        info = layout.get_info(li)
        shapes = cell.shapes(li)
        if shapes.size() == 0:
            continue
        for s in shapes.each():
            if s.is_box():
                b = s.box
                print(f"  L{info.layer}/{info.datatype}: BOX ({b.left*0.001:.3f},{b.bottom*0.001:.3f}) to ({b.right*0.001:.3f},{b.top*0.001:.3f})")
            elif s.is_polygon():
                bb = s.polygon.bbox()
                print(f"  L{info.layer}/{info.datatype}: POLY bbox ({bb.left*0.001:.3f},{bb.bottom*0.001:.3f}) to ({bb.right*0.001:.3f},{bb.top*0.001:.3f})")
            elif s.is_path():
                bb = s.path.bbox()
                print(f"  L{info.layer}/{info.datatype}: PATH bbox ({bb.left*0.001:.3f},{bb.bottom*0.001:.3f}) to ({bb.right*0.001:.3f},{bb.top*0.001:.3f})")
            elif s.is_text():
                print(f"  L{info.layer}/{info.datatype}: TEXT '{s.text.string}' at ({s.text.x*0.001:.3f},{s.text.y*0.001:.3f})")