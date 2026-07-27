import pya
layout = pya.Layout()
layout.read("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds")
for ci in range(layout.cells()):
    cell = layout.cell(ci)
    bb = cell.bbox()
    if "cap" in cell.name.lower() or "mim" in cell.name.lower():
        print(f"{cell.name}: {bb.width()*layout.dbu:.2f} x {bb.height()*layout.dbu:.2f} µm")
