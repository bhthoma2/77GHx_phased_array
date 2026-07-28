import pya
OUT = "/home/bthomas3/Videos/77GHz_phased_array/layout/"
PDK = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"

ly = pya.Layout()
ly.dbu = 0.001
ly.read(PDK)

import sys
sys.path.insert(0, OUT)
import generate_lna_transistor as gen_lna
import generate_ilfd_transistor as gen_ilfd
gen_lna.main(ly)
gen_ilfd.main(ly)

lna = ly.cell(ly.cell_by_name("RXAMP_77GD"))
ilfd = ly.cell(ly.cell_by_name("ILFD_77GD"))

# Check flat shapes near boundaries
# LNA bottom (y < 50um in cell) and ILFD top (y > 550um in cell)
# After placement: LNA_abs_y = 1100 + cell_y, ILFD_abs_y = 300 + cell_y
# Overlap zone: ILFD top (300+550=850 to 300+622.5=922.5) vs LNA bottom (1100+0=1100 to 1100+50=1150)
# Still 177um gap. Let me check the FULL flat view for overlapping X ranges

print("=== Checking boundary shapes (flattened) ===")
print("LNA placed at (200, 1100), ILFD at (200, 300)")
print()

for cell_name, offset_y, label in [("RXAMP_77GD", 1100, "LNA"), ("ILFD_77GD", 300, "ILFD")]:
    c = ly.cell(ly.cell_by_name(cell_name))
    print(f"{label} (offset_y={offset_y}):")
    for li_idx in range(ly.layers()):
        lp = ly.get_info(li_idx)
        if lp.layer not in [8, 10, 30, 50, 67, 125, 126, 133, 134]:
            continue
        ri = pya.Region()
        for si in c.begin_shapes_rec(li_idx).each():
            if si.shape().is_box() or si.shape().is_polygon() or si.shape().is_path():
                ri.insert(si.shape().polygon.transformed(si.trans()))
        ri.merge()
        if ri.is_empty():
            continue
        bb = ri.bbox()
        abs_bot = bb.bottom/1000.0 + offset_y
        abs_top = bb.top/1000.0 + offset_y
        if label == "LNA" and abs_bot < 1150:
            print(f"  L{lp.layer}/{lp.datatype}: cell_y [{bb.bottom/1000.0:.1f}, {bb.top/1000.0:.1f}] -> abs [{abs_bot:.1f}, {abs_top:.1f}]")
        elif label == "ILFD" and abs_top > 850:
            print(f"  L{lp.layer}/{lp.datatype}: cell_y [{bb.bottom/1000.0:.1f}, {bb.top/1000.0:.1f}] -> abs [{abs_bot:.1f}, {abs_top:.1f}]")