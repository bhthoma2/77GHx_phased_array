import pya

layout = pya.Layout()
layout.dbu = 0.001
layout.read("/home/bthomas3/Videos/77GHz_phased_array/lvs/IFA_77G_XTOR_lvs.gds")

print("Cells in exported GDS:")
for i in range(layout.cells()):
    c = layout.cell(i)
    print(f"  {c.name} (instances: {c.child_instances()})")

# Check if cmim exists
if layout.has_cell("cmim"):
    cmim = layout.cell(layout.cell_by_name("cmim"))
    print(f"\ncmim cell found, bbox: {cmim.bbox()}")
    # Check MIM layer
    mim_li = layout.layer(36, 0)
    print(f"  MIM shapes: {cmim.shapes(mim_li).size()}")
    m5_li = layout.layer(67, 0)
    print(f"  M5 shapes: {cmim.shapes(m5_li).size()}")
    tm1_li = layout.layer(126, 0)
    print(f"  TM1 shapes: {cmim.shapes(tm1_li).size()}")
else:
    print("\nNO cmim cell found!")

# Check top cell for cmim instances
top = layout.top_cell()
print(f"\nTop cell: {top.name}")
print(f"Child instances: {top.child_instances()}")
for inst in top.each_inst():
    print(f"  Instance of: {inst.cell.name} at {inst.trans}")
