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

q1_x, q1a_y = 104.7, 221.4
q2_x, q2a_y = 137.5, 221.4
q1b_y, q2b_y = 209.4, 209.4

vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q1_x), um(q1a_y))))
vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q2_x), um(q2a_y))))
vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q1_x), um(q1b_y))))
vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q2_x), um(q2b_y))))

LAYERS = {
    'M1': (8, 0), 'Via1': (19, 0), 'M2': (10, 0), 'Via2': (29, 0),
    'M3': (30, 0), 'Via3': (49, 0), 'M4': (50, 0),
}
ly = {}
for name, (ln, dt) in LAYERS.items():
    ly[name] = layout.layer(ln, dt)

def via_n(cell, x, y, bot_layer, via_layer, top_layer):
    x = round(x / 0.005) * 0.005
    y = round(y / 0.005) * 0.005
    ps = um(0.5)
    vs = um(0.19)
    cxi, cyi = um(x), um(y)
    cell.shapes(ly[bot_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))
    cell.shapes(ly[via_layer]).insert(pya.Box(cxi-vs//2, cyi-vs//2, cxi+vs//2, cyi+vs//2))
    cell.shapes(ly[top_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))

# LVS pin mapping: upper M1 (cell_y+5.425) = BASE, lower M1 (cell_y+1.775) = COLLECTOR
# OUTP = Q1.C(lower) + Q2.B(upper)
outp_pins = [
    (q1_x+3.9, q1a_y+1.775),  # Q1a collector (lower)
    (q1_x+3.9, q1b_y+1.775),  # Q1b collector (lower)
    (q2_x+3.9, q2a_y+5.425),  # Q2a base (upper)
    (q2_x+3.9, q2b_y+5.425),  # Q2b base (upper)
]

# OUTP: Via1->M2->Via2->M3
for px, py in outp_pins:
    via_n(vco, px, py, 'M1', 'Via1', 'M2')
    via_n(vco, px, py, 'M2', 'Via2', 'M3')

# OUTN = Q2.C(lower) + Q1.B(upper)
outn_pins = [
    (q2_x+3.9, q2a_y+1.775),  # Q2a collector (lower)
    (q2_x+3.9, q2b_y+1.775),  # Q2b collector (lower)
    (q1_x+3.9, q1a_y+5.425),  # Q1a base (upper)
    (q1_x+3.9, q1b_y+5.425),  # Q1b base (upper)
]

# OUTN: Via1->M2->Via2->M3->Via3->M4
for px, py in outn_pins:
    via_n(vco, px, py, 'M1', 'Via1', 'M2')
    via_n(vco, px, py, 'M2', 'Via2', 'M3')
    via_n(vco, px, py, 'M3', 'Via3', 'M4')

# OUTP M3 bus: offset verticals at x=106 (left) and x=144 (right)
# avoid OUTN M3 pads at (108.6, 226.825), (108.6, 214.825), (141.4, 223.175), (141.4, 211.175)
outp_vl = 106.0   # left vertical X (away from OUTN pads at x=108.6)
outp_vr = 144.0   # right vertical X (away from OUTN pads at x=141.4)
outp_hy = 219.0   # horizontal connecting both verticals (no pads at this Y)
# Left vertical from lowest to highest OUTP pin at x=108.6
vco.shapes(ly['M3']).insert(pya.Box(
    um(outp_vl-0.25), um(211.175-0.25), um(outp_vl+0.25), um(223.175+0.25)))
# Right vertical from lowest to highest OUTP pin at x=141.4
vco.shapes(ly['M3']).insert(pya.Box(
    um(outp_vr-0.25), um(214.825-0.25), um(outp_vr+0.25), um(226.825+0.25)))
# Horizontal stubs from OUTP pads to offset verticals
vco.shapes(ly['M3']).insert(pya.Box(um(outp_vl-0.25), um(223.175-0.25), um(108.85), um(223.175+0.25)))
vco.shapes(ly['M3']).insert(pya.Box(um(outp_vl-0.25), um(211.175-0.25), um(108.85), um(211.175+0.25)))
vco.shapes(ly['M3']).insert(pya.Box(um(141.15), um(226.825-0.25), um(outp_vr+0.25), um(226.825+0.25)))
vco.shapes(ly['M3']).insert(pya.Box(um(141.15), um(214.825-0.25), um(outp_vr+0.25), um(214.825+0.25)))
# Horizontal at y=219 connecting left and right verticals
vco.shapes(ly['M3']).insert(pya.Box(
    um(outp_vl-0.25), um(outp_hy-0.25), um(outp_vr+0.25), um(outp_hy+0.25)))

# OUTN M4 bus: offset verticals at x=110 and x=139
outn_vl = 110.0   # left vertical (slightly right of OUTN pads at 108.6)
outn_vr = 139.0   # right vertical (slightly left of OUTN pads at 141.4)
outn_hy = 219.0   # horizontal (same Y fine since different layer)
# Left vertical
vco.shapes(ly['M4']).insert(pya.Box(
    um(outn_vl-0.25), um(214.825-0.25), um(outn_vl+0.25), um(226.825+0.25)))
# Right vertical
vco.shapes(ly['M4']).insert(pya.Box(
    um(outn_vr-0.25), um(211.175-0.25), um(outn_vr+0.25), um(223.175+0.25)))
# Horizontal stubs from OUTN M4 pads to offset verticals
vco.shapes(ly['M4']).insert(pya.Box(um(108.35), um(226.825-0.25), um(outn_vl+0.25), um(226.825+0.25)))
vco.shapes(ly['M4']).insert(pya.Box(um(108.35), um(214.825-0.25), um(outn_vl+0.25), um(214.825+0.25)))
vco.shapes(ly['M4']).insert(pya.Box(um(outn_vr-0.25), um(223.175-0.25), um(141.65), um(223.175+0.25)))
vco.shapes(ly['M4']).insert(pya.Box(um(outn_vr-0.25), um(211.175-0.25), um(141.65), um(211.175+0.25)))
# Horizontal connecting both verticals
vco.shapes(ly['M4']).insert(pya.Box(
    um(outn_vl-0.25), um(outn_hy-0.25), um(outn_vr+0.25), um(outn_hy+0.25)))

# --- TAIL: M2 bus connecting all 4 emitters ---
# Emitter M2 center: cell_x+3.9, cell_y+3.6
tail_m2_y = 219.0
tail_xl = q1_x + 2.8   # 107.5
tail_xr = q2_x + 5.0   # 142.5
vco.shapes(ly['M2']).insert(pya.Box(
    um(tail_xl-0.5), um(tail_m2_y-0.5), um(tail_xr+0.5), um(tail_m2_y+0.5)))
for cy, sx in [(q1a_y+3.6, tail_xl), (q1b_y+3.6, tail_xl),
               (q2a_y+3.6, tail_xr), (q2b_y+3.6, tail_xr)]:
    y1 = min(cy, tail_m2_y) - 0.5
    y2 = max(cy, tail_m2_y) + 0.5
    vco.shapes(ly['M2']).insert(pya.Box(um(sx-0.5), um(y1), um(sx+0.5), um(y2)))

output = "/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G_XTOR.gds"
layout.write(output)
print("Written OUTP+OUTN+TAIL test")