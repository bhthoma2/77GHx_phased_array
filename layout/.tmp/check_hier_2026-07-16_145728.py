import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"
layout = pya.Layout()
layout.read(PDK_GDS)

cell = layout.cell(layout.cell_by_name("npn13G2L"))
print(f"npn13G2L child cells: {cell.child_cells()}")
for ci in cell.each_inst():
    child = ci.cell
    print(f"  child: {child.name} at ({ci.trans.disp.x*0.001:.3f},{ci.trans.disp.y*0.001:.3f})")
    for li in layout.layer_indices():
        info = layout.get_info(li)
        if info.layer in [8, 10, 19, 29, 30, 49, 50, 66, 67] and child.shapes(li).size() > 0:
            for s in child.shapes(li).each():
                if s.is_box():
                    b = s.box
                    print(f"    L{info.layer}/{info.datatype}: BOX ({b.left*0.001:.3f},{b.bottom*0.001:.3f}) to ({b.right*0.001:.3f},{b.top*0.001:.3f})")

print("\n\nSVaricap child cells:")
cell2 = layout.cell(layout.cell_by_name("SVaricap"))
print(f"  child_cells count: {cell2.child_cells()}")
for ci in cell2.each_inst():
    child = ci.cell
    print(f"  child: {child.name} at ({ci.trans.disp.x*0.001:.3f},{ci.trans.disp.y*0.001:.3f})")
