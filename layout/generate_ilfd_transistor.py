"""
77 GHz ILFD (divide-by-2) — Transistor-Level Layout
Injection-locked frequency divider on IHP SG13G2
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
CELL_W = 300.0
CELL_H = 600.0


def um(val):
    snapped = round(val / 0.005) * 0.005
    return int(snapped / DBU)


def snap(val):
    return round(val / 0.005) * 0.005


def create_cpw(cell, ly_sig, ly_gnd, x0, y0, length, direction='up'):
    seg, gap = 25.0, 3.0
    w, g, gw = TL_WIDTH, TL_GAP, TL_GND_W
    if direction == 'up':
        t = 0.0
        while t < length:
            s = min(seg, length - t)
            cell.shapes(ly_sig).insert(pya.Box(um(x0-w/2), um(y0+t), um(x0+w/2), um(y0+t+s)))
            cell.shapes(ly_gnd).insert(pya.Box(um(x0-w/2-g-gw), um(y0+t), um(x0-w/2-g), um(y0+t+s)))
            cell.shapes(ly_gnd).insert(pya.Box(um(x0+w/2+g), um(y0+t), um(x0+w/2+g+gw), um(y0+t+s)))
            t += seg + gap
    elif direction == 'down':
        t = 0.0
        while t < length:
            s = min(seg, length - t)
            cell.shapes(ly_sig).insert(pya.Box(um(x0-w/2), um(y0-t-s), um(x0+w/2), um(y0-t)))
            cell.shapes(ly_gnd).insert(pya.Box(um(x0-w/2-g-gw), um(y0-t-s), um(x0-w/2-g), um(y0-t)))
            cell.shapes(ly_gnd).insert(pya.Box(um(x0+w/2+g), um(y0-t-s), um(x0+w/2+g+gw), um(y0-t)))
            t += seg + gap
    elif direction == 'right':
        t = 0.0
        while t < length:
            s = min(seg, length - t)
            cell.shapes(ly_sig).insert(pya.Box(um(x0+t), um(y0-w/2), um(x0+t+s), um(y0+w/2)))
            cell.shapes(ly_gnd).insert(pya.Box(um(x0+t), um(y0+w/2+g), um(x0+t+s), um(y0+w/2+g+gw)))
            cell.shapes(ly_gnd).insert(pya.Box(um(x0+t), um(y0-w/2-g-gw), um(x0+t+s), um(y0-w/2-g)))
            t += seg + gap
    elif direction == 'left':
        t = 0.0
        while t < length:
            s = min(seg, length - t)
            cell.shapes(ly_sig).insert(pya.Box(um(x0-t-s), um(y0-w/2), um(x0-t), um(y0+w/2)))
            cell.shapes(ly_gnd).insert(pya.Box(um(x0-t-s), um(y0+w/2+g), um(x0-t), um(y0+w/2+g+gw)))
            cell.shapes(ly_gnd).insert(pya.Box(um(x0-t-s), um(y0-w/2-g-gw), um(x0-t), um(y0-w/2-g)))
            t += seg + gap


def create_via_stack(cell, ly, x, y, layers_from='M1', layers_to='TM2'):
    x = snap(x)
    y = snap(y)
    via_specs = [
        ('M1', 'Via1', 'M2', 0.19, 0.5),
        ('M2', 'Via2', 'M3', 0.19, 0.5),
        ('M3', 'Via3', 'M4', 0.19, 0.5),
        ('M4', 'Via4', 'M5', 0.19, 0.5),
        ('M5', 'TopVia1', 'TM1', 0.42, 1.0),
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
    rppd_idx = layout.cell_by_name("rppd") if layout.has_cell("rppd") else None

    ilfd = layout.create_cell("ILFD_77GD")
    cx = CELL_W / 2
    cy = CELL_H / 2

    # Ground plane (TM1 with slots) - Region-based to cut holes at via stacks
    slot_pitch = 25.0
    slot_w = 7.0
    _pair_gap = 25.0
    _inp_x = cx - _pair_gap/2 - 3.9
    _inn_x = cx + _pair_gap/2 + 3.9
    _res_start_y = cy + 20
    via_stack_positions = [(_inp_x, _res_start_y), (_inn_x, _res_start_y),
                           (cx, cy - 80)]
    hole_sz = 9.0
    seg = slot_pitch - slot_w
    y = 5.0
    while y < CELL_H - 5:
        sh = min(seg, CELL_H - 5 - y)
        if sh > 0:
            x = 5.0
            while x < CELL_W - 5:
                sw = min(seg, CELL_W - 5 - x)
                if sw > 0:
                    skip = False
                    for hx, hy in via_stack_positions:
                        if (x < snap(hx) + hole_sz/2 and x + sw > snap(hx) - hole_sz/2 and
                            y < snap(hy) + hole_sz/2 and y + sh > snap(hy) - hole_sz/2):
                            skip = True
                            break
                    if not skip:
                        ilfd.shapes(ly['TM1']).insert(pya.Box(um(x), um(y), um(x + sw), um(y + sh)))
                x += slot_pitch
        y += slot_pitch


    hbt_spacing = 10.0
    pair_gap = 25.0

    if npn_idx is not None:
        # Cross-coupled oscillator pair (2× Nx=2 = 4 HBTs)
        for i in range(2):
            ilfd.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8), um(cy - 10 + i * hbt_spacing))))
        for i in range(2):
            ilfd.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2), um(cy - 10 + i * hbt_spacing))))

        # Injection pair (2× Nx=2 = 4 HBTs)
        for i in range(2):
            ilfd.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8), um(cy - 40 + i * hbt_spacing))))
        for i in range(2):
            ilfd.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2), um(cy - 40 + i * hbt_spacing))))

    # Tail resistor (100Ω)
    if rppd_idx is not None:
        ilfd.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx - 0.45), um(cy - 70))))

    # === INTRA-BLOCK ROUTING ===
    # ILFD topology:
    #   Q1/Q2 (osc): cross-coupled, Q1.C=OUTP=Q2.B, Q2.C=OUTN=Q1.B
    #   Q3/Q4 (inj): Q3.C+Q4.C=Q1.E+Q2.E (MID), Q3.B=INJ_P, Q4.B=INJ_N
    #   TAIL = Q3.E + Q4.E
    pcx = 3.9
    col_dy = 5.425
    bas_dy = 1.775
    emi_dy = 3.6

    def via_n(cell, x, y, bot_layer, via_layer, top_layer):
        x, y = snap(x), snap(y)
        ps, vs = um(0.5), um(0.19)
        cxi, cyi = um(x), um(y)
        cell.shapes(ly[bot_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))
        cell.shapes(ly[via_layer]).insert(pya.Box(cxi-vs//2, cyi-vs//2, cxi+vs//2, cyi+vs//2))
        cell.shapes(ly[top_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))

    q1_x = cx - pair_gap/2 - 7.8  # 129.7
    q2_x = cx + pair_gap/2         # 162.5
    lx = q1_x + pcx   # 133.6
    rx = q2_x + pcx   # 166.4

    q1_ys = [cy - 10 + i*hbt_spacing for i in range(2)]  # 290, 300 (osc)
    q2_ys = [cy - 10 + i*hbt_spacing for i in range(2)]
    q3_ys = [cy - 40 + i*hbt_spacing for i in range(2)]  # 260, 270 (inj)
    q4_ys = [cy - 40 + i*hbt_spacing for i in range(2)]

    # --- MID (M3): Q1.E + Q2.E + Q3.C + Q4.C ---
    mid_bus_l = q1_x - 4.0  # 125.7
    mid_bus_r = q2_x + 7.8 + 4.0  # 174.3
    mid_hy = (q3_ys[1] + q1_ys[0]) / 2 + emi_dy  # ~283.6 (between inj and osc)
    for qy in q1_ys:
        via_n(ilfd, lx, qy+emi_dy, 'M2', 'Via2', 'M3')
    for qy in q2_ys:
        via_n(ilfd, rx, qy+emi_dy, 'M2', 'Via2', 'M3')
    for qy in q3_ys:
        via_n(ilfd, lx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(ilfd, lx, qy+col_dy, 'M2', 'Via2', 'M3')
    for qy in q4_ys:
        via_n(ilfd, rx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(ilfd, rx, qy+col_dy, 'M2', 'Via2', 'M3')
    # Left M3 bus (Q3.C + Q1.E)
    ilfd.shapes(ly['M3']).insert(pya.Box(
        um(mid_bus_l-0.25), um(q3_ys[0]+col_dy-0.25),
        um(mid_bus_l+0.25), um(q1_ys[1]+emi_dy+0.25)))
    for qy in q3_ys:
        ilfd.shapes(ly['M3']).insert(pya.Box(
            um(mid_bus_l-0.25), um(qy+col_dy-0.25), um(lx+0.25), um(qy+col_dy+0.25)))
    for qy in q1_ys:
        ilfd.shapes(ly['M3']).insert(pya.Box(
            um(mid_bus_l-0.25), um(qy+emi_dy-0.25), um(lx+0.25), um(qy+emi_dy+0.25)))
    # Right M3 bus (Q4.C + Q2.E)
    ilfd.shapes(ly['M3']).insert(pya.Box(
        um(mid_bus_r-0.25), um(q4_ys[0]+col_dy-0.25),
        um(mid_bus_r+0.25), um(q2_ys[1]+emi_dy+0.25)))
    for qy in q4_ys:
        ilfd.shapes(ly['M3']).insert(pya.Box(
            um(rx-0.25), um(qy+col_dy-0.25), um(mid_bus_r+0.25), um(qy+col_dy+0.25)))
    for qy in q2_ys:
        ilfd.shapes(ly['M3']).insert(pya.Box(
            um(rx-0.25), um(qy+emi_dy-0.25), um(mid_bus_r+0.25), um(qy+emi_dy+0.25)))
    # M3 horizontal connecting left and right MID buses
    ilfd.shapes(ly['M3']).insert(pya.Box(
        um(mid_bus_l-0.25), um(mid_hy-0.25), um(mid_bus_r+0.25), um(mid_hy+0.25)))

    # --- OUTP (M4): Q1.C + Q2.B (cross-coupled) ---
    outp_bus_l = mid_bus_l - 3.0  # 122.7
    outp_bus_r = mid_bus_r + 3.0  # 177.3
    outp_hy = q1_ys[1] + col_dy + 3.0  # 308.425 (above osc collectors)
    for qy in q1_ys:
        via_n(ilfd, lx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(ilfd, lx, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(ilfd, lx, qy+col_dy, 'M3', 'Via3', 'M4')
        ilfd.shapes(ly['M4']).insert(pya.Box(
            um(outp_bus_l-0.25), um(qy+col_dy-0.25), um(lx+0.25), um(qy+col_dy+0.25)))
    for qy in q2_ys:
        via_n(ilfd, rx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(ilfd, rx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(ilfd, rx, qy+bas_dy, 'M3', 'Via3', 'M4')
        ilfd.shapes(ly['M4']).insert(pya.Box(
            um(rx-0.25), um(qy+bas_dy-0.25), um(outp_bus_r+0.25), um(qy+bas_dy+0.25)))
    ilfd.shapes(ly['M4']).insert(pya.Box(
        um(outp_bus_l-0.25), um(q1_ys[0]+col_dy-0.25),
        um(outp_bus_l+0.25), um(outp_hy+0.25)))
    ilfd.shapes(ly['M4']).insert(pya.Box(
        um(outp_bus_r-0.25), um(q2_ys[0]+bas_dy-0.25),
        um(outp_bus_r+0.25), um(outp_hy+0.25)))
    ilfd.shapes(ly['M4']).insert(pya.Box(
        um(outp_bus_l-0.25), um(outp_hy-0.25), um(outp_bus_r+0.25), um(outp_hy+0.25)))

    
    # --- OUTN (M5): Q2.C + Q1.B (cross-coupled) ---
    outn_hy = outp_hy - 3.0  # 289.425
    for qy in q2_ys:
        via_n(ilfd, rx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(ilfd, rx, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(ilfd, rx, qy+col_dy, 'M3', 'Via3', 'M4')
        via_n(ilfd, rx, qy+col_dy, 'M4', 'Via4', 'M5')
    for qy in q1_ys:
        via_n(ilfd, lx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(ilfd, lx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(ilfd, lx, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(ilfd, lx, qy+bas_dy, 'M4', 'Via4', 'M5')
    ilfd.shapes(ly['M5']).insert(pya.Box(
        um(lx-0.25), um(q1_ys[0]+bas_dy-0.25), um(lx+0.25), um(q1_ys[1]+bas_dy+0.25)))
    ilfd.shapes(ly['M5']).insert(pya.Box(
        um(rx-0.25), um(q2_ys[0]+col_dy-0.25), um(rx+0.25), um(q2_ys[1]+col_dy+0.25)))
    ilfd.shapes(ly['M5']).insert(pya.Box(
        um(lx-0.25), um(outn_hy-0.25), um(rx+0.25), um(outn_hy+0.25)))
    ilfd.shapes(ly['M5']).insert(pya.Box(
        um(lx-0.25), um(outn_hy-0.25), um(lx+0.25), um(q1_ys[0]+bas_dy+0.25)))
    ilfd.shapes(ly['M5']).insert(pya.Box(
        um(rx-0.25), um(outn_hy-0.25), um(rx+0.25), um(q2_ys[0]+col_dy+0.25)))

    # --- INJ_P (M4): Q3.B ---
    injp_bus_x = mid_bus_l  # 125.7
    for qy in q3_ys:
        via_n(ilfd, lx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(ilfd, lx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(ilfd, lx, qy+bas_dy, 'M3', 'Via3', 'M4')
        ilfd.shapes(ly['M4']).insert(pya.Box(
            um(injp_bus_x-0.25), um(qy+bas_dy-0.25), um(lx+0.25), um(qy+bas_dy+0.25)))
    ilfd.shapes(ly['M4']).insert(pya.Box(
        um(injp_bus_x-0.25), um(q3_ys[0]+bas_dy-0.25),
        um(injp_bus_x+0.25), um(q3_ys[1]+bas_dy+0.25)))

    # --- INJ_N (M4): Q4.B ---
    injn_bus_x = mid_bus_r  # 174.3
    for qy in q4_ys:
        via_n(ilfd, rx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(ilfd, rx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(ilfd, rx, qy+bas_dy, 'M3', 'Via3', 'M4')
        ilfd.shapes(ly['M4']).insert(pya.Box(
            um(rx-0.25), um(qy+bas_dy-0.25), um(injn_bus_x+0.25), um(qy+bas_dy+0.25)))
    ilfd.shapes(ly['M4']).insert(pya.Box(
        um(injn_bus_x-0.25), um(q4_ys[0]+bas_dy-0.25),
        um(injn_bus_x+0.25), um(q4_ys[1]+bas_dy+0.25)))

    # --- TAIL (M4): Q3.E + Q4.E ---
    tail_vl = lx + 3.0   # 136.6
    tail_vr = rx - 3.0   # 163.4
    tail_hy = q3_ys[0] + emi_dy - 3.0  # 260.6
    for qy in q3_ys:
        via_n(ilfd, lx, qy+emi_dy, 'M2', 'Via2', 'M3')
        via_n(ilfd, lx, qy+emi_dy, 'M3', 'Via3', 'M4')
        ilfd.shapes(ly['M4']).insert(pya.Box(
            um(lx-0.25), um(qy+emi_dy-0.25), um(tail_vl+0.25), um(qy+emi_dy+0.25)))
    for qy in q4_ys:
        via_n(ilfd, rx, qy+emi_dy, 'M2', 'Via2', 'M3')
        via_n(ilfd, rx, qy+emi_dy, 'M3', 'Via3', 'M4')
        ilfd.shapes(ly['M4']).insert(pya.Box(
            um(tail_vr-0.25), um(qy+emi_dy-0.25), um(rx+0.25), um(qy+emi_dy+0.25)))
    ilfd.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl-0.25), um(tail_hy-0.25), um(tail_vl+0.25), um(q3_ys[1]+emi_dy+0.25)))
    ilfd.shapes(ly['M4']).insert(pya.Box(
        um(tail_vr-0.25), um(tail_hy-0.25), um(tail_vr+0.25), um(q4_ys[1]+emi_dy+0.25)))
    ilfd.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl-0.25), um(tail_hy-0.25), um(tail_vr+0.25), um(tail_hy+0.25)))

    print("Nets routed: MID, OUTP, OUTN, INJ_P, INJ_N, TAIL")

    # ----------------------------------------------------------------
    # M5 Port Access Pads
    # Via stacks from internal M3/M4 buses up to M5 with 5µm pads
    # ----------------------------------------------------------------

    # VCC: 3 taps along M3 VCC rail at y=600 (x=60, 150, 240)
    vcc_rail_y = cy + 300.0   # 600.0
    for vcc_tap_x in [60.0, 150.0, 240.0]:
        via_n(ilfd, vcc_tap_x, vcc_rail_y, 'M3', 'Via3', 'M4')
        via_n(ilfd, vcc_tap_x, vcc_rail_y, 'M4', 'Via4', 'M5')
        ilfd.shapes(ly['M5']).insert(pya.Box(
            um(vcc_tap_x - 2.5), um(vcc_rail_y - 2.5),
            um(vcc_tap_x + 2.5), um(vcc_rail_y + 2.5)))
    ilfd.shapes(ly['M5']).insert(pya.Text("ILFD_VCC", pya.Trans(um(150.0), um(vcc_rail_y))))

    # TAIL: tap at (cx=150, tail_hy=260.6) on M4 bus → M5
    # Short M4 stub from tail_vl to cx
    ilfd.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl - 0.25), um(tail_hy - 0.25),
        um(150.0 + 0.25), um(tail_hy + 0.25)))
    via_n(ilfd, 150.0, tail_hy, 'M4', 'Via4', 'M5')
    ilfd.shapes(ly['M5']).insert(pya.Box(
        um(150.0 - 2.5), um(tail_hy - 2.5),
        um(150.0 + 2.5), um(tail_hy + 2.5)))
    ilfd.shapes(ly['M5']).insert(pya.Text("ILFD_TAIL", pya.Trans(um(150.0), um(tail_hy))))

    # INJ_P: tap at (injp_bus_x=125.7, 266) on M4 bus → M5
    via_n(ilfd, injp_bus_x, 266.0, 'M4', 'Via4', 'M5')
    ilfd.shapes(ly['M5']).insert(pya.Box(
        um(injp_bus_x - 2.5), um(266.0 - 2.5),
        um(injp_bus_x + 2.5), um(266.0 + 2.5)))
    ilfd.shapes(ly['M5']).insert(pya.Text("ILFD_INJ_P", pya.Trans(um(injp_bus_x), um(266.0))))

    # INJ_N: tap at (injn_bus_x=174.3, 266) on M4 bus → M5
    via_n(ilfd, injn_bus_x, 266.0, 'M4', 'Via4', 'M5')
    ilfd.shapes(ly['M5']).insert(pya.Box(
        um(injn_bus_x - 2.5), um(266.0 - 2.5),
        um(injn_bus_x + 2.5), um(266.0 + 2.5)))
    ilfd.shapes(ly['M5']).insert(pya.Text("ILFD_INJ_N", pya.Trans(um(injn_bus_x), um(266.0))))

    # OUTP: tap at (cx=150, outp_hy=308.425) on M4 bus → M5
    via_n(ilfd, 150.0, outp_hy, 'M4', 'Via4', 'M5')
    ilfd.shapes(ly['M5']).insert(pya.Box(
        um(150.0 - 2.5), um(outp_hy - 2.5),
        um(150.0 + 2.5), um(outp_hy + 2.5)))
    ilfd.shapes(ly['M5']).insert(pya.Text("ILFD_OUTP", pya.Trans(um(150.0), um(outp_hy))))

    # OUTN: already on M5 bus (outn_hy=289.425) — no extra pad needed
    # The M5 bus itself serves as the port connection point
    ilfd.shapes(ly['M5']).insert(pya.Text("ILFD_OUTN", pya.Trans(um(150.0), um(outn_hy))))
    # CPW TLs
    inp_x = cx - pair_gap/2 - 3.9
    inn_x = cx + pair_gap/2 + 3.9

    # TL_resonator: 850µm folded as U-shape (up 280, right 290, down 280)
    res_start_y = cy + 20
    create_cpw(ilfd, ly['TM2'], ly['TM2'], inp_x, res_start_y, 280.0, 'up')
    create_cpw(ilfd, ly['TM2'], ly['TM2'], inp_x, res_start_y + 280.0, 290.0, 'right')
    create_cpw(ilfd, ly['TM2'], ly['TM2'], inn_x, res_start_y, 280.0, 'up')

    # TL_choke: 250µm (down from emitters)
    create_cpw(ilfd, ly['TM2'], ly['TM2'], cx, cy - 80, 250.0, 'down')

    # Via stacks
    create_via_stack(ilfd, ly, inp_x, res_start_y)
    create_via_stack(ilfd, ly, inn_x, res_start_y)
    create_via_stack(ilfd, ly, cx, cy - 80)

    # VCC rail
    ilfd.shapes(ly['M3']).insert(pya.Box(um(10), um(cy + 295), um(CELL_W - 10), um(cy + 305)))

    # Port labels
    ilfd.shapes(ly['TM2']).insert(pya.Text("ILFD_INJ_P", pya.Trans(um(inp_x), um(cy - 335))))
    ilfd.shapes(ly['TM2']).insert(pya.Text("ILFD_INJ_N", pya.Trans(um(inn_x), um(cy - 335))))
    ilfd.shapes(ly['TM2']).insert(pya.Text("ILFD_OUTP", pya.Trans(um(inp_x), um(res_start_y + 285))))
    ilfd.shapes(ly['TM2']).insert(pya.Text("ILFD_OUTN", pya.Trans(um(inn_x), um(res_start_y + 285))))
    ilfd.shapes(ly['M3']).insert(pya.Text("ILFD_VCC", pya.Trans(um(cx), um(cy + 300))))

    if ext_layout is None:
        output = "/home/bthomas3/Videos/77GHz_phased_array/layout/ILFD_77G_XTOR.gds"
        layout.write(output)
        print(f"\nILFD layout: {output}")
        print(f"Cell size: {CELL_W} x {CELL_H} um")
        print(f"Devices: 8x npn13G2L + 1x rppd")


if __name__ == "__main__":
    main()
