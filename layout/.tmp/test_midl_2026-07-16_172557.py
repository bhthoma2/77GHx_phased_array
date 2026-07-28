import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"
DBU = 0.001

def um(val):
    return int(round(val / 0.005) * 0.005 / DBU)

def snap(val):
    return round(val / 0.005) * 0.005

layout = pya.Layout()
layout.dbu = DBU
layout.read(PDK_GDS)

npn_idx = layout.cell_by_name("npn13G2L")
cell = layout.create_cell("RXAMP_77GD")

LAYERS = {
    'M1': (8, 0), 'Via1': (19, 0), 'M2': (10, 0), 'Via2': (29, 0), 'M3': (30, 0),
}
ly = {}
for name, (ln, dt) in LAYERS.items():
    ly[name] = layout.layer(ln, dt)

def via_n(c, x, y, bot, via, top):
    x, y = snap(x), snap(y)
    ps, vs = um(0.5), um(0.19)
    cx, cy = um(x), um(y)
    c.shapes(ly[bot]).insert(pya.Box(cx-ps//2, cy-ps//2, cx+ps//2, cy+ps//2))
    c.shapes(ly[via]).insert(pya.Box(cx-vs//2, cy-vs//2, cx+vs//2, cy+vs//2))
    c.shapes(ly[top]).insert(pya.Box(cx-ps//2, cy-ps//2, cx+ps//2, cy+ps//2))

# Place 1 device and probe all 3 pins with separate M3 nets
q1_x = 127.2
cell.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q1_x), um(230.0))))

pcx = 3.9
lx = q1_x + pcx  # 131.1

# Pin A: lower M1 (y+1.775) → M3 at x=120
via_n(cell, lx, 231.775, 'M1', 'Via1', 'M2')
via_n(cell, lx, 231.775, 'M2', 'Via2', 'M3')
cell.shapes(ly['M3']).insert(pya.Box(um(119.75), um(231.525), um(131.35), um(232.025)))
cell.shapes(ly['M3']).insert(pya.Text("PIN_LOWER", pya.Trans(um(120), um(231.775))))

# Pin B: M2 emitter (y+3.6) → M3 at x=135
via_n(cell, lx, 233.6, 'M2', 'Via2', 'M3')
cell.shapes(ly['M3']).insert(pya.Box(um(131.35), um(233.35), um(136.0), um(233.85)))
cell.shapes(ly['M3']).insert(pya.Text("PIN_EMI", pya.Trans(um(135), um(233.6))))

# Pin C: upper M1 (y+5.425) → M3 at x=140
via_n(cell, lx, 235.425, 'M1', 'Via1', 'M2')
via_n(cell, lx, 235.425, 'M2', 'Via2', 'M3')
cell.shapes(ly['M3']).insert(pya.Box(um(131.35), um(235.175), um(141.0), um(235.675)))
cell.shapes(ly['M3']).insert(pya.Text("PIN_UPPER", pya.Trans(um(140), um(235.425))))

# Connect PIN_LOWER and PIN_EMI on M3 to identify which terminals merge
cell.shapes(ly['M3']).insert(pya.Box(um(119.75), um(231.525), um(136.0), um(233.85)))

layout.write("/home/bthomas3/Videos/77GHz_phased_array/layout/LNA_77G_XTOR.gds")
print("Written MIDL-only test (4 BJTs)")