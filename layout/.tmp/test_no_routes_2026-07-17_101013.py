import pya

layout = pya.Layout()
layout.dbu = 0.001

top = layout.create_cell("TEST_TOP")

gds_path = '/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G_XTOR.gds'
layout.read(gds_path)
vco_cell = layout.cell("VCO_77G_XTOR")
px, py = 900, 1125
top.insert(pya.CellInstArray(vco_cell.cell_index(), pya.Trans(int(px/layout.dbu), int(py/layout.dbu))))

layout.write("/home/bthomas3/Videos/77GHz_phased_array/layout/.tmp/test_no_routes.gds")
print("Done")
