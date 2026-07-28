import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"
DBU = 0.001

def um(val):
    return int(round(val / 0.005) * 0.005 / DBU)

layout = pya.Layout()
layout.dbu = DBU
layout.read(PDK_GDS)

npn_idx = layout.cell_by_name("npn13G2L")
vco = layout.create_cell("VCO_77G_XTOR")

# Place just 2 BJTs (Q1a and Q2a) with NO routing
q1_x, q1a_y = 104.7, 221.4
q2_x, q2a_y = 137.5, 221.4

vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q1_x), um(q1a_y))))
vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q2_x), um(q2a_y))))

LAYERS = {
    'M1': (8, 0), 'Via1': (19, 0), 'M2': (10, 0), 'Via2': (29, 0),
    'M3': (30, 0), 'Via3': (49, 0), 'M4': (50, 0), 'Via4': (66, 0),
    'M5': (67, 0), 'TopVia1': (125, 0), 'TM1': (126, 0),
}
ly = {}
for name, (ln, dt) in LAYERS.items():
    ly[name] = layout.layer(ln, dt)

def snap(val):
    return round(val / 0.005) * 0.005

def via_n(cell, x, y, bot_layer, via_layer, top_layer):
    x, y = snap(x), snap(y)
    ps = um(0.5)
    vs = um(0.19)
    cxi, cyi = um(x), um(y)
    cell.shapes(ly[bot_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))
    cell.shapes(ly[via_layer]).insert(pya.Box(cxi-vs//2, cyi-vs//2, cxi+vs//2, cyi+vs//2))
    cell.shapes(ly[top_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))

# Q1a pin centers
q1a_c_cx, q1a_c_cy = q1_x + 3.9, q1a_y + 5.425
q1a_e_cx, q1a_e_cy = q1_x + 3.9, q1a_y + 1.775

# 4 BJTs + OUTP M1 only (Q1.C + Q2.B)
q1b_y = q1a_y - 12.0
q2b_y = q2a_y - 12.0
vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q1_x), um(q1b_y))))
vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q2_x), um(q2b_y))))

ly_m1 = layout.layer(8, 0)

# HUGE M1 box covering entire base Y range for BOTH Q1a and Q2a
# Q1a base: (108.085,222.85)-(109.115,223.5)
# Q2a base: (140.885,222.85)-(141.915,223.5)
# One giant box from x=107 to x=143, y=222.5 to y=224
vco.shapes(ly_m1).insert(pya.Box(um(107.0), um(222.5), um(143.0), um(224.0)))

output = "/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G_XTOR.gds"
layout.write(output)
print("Written 4-BJT + OUTP M1 only")
