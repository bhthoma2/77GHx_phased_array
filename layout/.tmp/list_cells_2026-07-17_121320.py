import pya
OUT = "/home/bthomas3/Videos/77GHz_phased_array/layout/"
for f in ["LNA_77G_XTOR.gds", "ILFD_77G_XTOR.gds", "MIXER_77G_XTOR.gds"]:
    ly = pya.Layout()
    ly.read(OUT + f)
    cells = sorted([ly.cell(i).name for i in range(ly.cells())])
    print(f"{f}: {cells}")