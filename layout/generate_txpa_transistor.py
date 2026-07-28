"""
77 GHz TX PA (TXAMP_77GD) — Transistor-Level Layout
Differential cascode with larger devices for power on IHP SG13G2
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
CELL_W = 350.0
CELL_H = 550.0


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

    pa = layout.create_cell("TXAMP_77GD")
    cx = CELL_W / 2
    cy = CELL_H / 2

    # Ground plane (TM1 with slots) - Region-based to cut holes at via stacks
    slot_pitch = 25.0
    slot_w = 4.0
    _inp_x = cx - 17.5 - 3.9   # pair_gap=35.0
    _inn_x = cx + 17.5 + 3.9
    via_stack_positions = [(_inp_x, cy - 120), (_inn_x, cy - 120),
                           (_inp_x, cy + 120), (_inn_x, cy + 120)]
    hole_sz = 9.0
    y = 5.0
    while y < CELL_H - 5:
        sh = min(slot_pitch - slot_w, CELL_H - 5 - y)
        if sh > 0:
            x = 5.0
            while x < CELL_W - 5:
                sw = min(slot_pitch - slot_w, CELL_W - 5 - x)
                if sw > 0:
                    skip = False
                    for hx, hy in via_stack_positions:
                        if (x < snap(hx) + hole_sz/2 and x + sw > snap(hx) - hole_sz/2 and
                            y < snap(hy) + hole_sz/2 and y + sh > snap(hy) - hole_sz/2):
                            skip = True
                            break
                    if not skip:
                        pa.shapes(ly['TM1']).insert(pya.Box(um(x), um(y), um(x + sw), um(y + sh)))
                x += slot_pitch
        y += slot_pitch

    # HBTs: 4× Nx=8 = 32 instances total (differential cascode)
    hbt_spacing = 10.0
    pair_gap = 35.0

    if npn_idx is not None:
        # Input pair Q1 (left, 8 instances)
        for i in range(8):
            pa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8), um(cy - 60 + i * hbt_spacing))))
        # Input pair Q2 (right, 8 instances)
        for i in range(8):
            pa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2), um(cy - 60 + i * hbt_spacing))))
        # Cascode Q3 (left, 8 instances)
        for i in range(8):
            pa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8), um(cy + 30 + i * hbt_spacing))))
        # Cascode Q4 (right, 8 instances)
        for i in range(8):
            pa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2), um(cy + 30 + i * hbt_spacing))))

    # Bias resistor (1kΩ)
    if rppd_idx is not None:
        pa.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx - 0.45), um(cy - 90))))

    # === INTRA-BLOCK ROUTING ===
    pcx = 3.9
    col_dy = 5.425   # upper = collector
    bas_dy = 1.775   # lower = base
    emi_dy = 3.6     # M2 = emitter

    def via_n(cell, x, y, bot_layer, via_layer, top_layer):
        x, y = snap(x), snap(y)
        ps, vs = um(0.5), um(0.19)
        cxi, cyi = um(x), um(y)
        cell.shapes(ly[bot_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))
        cell.shapes(ly[via_layer]).insert(pya.Box(cxi-vs//2, cyi-vs//2, cxi+vs//2, cyi+vs//2))
        cell.shapes(ly[top_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))

    q1_x = cx - pair_gap/2 - 7.8   # 149.7
    q2_x = cx + pair_gap/2          # 192.5
    lx = q1_x + pcx   # 153.6 (left pin center X)
    rx = q2_x + pcx   # 196.4 (right pin center X)

    q1_ys = [cy - 60 + i*hbt_spacing for i in range(8)]  # 215..285
    q2_ys = [cy - 60 + i*hbt_spacing for i in range(8)]
    q3_ys = [cy + 30 + i*hbt_spacing for i in range(8)]  # 305..375
    q4_ys = [cy + 30 + i*hbt_spacing for i in range(8)]

    # --- MIDL (M3): Q1.C + Q3.E ---
    midl_bus_x = q1_x - 4.0  # 145.7
    for qy in q1_ys:
        via_n(pa, lx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(pa, lx, qy+col_dy, 'M2', 'Via2', 'M3')
    for qy in q3_ys:
        via_n(pa, lx, qy+emi_dy, 'M2', 'Via2', 'M3')
    mixer_shapes = ly['M3']
    pa.shapes(mixer_shapes).insert(pya.Box(
        um(midl_bus_x-0.25), um(q1_ys[0]+col_dy-0.25),
        um(midl_bus_x+0.25), um(q3_ys[7]+emi_dy+0.25)))
    for qy in q1_ys:
        pa.shapes(mixer_shapes).insert(pya.Box(
            um(midl_bus_x-0.25), um(qy+col_dy-0.25), um(lx+0.25), um(qy+col_dy+0.25)))
    for qy in q3_ys:
        pa.shapes(mixer_shapes).insert(pya.Box(
            um(midl_bus_x-0.25), um(qy+emi_dy-0.25), um(lx+0.25), um(qy+emi_dy+0.25)))

    # --- MIDR (M3): Q2.C + Q4.E ---
    midr_bus_x = q2_x + 7.8 + 4.0  # 204.3
    for qy in q2_ys:
        via_n(pa, rx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(pa, rx, qy+col_dy, 'M2', 'Via2', 'M3')
    for qy in q4_ys:
        via_n(pa, rx, qy+emi_dy, 'M2', 'Via2', 'M3')
    pa.shapes(mixer_shapes).insert(pya.Box(
        um(midr_bus_x-0.25), um(q2_ys[0]+col_dy-0.25),
        um(midr_bus_x+0.25), um(q4_ys[7]+emi_dy+0.25)))
    for qy in q2_ys:
        pa.shapes(mixer_shapes).insert(pya.Box(
            um(rx-0.25), um(qy+col_dy-0.25), um(midr_bus_x+0.25), um(qy+col_dy+0.25)))
    for qy in q4_ys:
        pa.shapes(mixer_shapes).insert(pya.Box(
            um(rx-0.25), um(qy+emi_dy-0.25), um(midr_bus_x+0.25), um(qy+emi_dy+0.25)))

    # --- TAIL (M4): Q1.E + Q2.E ---
    tail_vl = lx + 3.0    # 156.6
    tail_vr = rx - 3.0    # 193.4
    tail_hy = q1_ys[0] + emi_dy - 3.0  # 215.6
    for qy in q1_ys:
        via_n(pa, lx, qy+emi_dy, 'M2', 'Via2', 'M3')
        via_n(pa, lx, qy+emi_dy, 'M3', 'Via3', 'M4')
        pa.shapes(ly['M4']).insert(pya.Box(
            um(lx-0.25), um(qy+emi_dy-0.25), um(tail_vl+0.25), um(qy+emi_dy+0.25)))
    for qy in q2_ys:
        via_n(pa, rx, qy+emi_dy, 'M2', 'Via2', 'M3')
        via_n(pa, rx, qy+emi_dy, 'M3', 'Via3', 'M4')
        pa.shapes(ly['M4']).insert(pya.Box(
            um(tail_vr-0.25), um(qy+emi_dy-0.25), um(rx+0.25), um(qy+emi_dy+0.25)))
    pa.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl-0.25), um(tail_hy-0.25), um(tail_vl+0.25), um(q1_ys[7]+emi_dy+0.25)))
    pa.shapes(ly['M4']).insert(pya.Box(
        um(tail_vr-0.25), um(tail_hy-0.25), um(tail_vr+0.25), um(q2_ys[7]+emi_dy+0.25)))
    pa.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl-0.25), um(tail_hy-0.25), um(tail_vr+0.25), um(tail_hy+0.25)))

    # --- INP_B (M4): Q1.B ---
    inp_bus_x = q1_x - 6.0  # 143.7
    for qy in q1_ys:
        via_n(pa, lx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(pa, lx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(pa, lx, qy+bas_dy, 'M3', 'Via3', 'M4')
        pa.shapes(ly['M4']).insert(pya.Box(
            um(inp_bus_x-0.25), um(qy+bas_dy-0.25), um(lx+0.25), um(qy+bas_dy+0.25)))
    pa.shapes(ly['M4']).insert(pya.Box(
        um(inp_bus_x-0.25), um(q1_ys[0]+bas_dy-0.25),
        um(inp_bus_x+0.25), um(q1_ys[7]+bas_dy+0.25)))

    # --- INN_B (M4): Q2.B ---
    inn_bus_x = q2_x + 7.8 + 6.0  # 206.3
    for qy in q2_ys:
        via_n(pa, rx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(pa, rx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(pa, rx, qy+bas_dy, 'M3', 'Via3', 'M4')
        pa.shapes(ly['M4']).insert(pya.Box(
            um(rx-0.25), um(qy+bas_dy-0.25), um(inn_bus_x+0.25), um(qy+bas_dy+0.25)))
    pa.shapes(ly['M4']).insert(pya.Box(
        um(inn_bus_x-0.25), um(q2_ys[0]+bas_dy-0.25),
        um(inn_bus_x+0.25), um(q2_ys[7]+bas_dy+0.25)))

    # --- OUTP_C (M4): Q3.C ---
    outp_bus_x = inp_bus_x  # 143.7 (reuse same X, different Y range)
    for qy in q3_ys:
        via_n(pa, lx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(pa, lx, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(pa, lx, qy+col_dy, 'M3', 'Via3', 'M4')
        pa.shapes(ly['M4']).insert(pya.Box(
            um(outp_bus_x-0.25), um(qy+col_dy-0.25), um(lx+0.25), um(qy+col_dy+0.25)))
    pa.shapes(ly['M4']).insert(pya.Box(
        um(outp_bus_x-0.25), um(q3_ys[0]+col_dy-0.25),
        um(outp_bus_x+0.25), um(q3_ys[7]+col_dy+0.25)))

    # --- OUTN_C (M4): Q4.C ---
    outn_bus_x = inn_bus_x  # 206.3
    for qy in q4_ys:
        via_n(pa, rx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(pa, rx, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(pa, rx, qy+col_dy, 'M3', 'Via3', 'M4')
        pa.shapes(ly['M4']).insert(pya.Box(
            um(rx-0.25), um(qy+col_dy-0.25), um(outn_bus_x+0.25), um(qy+col_dy+0.25)))
    pa.shapes(ly['M4']).insert(pya.Box(
        um(outn_bus_x-0.25), um(q4_ys[0]+col_dy-0.25),
        um(outn_bus_x+0.25), um(q4_ys[7]+col_dy+0.25)))

    # --- VCB (M5): Q3.B + Q4.B (shared cascode bias) ---
    vcb_hy = q3_ys[0] + bas_dy - 3.0  # 304.775
    for qy in q3_ys:
        via_n(pa, lx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(pa, lx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(pa, lx, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(pa, lx, qy+bas_dy, 'M4', 'Via4', 'M5')
    for qy in q4_ys:
        via_n(pa, rx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(pa, rx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(pa, rx, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(pa, rx, qy+bas_dy, 'M4', 'Via4', 'M5')
    pa.shapes(ly['M5']).insert(pya.Box(
        um(lx-0.25), um(q3_ys[0]+bas_dy-0.25), um(lx+0.25), um(q3_ys[7]+bas_dy+0.25)))
    pa.shapes(ly['M5']).insert(pya.Box(
        um(rx-0.25), um(q4_ys[0]+bas_dy-0.25), um(rx+0.25), um(q4_ys[7]+bas_dy+0.25)))
    pa.shapes(ly['M5']).insert(pya.Box(
        um(lx-0.25), um(vcb_hy-0.25), um(rx+0.25), um(vcb_hy+0.25)))
    pa.shapes(ly['M5']).insert(pya.Box(
        um(lx-0.25), um(vcb_hy-0.25), um(lx+0.25), um(q3_ys[0]+bas_dy+0.25)))
    pa.shapes(ly['M5']).insert(pya.Box(
        um(rx-0.25), um(vcb_hy-0.25), um(rx+0.25), um(q4_ys[0]+bas_dy+0.25)))

    print("Nets routed: MIDL, MIDR, TAIL, INP_B, INN_B, OUTP_C, OUTN_C, VCB")

    # ----------------------------------------------------------------
    # M5 Port Access Pads
    # Via stacks from internal M3/M4 buses up to M5 with 5µm pads
    # ----------------------------------------------------------------

    # VCC: 3 taps along M3 VCC rail at y=605 (x=60, 175, 290)
    vcc_rail_y = cy + 330.0   # 605.0
    for vcc_tap_x in [60.0, 175.0, 290.0]:
        via_n(pa, vcc_tap_x, vcc_rail_y, 'M3', 'Via3', 'M4')
        via_n(pa, vcc_tap_x, vcc_rail_y, 'M4', 'Via4', 'M5')
        pa.shapes(ly['M5']).insert(pya.Box(
            um(vcc_tap_x - 2.5), um(vcc_rail_y - 2.5),
            um(vcc_tap_x + 2.5), um(vcc_rail_y + 2.5)))
    pa.shapes(ly['M5']).insert(pya.Text("VCC", pya.Trans(um(175.0), um(vcc_rail_y))))

    # TAIL: tap at (cx=175, tail_hy=215.6) on M4 bus → M5
    # Short M4 stub from tail_vl to cx
    pa.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl - 0.25), um(tail_hy - 0.25),
        um(175.0 + 0.25), um(tail_hy + 0.25)))
    via_n(pa, 175.0, tail_hy, 'M4', 'Via4', 'M5')
    pa.shapes(ly['M5']).insert(pya.Box(
        um(175.0 - 2.5), um(tail_hy - 2.5),
        um(175.0 + 2.5), um(tail_hy + 2.5)))
    pa.shapes(ly['M5']).insert(pya.Text("TAIL", pya.Trans(um(175.0), um(tail_hy))))

    # INP_B: tap at (inp_bus_x=143.7, 250) on M4 bus → M5
    via_n(pa, inp_bus_x, 250.0, 'M4', 'Via4', 'M5')
    pa.shapes(ly['M5']).insert(pya.Box(
        um(inp_bus_x - 2.5), um(250.0 - 2.5),
        um(inp_bus_x + 2.5), um(250.0 + 2.5)))
    pa.shapes(ly['M5']).insert(pya.Text("INP_B", pya.Trans(um(inp_bus_x), um(250.0))))

    # INN_B: tap at (inn_bus_x=206.3, 250) on M4 bus → M5
    via_n(pa, inn_bus_x, 250.0, 'M4', 'Via4', 'M5')
    pa.shapes(ly['M5']).insert(pya.Box(
        um(inn_bus_x - 2.5), um(250.0 - 2.5),
        um(inn_bus_x + 2.5), um(250.0 + 2.5)))
    pa.shapes(ly['M5']).insert(pya.Text("INN_B", pya.Trans(um(inn_bus_x), um(250.0))))

    # OUTP_C: tap at (outp_bus_x=143.7, 375) on M4 bus → M5
    via_n(pa, outp_bus_x, 375.0, 'M4', 'Via4', 'M5')
    pa.shapes(ly['M5']).insert(pya.Box(
        um(outp_bus_x - 2.5), um(375.0 - 2.5),
        um(outp_bus_x + 2.5), um(375.0 + 2.5)))
    pa.shapes(ly['M5']).insert(pya.Text("OUTP_C", pya.Trans(um(outp_bus_x), um(375.0))))

    # OUTN_C: tap at (outn_bus_x=206.3, 375) on M4 bus → M5
    via_n(pa, outn_bus_x, 375.0, 'M4', 'Via4', 'M5')
    pa.shapes(ly['M5']).insert(pya.Box(
        um(outn_bus_x - 2.5), um(375.0 - 2.5),
        um(outn_bus_x + 2.5), um(375.0 + 2.5)))
    pa.shapes(ly['M5']).insert(pya.Text("OUTN_C", pya.Trans(um(outn_bus_x), um(375.0))))

    # VCB: already on M5 at vcb_hy=304.775. Extend M5 stub to y=340 pad.
    vcb_pad_y = 340.0
    # M5 stub from vcb_hy up to pad at 340 (center column x=175)
    pa.shapes(ly['M5']).insert(pya.Box(
        um(175.0 - 0.25), um(vcb_hy - 0.25),
        um(175.0 + 0.25), um(vcb_pad_y + 2.5)))
    pa.shapes(ly['M5']).insert(pya.Box(
        um(175.0 - 2.5), um(vcb_pad_y - 2.5),
        um(175.0 + 2.5), um(vcb_pad_y + 2.5)))
    pa.shapes(ly['M5']).insert(pya.Text("VCB", pya.Trans(um(175.0), um(vcb_pad_y))))

    # CPW TLs
    inp_x = cx - pair_gap/2 - 3.9
    inn_x = cx + pair_gap/2 + 3.9

    # TL_input: 97µm
    create_cpw(pa, ly['TM2'], ly['TM2'], inp_x, cy - 120, 97.0, 'down')
    create_cpw(pa, ly['TM2'], ly['TM2'], inn_x, cy - 120, 97.0, 'down')

    # TL_load: 210µm
    create_cpw(pa, ly['TM2'], ly['TM2'], inp_x, cy + 120, 210.0, 'up')
    create_cpw(pa, ly['TM2'], ly['TM2'], inn_x, cy + 120, 210.0, 'up')

    # TL_degen: 58µm
    create_cpw(pa, ly['TM2'], ly['TM2'], cx, cy - 70, 58.0, 'down')

    # Via stacks
    create_via_stack(pa, ly, inp_x, cy - 120)
    create_via_stack(pa, ly, inn_x, cy - 120)
    create_via_stack(pa, ly, inp_x, cy + 120)
    create_via_stack(pa, ly, inn_x, cy + 120)

    # VCC rail
    pa.shapes(ly['M3']).insert(pya.Box(um(10), um(cy + 325), um(CELL_W - 10), um(cy + 335)))

    # ----------------------------------------------------------------
    # Bias resistor wiring (R_bias → VCB net)
    # Connect rppd Pin1 to VCB bus via M1→M5 stack
    # ----------------------------------------------------------------
    rbias_x = cx - 0.45 + 0.25  # rppd pin1 center X
    rbias_y = cy - 90 + 0.78    # rppd pin1 center Y
    via_n(pa, rbias_x, rbias_y, 'M1', 'Via1', 'M2')
    via_n(pa, rbias_x, rbias_y, 'M2', 'Via2', 'M3')
    via_n(pa, rbias_x, rbias_y, 'M3', 'Via3', 'M4')
    via_n(pa, rbias_x, rbias_y, 'M4', 'Via4', 'M5')

    # Port labels (matched to xschem TXPA_77G.sch for LVS)
    pa.shapes(ly['TM2']).insert(pya.Text("INP", pya.Trans(um(inp_x), um(cy - 220))))
    pa.shapes(ly['TM2']).insert(pya.Text("INN", pya.Trans(um(inn_x), um(cy - 220))))
    pa.shapes(ly['TM2']).insert(pya.Text("OUTP", pya.Trans(um(inp_x), um(cy + 335))))
    pa.shapes(ly['TM2']).insert(pya.Text("OUTN", pya.Trans(um(inn_x), um(cy + 335))))
    pa.shapes(ly['M3']).insert(pya.Text("2V4", pya.Trans(um(cx), um(cy + 330))))
    pa.shapes(ly['M5']).insert(pya.Text("GND", pya.Trans(um(cx), um(cy - 130))))
    pa.shapes(ly['M5']).insert(pya.Text("VCB", pya.Trans(um(rbias_x), um(rbias_y))))

    if ext_layout is None:
        output = "/home/bthomas3/Videos/77GHz_phased_array/layout/TXPA_77G_XTOR.gds"
        layout.write(output)
        print(f"\nTX PA layout: {output}")
        print(f"Cell size: {CELL_W} x {CELL_H} um")
        print(f"Devices: 32x npn13G2L + 1x rppd (bias wired)")


if __name__ == "__main__":
    main()
