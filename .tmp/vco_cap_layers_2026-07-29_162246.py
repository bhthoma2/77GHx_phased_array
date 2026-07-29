import pya

layout = pya.Layout()
layout.dbu = 0.001
layout.read("/home/bthomas3/Videos/77GHz_phased_array/lvs/VCO_77G_XTOR_lvs.gds")

# Flatten to see all shapes
top = layout.top_cell()
top.flatten(True)

cap_x, cap_y = 121.0, 170.0
cap_box = pya.DBox(cap_x-1, cap_y-1, cap_x+9, cap_y+9)

print("Layers with shapes in VCO cap area:")
layer_names = {(8,0):'M1',(10,0):'M2',(19,0):'Via1',(29,0):'Via2',
    (30,0):'M3',(36,0):'MIM',(49,0):'Via3',(50,0):'M4',(66,0):'Via4',
    (67,0):'M5',(67,25):'M5_txt',(125,0):'TopVia1',(126,0):'TM1',
    (126,25):'TM1_txt',(133,0):'TopVia2',(134,0):'TM2',
    (35,0):'VMIM'}

for (ln,dt), name in sorted(layer_names.items()):
    li = layout.layer(ln, dt)
    count = 0
    for s in top.shapes(li).each_overlapping(pya.DBox(cap_x-1, cap_y-1, cap_x+9, cap_y+9)):
        count += 1
    if count > 0:
        print(f"  {name} ({ln},{dt}): {count} shapes")
