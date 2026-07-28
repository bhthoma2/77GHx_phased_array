import pya
OUT = "/home/bthomas3/Videos/77GHz_phased_array/layout/"
for f, cell_name, expected_w, expected_h in [
    ("LNA_77G_XTOR.gds", "RXAMP_77GD", 300000, 500000),
    ("ILFD_77G_XTOR.gds", "ILFD_77GD", 300000, 600000),
]:
    ly = pya.Layout()
    ly.read(OUT + f)
    c = ly.cell(cell_name)
    bb = c.bbox()
    print(f"{cell_name}: bbox = ({bb.left},{bb.bottom}) to ({bb.right},{bb.top})")
    print(f"  Expected: (0,0) to ({expected_w},{expected_h})")
    if bb.left < 0 or bb.bottom < 0 or bb.right > expected_w or bb.top > expected_h:
        print(f"  WARNING: shapes extend OUTSIDE cell boundary!")
        overshoot_y = bb.top - expected_h if bb.top > expected_h else 0
        undershoot_y = -bb.bottom if bb.bottom < 0 else 0
        print(f"  Overshoot top: {overshoot_y/1000}um, Undershoot bottom: {undershoot_y/1000}um")