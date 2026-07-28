import pya
d = "/home/bthomas3/Videos/77GHz_phased_array/layout/"
for f in ["LNA_77G_XTOR.gds", "MIXER_77G_XTOR.gds", "TXPA_77G_XTOR.gds", "ILFD_77G_XTOR.gds"]:
    layout = pya.Layout()
    layout.read(d + f)
    tops = [c.name for c in layout.each_cell() if c.parent_cells() == 0]
    print(f"{f}: top cells = {tops}")
