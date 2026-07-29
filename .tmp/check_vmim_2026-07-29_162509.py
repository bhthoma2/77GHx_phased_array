import pya
layout = pya.Layout()
layout.dbu = 0.001
layout.read("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds")
cmim = layout.cell(layout.cell_by_name("cmim"))
# Check ALL layers in cmim cell
for li in range(layout.layers()):
    if cmim.shapes(li).size() > 0:
        info = layout.get_info(li)
        print(f"Layer ({info.layer},{info.datatype}): {cmim.shapes(li).size()} shapes")
        for s in cmim.shapes(li).each():
            if s.is_box():
                b = s.box
                print(f"  ({b.left*0.001:.3f},{b.bottom*0.001:.3f})-({b.right*0.001:.3f},{b.top*0.001:.3f})")
