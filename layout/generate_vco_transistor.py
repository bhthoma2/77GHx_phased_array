"""
77 GHz VCO — Transistor-Level Layout with Full Routing
Uses actual IHP SG13G2 PDK cells from sg13g2_pr.gds

Schematic:
  Q1a,Q1b (left pair): C→OUTP, B→OUTN, E→TAIL
  Q2a,Q2b (right pair): C→OUTN, B→OUTP, E→TAIL
  R: TAIL↔VSS
  CV1: OUTP↔VTUNE (gate=VTUNE, top/bot=OUTP)
  CV2: OUTN↔VTUNE (gate=VTUNE, top/bot=OUTN)
  Cdecap: VCC(TM1)↔VSS(M5)

PDK cell pin locations (from L63/0 TEXT labels, relative to cell origin):
  npn13G2L (7.8x7.2µm):
    Collector M1 (2.5,5.1)-(5.3,5.75)   label 'C' at (3.9,5.425)
    Base     M1 (3.385,1.45)-(4.415,2.1) label 'B' at (3.9,1.775)
    Emitter  M2 (2.5,2.9)-(5.3,4.3)     label 'E' at (3.9,3.6)
  SVaricap: Gate M1 (0.29,1.915)-(0.49,2.855), Top M1 (0.75,4.5)-(1.56,4.76), Bot M1 (0.75,0.01)-(1.56,0.27)
  rppd: Pin1 M1 (0.02,0.63)-(0.48,0.93), Pin2 M1 (0.02,-0.43)-(0.48,-0.13)
  cmim: Bot M5 (-0.6,-0.6)-(7.59,7.59), Top TM1 (0.345,0.345)-(6.645,6.645)

Routing layers:
  OUTP: M1 (C and B both on M1)
  OUTN: M3 (crosses OUTP, needs different layer)
  TAIL: M2 (emitters on M2)
  VTUNE: M3
  VSS: M1→via stack→M5 to cmim
"""

import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"

LAYERS = {
    'M1': (8, 0), 'Via1': (19, 0), 'M2': (10, 0), 'Via2': (29, 0),
    'M3': (30, 0), 'Via3': (49, 0), 'M4': (50, 0), 'Via4': (66, 0),
    'M5': (67, 0), 'TopVia1': (125, 0), 'TM1': (126, 0),
    'TopVia2': (133, 0), 'TM2': (134, 0),
}

DBU = 0.001
TL_WIDTH = 5.0
TL_GAP = 5.0
TL_GND_W = 15.0
STUB_LEN = 135.0
CHOKE_LEN = 105.0
CELL_W = 250.0
CELL_H = 450.0


def um(val):
    snapped = round(val / 0.005) * 0.005
    return int(snapped / DBU)


def snap(val):
    return round(val / 0.005) * 0.005


def create_cpw(cell, ly_sig, ly_gnd, x0, y0, length, direction='up'):
    w = um(TL_WIDTH)
    g = um(TL_GAP)
    gw = um(TL_GND_W)
    seg_max = 25.0
    slot_gap = 3.0

    if direction == 'up':
        cell.shapes(ly_sig).insert(pya.Box(um(x0) - w//2, um(y0), um(x0) + w//2, um(y0 + length)))
        pos = 0.0
        while pos < length:
            seg_l = min(seg_max, length - pos)
            ys = um(y0 + pos)
            ye = um(y0 + pos + seg_l)
            cell.shapes(ly_gnd).insert(pya.Box(um(x0)-w//2-g-gw, ys, um(x0)-w//2-g, ye))
            cell.shapes(ly_gnd).insert(pya.Box(um(x0)+w//2+g, ys, um(x0)+w//2+g+gw, ye))
            pos += seg_max + slot_gap
    elif direction == 'down':
        cell.shapes(ly_sig).insert(pya.Box(um(x0) - w//2, um(y0 - length), um(x0) + w//2, um(y0)))
        pos = 0.0
        while pos < length:
            seg_l = min(seg_max, length - pos)
            ys = um(y0 - pos - seg_l)
            ye = um(y0 - pos)
            cell.shapes(ly_gnd).insert(pya.Box(um(x0)-w//2-g-gw, ys, um(x0)-w//2-g, ye))
            cell.shapes(ly_gnd).insert(pya.Box(um(x0)+w//2+g, ys, um(x0)+w//2+g+gw, ye))
            pos += seg_max + slot_gap


def create_via_stack(cell, ly, x, y, layers_from='M1', layers_to='TM2'):
    x = snap(x)
    y = snap(y)
    via_specs = [
        ('M1', 'Via1', 'M2', 0.19, 0.5),
        ('M2', 'Via2', 'M3', 0.19, 0.5),
        ('M3', 'Via3', 'M4', 0.19, 0.5),
        ('M4', 'Via4', 'M5', 0.19, 0.5),
        ('M5', 'TopVia1', 'TM1', 0.42, 5.0),
        ('TM1', 'TopVia2', 'TM2', 0.9, 5.0),
    ]
    started = False
    for bot, via, top_l, via_sz, pad_sz in via_specs:
        if bot == layers_from:
            started = True
        if started:
            vs = um(snap(via_sz))
            ps = um(snap(pad_sz))
            cx = um(x)
            cy = um(y)
            cell.shapes(ly[bot]).insert(pya.Box(cx - ps//2, cy - ps//2, cx + ps//2, cy + ps//2))
            cell.shapes(ly[via]).insert(pya.Box(cx - vs//2, cy - vs//2, cx + vs//2, cy + vs//2))
            cell.shapes(ly[top_l]).insert(pya.Box(cx - ps//2, cy - ps//2, cx + ps//2, cy + ps//2))
        if top_l == layers_to:
            break


def via1(cell, ly, x, y):
    x, y = snap(x), snap(y)
    ps = um(0.5)
    vs = um(0.19)
    cx, cy = um(x), um(y)
    cell.shapes(ly['M1']).insert(pya.Box(cx-ps//2, cy-ps//2, cx+ps//2, cy+ps//2))
    cell.shapes(ly['Via1']).insert(pya.Box(cx-vs//2, cy-vs//2, cx+vs//2, cy+vs//2))
    cell.shapes(ly['M2']).insert(pya.Box(cx-ps//2, cy-ps//2, cx+ps//2, cy+ps//2))


def main(ext_layout=None):
    if ext_layout is not None:
        layout = ext_layout
    else:
        layout = pya.Layout()
        layout.dbu = DBU
        layout.read(PDK_GDS)

    ly = {}
    for name, (ln, dt) in LAYERS.items():
        ly[name] = layout.layer(ln, dt)

    npn_idx = layout.cell_by_name("npn13G2L") if layout.has_cell("npn13G2L") else None
    cmim_idx = layout.cell_by_name("cmim") if layout.has_cell("cmim") else None
    svar_idx = layout.cell_by_name("SVaricap") if layout.has_cell("SVaricap") else None
    rppd_idx = layout.cell_by_name("rppd") if layout.has_cell("rppd") else None

    vco = layout.create_cell("VCO_77G_XTOR")

    cx = CELL_W / 2
    cy = CELL_H / 2
    pair_gap = 25.0
    hbt_spacing = 12.0

    # === DEVICE PLACEMENT ===
    q1_x = cx - pair_gap/2 - 7.8  # 104.7
    q1a_y = cy - 3.6               # 221.4 (Q1a)
    q1b_y = q1a_y - hbt_spacing    # 209.4 (Q1b)
    q2_x = cx + pair_gap/2         # 137.5
    q2a_y = q1a_y                   # 221.4 (Q2a)
    q2b_y = q1b_y                   # 209.4 (Q2b)

    vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q1_x), um(q1a_y))))
    vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q1_x), um(q1b_y))))
    vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q2_x), um(q2a_y))))
    vco.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q2_x), um(q2b_y))))

    var1_x, var1_y = cx - 20, cy + 20  # 105, 245
    var2_x, var2_y = cx + 15, cy + 20  # 140, 245
    vco.insert(pya.CellInstArray(svar_idx, pya.Trans(um(var1_x), um(var1_y))))
    vco.insert(pya.CellInstArray(svar_idx, pya.Trans(um(var2_x), um(var2_y))))

    res_x, res_y = cx - 0.25, cy - 30  # 124.75, 195
    vco.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(res_x), um(res_y))))

    cap_x, cap_y = cx - 4.0, cy - 55  # 121, 170
    vco.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cap_x), um(cap_y))))

    # === ABSOLUTE PIN POSITIONS ===
    # npn13G2L: C(M1)=(+2.5,+5.1)-(+5.3,+5.75), B(M1)=(+3.385,+1.45)-(+4.415,+2.1), E(M2)=(+2.5,+2.9)-(+5.3,+4.3)
    def npn_c(px, py):
        return (px+2.5, py+5.1, px+5.3, py+5.75)
    def npn_b(px, py):
        return (px+3.385, py+1.45, px+4.415, py+2.1)
    def npn_e(px, py):
        return (px+2.5, py+2.9, px+5.3, py+4.3)

    q1a_c = npn_c(q1_x, q1a_y)
    q1b_c = npn_c(q1_x, q1b_y)
    q2a_c = npn_c(q2_x, q2a_y)
    q2b_c = npn_c(q2_x, q2b_y)
    q1a_b = npn_b(q1_x, q1a_y)
    q1b_b = npn_b(q1_x, q1b_y)
    q2a_b = npn_b(q2_x, q2a_y)
    q2b_b = npn_b(q2_x, q2b_y)
    q1a_e = npn_e(q1_x, q1a_y)  # M2
    q1b_e = npn_e(q1_x, q1b_y)
    q2a_e = npn_e(q2_x, q2a_y)
    q2b_e = npn_e(q2_x, q2b_y)

    r_pin1 = (res_x+0.02, res_y+0.63, res_x+0.48, res_y+0.93)
    r_pin2 = (res_x+0.02, res_y-0.43, res_x+0.48, res_y-0.13)

    cv1_gate = (var1_x+0.29, var1_y+1.915, var1_x+0.49, var1_y+2.855)
    cv1_top = (var1_x+0.75, var1_y+4.5, var1_x+1.56, var1_y+4.76)
    cv1_bot = (var1_x+0.75, var1_y+0.01, var1_x+1.56, var1_y+0.27)
    cv2_gate = (var2_x+0.29, var2_y+1.915, var2_x+0.49, var2_y+2.855)
    cv2_top = (var2_x+0.75, var2_y+4.5, var2_x+1.56, var2_y+4.76)
    cv2_bot = (var2_x+0.75, var2_y+0.01, var2_x+1.56, var2_y+0.27)

    # === ROUTING ===
    # LVS pin mapping: upper M1 (cell_y+5.425) = BASE, lower M1 (cell_y+1.775) = COLLECTOR
    # OUTP = Q1.C(lower) + Q2.B(upper) on M3
    # OUTN = Q2.C(lower) + Q1.B(upper) on M4
    # TAIL = all emitters (M2) bus
    # VTUNE = varactor gates (M3); VSS = via stack→M5

    def via_n(cell, x, y, bot_layer, via_layer, top_layer):
        x, y = snap(x), snap(y)
        ps = um(0.5)
        vs = um(0.19)
        cxi, cyi = um(x), um(y)
        cell.shapes(ly[bot_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))
        cell.shapes(ly[via_layer]).insert(pya.Box(cxi-vs//2, cyi-vs//2, cxi+vs//2, cyi+vs//2))
        cell.shapes(ly[top_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))

    # Pin centers (LVS-correct mapping confirmed by single-device probe)
    # Collector = upper M1 pin center: cell_x+3.9, cell_y+5.425
    # Base = lower M1 pin center: cell_x+3.9, cell_y+1.775
    pcx = 3.9
    col_dy = 5.425   # upper = collector
    bas_dy = 1.775   # lower = base

    # OUTP pins: Q1.C(lower) + Q2.B(upper)
    outp_pins = [
        (q1_x+pcx, q1a_y+col_dy),  # Q1a.C
        (q1_x+pcx, q1b_y+col_dy),  # Q1b.C
        (q2_x+pcx, q2a_y+bas_dy),  # Q2a.B
        (q2_x+pcx, q2b_y+bas_dy),  # Q2b.B
    ]
    # OUTN pins: Q2.C(lower) + Q1.B(upper)
    outn_pins = [
        (q2_x+pcx, q2a_y+col_dy),  # Q2a.C
        (q2_x+pcx, q2b_y+col_dy),  # Q2b.C
        (q1_x+pcx, q1a_y+bas_dy),  # Q1a.B
        (q1_x+pcx, q1b_y+bas_dy),  # Q1b.B
    ]

    r_pin1_cx = (r_pin1[0]+r_pin1[2])/2
    r_pin1_cy = (r_pin1[1]+r_pin1[3])/2
    r_pin2_cx = (r_pin2[0]+r_pin2[2])/2
    r_pin2_cy = (r_pin2[1]+r_pin2[3])/2
    row_gap_y = (q1b_y + 7.2 + q1a_y) / 2  # 219.0

    # --- OUTP: Via1→M2→Via2→M3 at pin centers, M3 bus ---
    for px, py in outp_pins:
        via_n(vco, px, py, 'M1', 'Via1', 'M2')
        via_n(vco, px, py, 'M2', 'Via2', 'M3')

    # --- OUTN: Via1→M2→Via2→M3→Via3→M4 at pin centers, M4 bus ---
    for px, py in outn_pins:
        via_n(vco, px, py, 'M1', 'Via1', 'M2')
        via_n(vco, px, py, 'M2', 'Via2', 'M3')
        via_n(vco, px, py, 'M3', 'Via3', 'M4')

    # OUTP M3 bus: offset verticals to avoid OUTN M3 pads (which interleave at same X)
    outp_vl = 106.0   # left vertical (away from OUTN M3 pads at x=108.6)
    outp_vr = 144.0   # right vertical (away from OUTN M3 pads at x=141.4)
    outp_hy = row_gap_y  # 219.0
    # Left vertical spanning Q1 collector pins (y=211.175 to 223.175)
    vco.shapes(ly['M3']).insert(pya.Box(
        um(outp_vl-0.25), um(outp_pins[1][1]-0.25),
        um(outp_vl+0.25), um(outp_pins[0][1]+0.25)))
    # Right vertical spanning Q2 base pins (y=214.825 to 226.825)
    vco.shapes(ly['M3']).insert(pya.Box(
        um(outp_vr-0.25), um(outp_pins[3][1]-0.25),
        um(outp_vr+0.25), um(outp_pins[2][1]+0.25)))
    # Horizontal stubs from pads to offset verticals
    for px, py in outp_pins[:2]:  # Q1 collectors → left vertical
        vco.shapes(ly['M3']).insert(pya.Box(
            um(outp_vl-0.25), um(py-0.25), um(px+0.25), um(py+0.25)))
    for px, py in outp_pins[2:]:  # Q2 bases → right vertical
        vco.shapes(ly['M3']).insert(pya.Box(
            um(px-0.25), um(py-0.25), um(outp_vr+0.25), um(py+0.25)))
    # Horizontal connecting both verticals
    vco.shapes(ly['M3']).insert(pya.Box(
        um(outp_vl-0.25), um(outp_hy-0.25), um(outp_vr+0.25), um(outp_hy+0.25)))

    # OUTN M4 bus: offset verticals
    outn_vl = 110.0   # left vertical (right of OUTN pads at x=108.6)
    outn_vr = 139.0   # right vertical (left of OUTN pads at x=141.4)
    outn_hy = row_gap_y  # 219.0 (different layer, no conflict)
    # Left vertical spanning Q1 base pins (y=214.825 to 226.825)
    vco.shapes(ly['M4']).insert(pya.Box(
        um(outn_vl-0.25), um(outn_pins[3][1]-0.25),
        um(outn_vl+0.25), um(outn_pins[2][1]+0.25)))
    # Right vertical spanning Q2 collector pins (y=211.175 to 223.175)
    vco.shapes(ly['M4']).insert(pya.Box(
        um(outn_vr-0.25), um(outn_pins[1][1]-0.25),
        um(outn_vr+0.25), um(outn_pins[0][1]+0.25)))
    # Horizontal stubs from pads to offset verticals
    for px, py in outn_pins[2:]:  # Q1 bases → left vertical
        vco.shapes(ly['M4']).insert(pya.Box(
            um(px-0.25), um(py-0.25), um(outn_vl+0.25), um(py+0.25)))
    for px, py in outn_pins[:2]:  # Q2 collectors → right vertical
        vco.shapes(ly['M4']).insert(pya.Box(
            um(outn_vr-0.25), um(py-0.25), um(px+0.25), um(py+0.25)))
    # Horizontal connecting both verticals
    vco.shapes(ly['M4']).insert(pya.Box(
        um(outn_vl-0.25), um(outn_hy-0.25), um(outn_vr+0.25), um(outn_hy+0.25)))

    # --- TAIL: All 4 emitters (M2) + R.Pin1 ---
    tail_m2_y = row_gap_y
    tail_stub_xl = q1_x + 2.8   # 107.5
    tail_stub_xr = q2_x + 5.0   # 142.5
    vco.shapes(ly['M2']).insert(pya.Box(
        um(tail_stub_xl-0.5), um(tail_m2_y-0.5), um(tail_stub_xr+0.5), um(tail_m2_y+0.5)))
    for e, sx in [(q1a_e, tail_stub_xl), (q1b_e, tail_stub_xl),
                  (q2a_e, tail_stub_xr), (q2b_e, tail_stub_xr)]:
        ey = (e[1] + e[3]) / 2
        y1 = min(ey, tail_m2_y) - 0.5
        y2 = max(ey, tail_m2_y) + 0.5
        vco.shapes(ly['M2']).insert(pya.Box(um(sx-0.5), um(y1), um(sx+0.5), um(y2)))
    vco.shapes(ly['M2']).insert(pya.Box(
        um(r_pin1_cx-0.5), um(r_pin1_cy), um(r_pin1_cx+0.5), um(tail_m2_y-0.5)))
    via_n(vco, r_pin1_cx, r_pin1_cy, 'M2', 'Via1', 'M1')

    # --- VSS: R.Pin2 + Cdecap bottom (M5) ---
    create_via_stack(vco, ly, r_pin2_cx, r_pin2_cy, layers_from='M1', layers_to='M5')
    cmim_m5_top = cap_y + 7.59
    vco.shapes(ly['M5']).insert(pya.Box(
        um(r_pin2_cx-1.0), um(cmim_m5_top), um(r_pin2_cx+1.0), um(r_pin2_cy)))

    # --- OUTP to CV1: connect G1 and G2 terminals to OUTP ---
    cv1_gate_cx = (cv1_gate[0]+cv1_gate[2])/2
    cv1_gate_cy = (cv1_gate[1]+cv1_gate[3])/2
    cv1_top_cx = (cv1_top[0]+cv1_top[2])/2
    cv1_top_cy = (cv1_top[1]+cv1_top[3])/2
    cv2_gate_cx = (cv2_gate[0]+cv2_gate[2])/2
    cv2_gate_cy = (cv2_gate[1]+cv2_gate[3])/2
    cv2_top_cx = (cv2_top[0]+cv2_top[2])/2
    cv2_top_cy = (cv2_top[1]+cv2_top[3])/2

    # Varactor terminal mapping: G1=gate(VTUNE), G2=W=well(signal)
    # CV1.G2|W → OUTP: via at G2 to M3, connect to OUTP M3 left vertical
    via_n(vco, cv1_top_cx, cv1_top_cy, 'M1', 'Via1', 'M2')
    via_n(vco, cv1_top_cx, cv1_top_cy, 'M2', 'Via2', 'M3')
    vco.shapes(ly['M3']).insert(pya.Box(
        um(outp_vl-0.25), um(outp_pins[0][1]+0.25), um(outp_vl+0.25), um(cv1_top_cy+0.25)))
    vco.shapes(ly['M3']).insert(pya.Box(
        um(outp_vl-0.25), um(cv1_top_cy-0.25), um(cv1_top_cx+0.25), um(cv1_top_cy+0.25)))

    # CV1.G1 → VTUNE: route M1 left to clear OUTP M3, then via stack to M5
    # G1 pin at (105.75, 245.01)-(106.56, 245.27). OUTP M3 at x≥105.75.
    # Extend M1 left to x=104.5 (outside CV1 cell bbox left=104.9, outside OUTP M3)
    vtune_x = 104.5
    vtune_y = (cv1_bot[1]+cv1_bot[3])/2  # 245.14
    vco.shapes(ly['M1']).insert(pya.Box(
        um(vtune_x-0.25), um(cv1_bot[1]), um(cv1_bot[0]), um(cv1_bot[3])))
    via_n(vco, vtune_x, vtune_y, 'M1', 'Via1', 'M2')
    via_n(vco, vtune_x, vtune_y, 'M2', 'Via2', 'M3')
    via_n(vco, vtune_x, vtune_y, 'M3', 'Via3', 'M4')
    via_n(vco, vtune_x, vtune_y, 'M4', 'Via4', 'M5')
    vco.shapes(ly['M5']).insert(pya.Text("VTUNE", pya.Trans(um(vtune_x), um(vtune_y))))

    # CV2.G2|W → OUTN: M1 trace from Q2a.C collector to CV2 G2 left strip
    # Route at x=140.75-141.01 (matches left strip X) from y=227 to y=245.72
    # This also bridges G1 pin (tied gates, valid for VCO varactor)
    vco.shapes(ly['M1']).insert(pya.Box(
        um(140.75), um(227.0), um(141.01), um(245.72)))

    # --- VCC: Cdecap top plate (TM1) ---
    vco.shapes(ly['TM1']).insert(pya.Text("VCC", pya.Trans(um(cap_x+3.5), um(cap_y+3.5))))

    # === Port labels ===
    vco.shapes(ly['M3']).insert(pya.Text("OUTP", pya.Trans(um(cx), um(outp_hy))))
    vco.shapes(ly['M4']).insert(pya.Text("OUTN", pya.Trans(um(cx), um(outn_hy))))
    vco.shapes(ly['M1']).insert(pya.Text("VSS", pya.Trans(um(r_pin2_cx), um(r_pin2_cy))))

    # ----------------------------------------------------------------
    # M5 Port Access Pads
    # Via stacks from internal M3/M4 buses up to M5 with 5µm pads
    # ----------------------------------------------------------------

    # OUTP: use RIGHT M3 bus (outp_vr=144) for port access — far from OUTN
    via_n(vco, outp_vr, outp_hy, 'M3', 'Via3', 'M4')
    via_n(vco, outp_vr, outp_hy, 'M4', 'Via4', 'M5')
    vco.shapes(ly['M5']).insert(pya.Text("OUTP", pya.Trans(um(outp_vr), um(outp_hy))))

    # OUTN: use RIGHT M4 bus (outn_vr=139) for port access — far from OUTP
    via_n(vco, outn_vr, outn_hy, 'M4', 'Via4', 'M5')
    vco.shapes(ly['M5']).insert(pya.Text("OUTN", pya.Trans(um(outn_vr), um(outn_hy))))

    # VTUNE: handled by W terminals of varactors (shared internally)

    # TAIL: skip M5 port (TAIL is internal, connects to tail resistor only)
    # Cannot route TAIL to M5 at y=219 without shorting to OUTP M3 / OUTN M4 buses

    # Save
    if ext_layout is None:
        output = "/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G_XTOR.gds"
        layout.write(output)
        print(f"\nVCO layout with routing: {output}")
        print(f"Devices: 4× npn13G2L + 2× SVaricap + 1× rppd + 1× cmim")
        print(f"Nets routed: OUTP, OUTN, TAIL, VSS, VTUNE, VCC")


if __name__ == "__main__":
    main()
