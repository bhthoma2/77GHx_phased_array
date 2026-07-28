import pya

layout = pya.Layout()
layout.dbu = 0.001

top = layout.create_cell("ISO_TEST")

gds_files = [
    ('VCO_77G_XTOR.gds', 'VCO_77G_XTOR', 900, 1125),
    ('LNA_77G_XTOR.gds', 'RXAMP_77GD', 200, 1100),
    ('MIXER_77G_XTOR.gds', 'MIXER_77GD', 550, 1125),
    ('TXPA_77G_XTOR.gds', 'TXAMP_77GD', 900, 300),
    ('ILFD_77G_XTOR.gds', 'ILFD_77GD', 200, 300),
]

base = "/home/bthomas3/Videos/77GHz_phased_array/layout/"
for fname, cellname, px, py in gds_files:
    layout.read(base + fname)
    cell = layout.cell(cellname)
    top.insert(pya.CellInstArray(cell.cell_index(),
        pya.Trans(int(px / layout.dbu), int(py / layout.dbu))))

layout.write(base + ".tmp/iso_test.gds")
print("Done - no routing, no mesh, blocks only")
