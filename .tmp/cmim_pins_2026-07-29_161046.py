import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"
layout = pya.Layout()
layout.dbu = 0.001
layout.read(PDK_GDS)

cmim_idx = layout.cell_by_name("cmim")
cmim = layout.cell(cmim_idx)

print(f"cmim cell bbox: {cmim.bbox()}")
print(f"cmim cell bbox in um: {cmim.bbox().left*0.001:.3f}, {cmim.bbox().bottom*0.001:.3f} to {cmim.bbox().right*0.001:.3f}, {cmim.bbox().top*0.001:.3f}")
print()

# Check all layers for shapes
layer_map = {
    'M1': (8,0), 'M2': (10,0), 'M3': (30,0), 'M4': (50,0),
    'M5': (67,0), 'TM1': (126,0), 'TM2': (134,0),
    'Via1': (19,0), 'Via2': (29,0), 'Via3': (49,0), 'Via4': (66,0),
    'TopVia1': (125,0), 'TopVia2': (133,0),
    'MIM': (36,0), 'M5_pin': (67,2), 'TM1_pin': (126,2),
    'M5_label': (67,25), 'TM1_label': (126,25),
}

for name, (ln, dt) in sorted(layer_map.items()):
    li = layout.layer(ln, dt)
    shapes = cmim.shapes(li)
    if shapes.size() > 0:
        print(f"{name} ({ln},{dt}): {shapes.size()} shapes")
        for s in shapes.each():
            if s.is_box():
                b = s.box
                print(f"  Box: ({b.left*0.001:.3f}, {b.bottom*0.001:.3f}) to ({b.right*0.001:.3f}, {b.top*0.001:.3f})")
            elif s.is_text():
                print(f"  Text: '{s.text.string}' at ({s.text.x*0.001:.3f}, {s.text.y*0.001:.3f})")
            elif s.is_polygon():
                bb = s.polygon.bbox()
                print(f"  Poly: ({bb.left*0.001:.3f}, {bb.bottom*0.001:.3f}) to ({bb.right*0.001:.3f}, {bb.top*0.001:.3f})")
