import pya
PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"
ly = pya.Layout()
ly.read(PDK_GDS)
for name in ["npn13G2L", "cmim", "rppd"]:
    if ly.has_cell(name):
        c = ly.cell(ly.cell_by_name(name))
        bb = c.bbox()
        print(f"{name}: bbox ({bb.left/1000:.1f}, {bb.bottom/1000:.1f}) to ({bb.right/1000:.1f}, {bb.top/1000:.1f}) um")
        print(f"  Size: {(bb.right-bb.left)/1000:.1f} x {(bb.top-bb.bottom)/1000:.1f} um")
        for li in range(ly.layers()):
            si = c.shapes(li)
            if not si.is_empty():
                lp = ly.get_info(li)
                sbb = pya.Region(si).bbox()
                print(f"  Layer {lp.layer}/{lp.datatype}: ({sbb.left/1000:.1f},{sbb.bottom/1000:.1f}) to ({sbb.right/1000:.1f},{sbb.top/1000:.1f})")