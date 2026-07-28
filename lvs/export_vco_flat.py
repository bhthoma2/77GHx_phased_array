import pya

src = pya.Layout()
src.read("/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G_XTOR.gds")

vco_idx = src.cell_by_name("VCO_77G_XTOR")

out = pya.Layout()
out.dbu = src.dbu
out_top = out.create_cell("VCO_77G_XTOR")
out_top.copy_tree(src.cell(vco_idx))

out.write("/home/bthomas3/Videos/77GHz_phased_array/lvs/VCO_77G_XTOR_lvs.gds")
print(f"Exported VCO, top cell: VCO_77G_XTOR, cells: {out.cells()}")