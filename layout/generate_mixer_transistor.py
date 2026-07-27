"""
77 GHz Mixer (MIXER_77GD) — Transistor-Level Layout
Gilbert cell with CPW transmission lines on IHP SG13G2
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
CELL_H = 450.0


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

    mixer = layout.create_cell("MIXER_77GD")
    cx = CELL_W / 2
    cy = CELL_H / 2

    # Ground plane (TM1 with slots) - Region-based to cut holes at via stacks
    slot_pitch = 25.0
    slot_w = 4.0
    _inp_x = cx - 15.0 - 3.9   # pair_gap=30.0
    _inn_x = cx + 15.0 + 3.9
    via_stack_positions = [(_inp_x, cy - 80), (_inn_x, cy - 80),
                           (_inp_x, cy + 70), (_inn_x, cy + 70)]
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
                        mixer.shapes(ly['TM1']).insert(pya.Box(um(x), um(y), um(x + sw), um(y + sh)))
                x += slot_pitch
        y += slot_pitch

    hbt_spacing = 10.0
    pair_gap = 30.0

    if npn_idx is not None:
        # RF transconductor pair (Nx=4 each side = 8 HBTs)
        for i in range(4):
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8), um(cy - 40 + i * hbt_spacing))))
        for i in range(4):
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2), um(cy - 40 + i * hbt_spacing))))

        # LO switching quad (Nx=2 each = 8 HBTs)
        for i in range(2):
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8 - 15), um(cy + 40 + i * hbt_spacing))))
        for i in range(2):
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8), um(cy + 40 + i * hbt_spacing))))
        for i in range(2):
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2), um(cy + 40 + i * hbt_spacing))))
        for i in range(2):
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2 + 15), um(cy + 40 + i * hbt_spacing))))

    # Load resistors (2× 500Ω) and tail resistor (200Ω)
    if rppd_idx is not None:
        mixer.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx - 20), um(cy + 80))))
        mixer.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx + 20), um(cy + 80))))
        mixer.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx - 0.45), um(cy - 70))))

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

    # Device positions
    q1_x = cx - pair_gap/2 - 7.8   # 127.2
    q2_x = cx + pair_gap/2          # 165.0
    sw1_x = cx - pair_gap/2 - 7.8 - 15  # 112.2
    sw2_x = cx - pair_gap/2 - 7.8       # 127.2
    sw3_x = cx + pair_gap/2              # 165.0
    sw4_x = cx + pair_gap/2 + 15         # 180.0

    q1_ys = [cy - 40 + i*hbt_spacing for i in range(4)]   # 185,195,205,215
    q2_ys = [cy - 40 + i*hbt_spacing for i in range(4)]
    sw1_ys = [cy + 40 + i*hbt_spacing for i in range(2)]  # 265,275
    sw2_ys = [cy + 40 + i*hbt_spacing for i in range(2)]
    sw3_ys = [cy + 40 + i*hbt_spacing for i in range(2)]
    sw4_ys = [cy + 40 + i*hbt_spacing for i in range(2)]

    # Pin center X for each column
    q1_px = q1_x + pcx    # 131.1
    q2_px = q2_x + pcx    # 168.9
    sw1_px = sw1_x + pcx  # 116.1
    sw2_px = sw2_x + pcx  # 131.1
    sw3_px = sw3_x + pcx  # 168.9
    sw4_px = sw4_x + pcx  # 183.9

    # --- MIDL (M3): Q1.C + SW1.E + SW2.E ---
    midl_bus_x = 108.0
    for qy in q1_ys:
        via_n(mixer, q1_px, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, q1_px, qy+col_dy, 'M2', 'Via2', 'M3')
    for qy in sw1_ys:
        via_n(mixer, sw1_px, qy+emi_dy, 'M2', 'Via2', 'M3')
    for qy in sw2_ys:
        via_n(mixer, sw2_px, qy+emi_dy, 'M2', 'Via2', 'M3')
    # M3 bus vertical
    mixer.shapes(ly['M3']).insert(pya.Box(
        um(midl_bus_x-0.25), um(q1_ys[0]+col_dy-0.25),
        um(midl_bus_x+0.25), um(sw2_ys[1]+emi_dy+0.25)))
    # Stubs from bus to Q1.C pads
    for qy in q1_ys:
        mixer.shapes(ly['M3']).insert(pya.Box(
            um(midl_bus_x-0.25), um(qy+col_dy-0.25), um(q1_px+0.25), um(qy+col_dy+0.25)))
    # Stubs from bus to SW1.E pads
    for qy in sw1_ys:
        mixer.shapes(ly['M3']).insert(pya.Box(
            um(midl_bus_x-0.25), um(qy+emi_dy-0.25), um(sw1_px+0.25), um(qy+emi_dy+0.25)))
    # Stubs from bus to SW2.E pads
    for qy in sw2_ys:
        mixer.shapes(ly['M3']).insert(pya.Box(
            um(midl_bus_x-0.25), um(qy+emi_dy-0.25), um(sw2_px+0.25), um(qy+emi_dy+0.25)))

    # --- MIDR (M3): Q2.C + SW3.E + SW4.E ---
    midr_bus_x = 192.0
    for qy in q2_ys:
        via_n(mixer, q2_px, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, q2_px, qy+col_dy, 'M2', 'Via2', 'M3')
    for qy in sw3_ys:
        via_n(mixer, sw3_px, qy+emi_dy, 'M2', 'Via2', 'M3')
    for qy in sw4_ys:
        via_n(mixer, sw4_px, qy+emi_dy, 'M2', 'Via2', 'M3')
    mixer.shapes(ly['M3']).insert(pya.Box(
        um(midr_bus_x-0.25), um(q2_ys[0]+col_dy-0.25),
        um(midr_bus_x+0.25), um(sw4_ys[1]+emi_dy+0.25)))
    for qy in q2_ys:
        mixer.shapes(ly['M3']).insert(pya.Box(
            um(q2_px-0.25), um(qy+col_dy-0.25), um(midr_bus_x+0.25), um(qy+col_dy+0.25)))
    for qy in sw3_ys:
        mixer.shapes(ly['M3']).insert(pya.Box(
            um(sw3_px-0.25), um(qy+emi_dy-0.25), um(midr_bus_x+0.25), um(qy+emi_dy+0.25)))
    for qy in sw4_ys:
        mixer.shapes(ly['M3']).insert(pya.Box(
            um(sw4_px-0.25), um(qy+emi_dy-0.25), um(midr_bus_x+0.25), um(qy+emi_dy+0.25)))

    # --- TAIL (M4): Q1.E + Q2.E ---
    tail_vl = q1_px + 3.0   # 134.1 (offset right of Q1 pins)
    tail_vr = q2_px - 3.0   # 165.9 (offset left of Q2 pins)
    tail_hy = q1_ys[0] + emi_dy - 3.0  # 185.6 (below bottom device)
    for qy in q1_ys:
        via_n(mixer, q1_px, qy+emi_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, q1_px, qy+emi_dy, 'M3', 'Via3', 'M4')
        mixer.shapes(ly['M4']).insert(pya.Box(
            um(q1_px-0.25), um(qy+emi_dy-0.25), um(tail_vl+0.25), um(qy+emi_dy+0.25)))
    for qy in q2_ys:
        via_n(mixer, q2_px, qy+emi_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, q2_px, qy+emi_dy, 'M3', 'Via3', 'M4')
        mixer.shapes(ly['M4']).insert(pya.Box(
            um(tail_vr-0.25), um(qy+emi_dy-0.25), um(q2_px+0.25), um(qy+emi_dy+0.25)))
    # M4 verticals
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl-0.25), um(tail_hy-0.25),
        um(tail_vl+0.25), um(q1_ys[3]+emi_dy+0.25)))
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(tail_vr-0.25), um(tail_hy-0.25),
        um(tail_vr+0.25), um(q2_ys[3]+emi_dy+0.25)))
    # M4 horizontal connecting both verticals
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl-0.25), um(tail_hy-0.25), um(tail_vr+0.25), um(tail_hy+0.25)))

    # --- RF_P (M4): Q1.B ---
    rfp_bus_x = q1_px - 8.0  # 123.1
    for qy in q1_ys:
        via_n(mixer, q1_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, q1_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, q1_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        mixer.shapes(ly['M4']).insert(pya.Box(
            um(rfp_bus_x-0.25), um(qy+bas_dy-0.25), um(q1_px+0.25), um(qy+bas_dy+0.25)))
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(rfp_bus_x-0.25), um(q1_ys[0]+bas_dy-0.25),
        um(rfp_bus_x+0.25), um(q1_ys[3]+bas_dy+0.25)))

    # --- RF_N (M4): Q2.B ---
    rfn_bus_x = q2_px + pcx + 4.1  # 176.9... let me use 177.0
    rfn_bus_x = q2_px + 8.0  # 173.0
    for qy in q2_ys:
        via_n(mixer, q2_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, q2_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, q2_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        mixer.shapes(ly['M4']).insert(pya.Box(
            um(q2_px-0.25), um(qy+bas_dy-0.25), um(rfn_bus_x+0.25), um(qy+bas_dy+0.25)))
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(rfn_bus_x-0.25), um(q2_ys[0]+bas_dy-0.25),
        um(rfn_bus_x+0.25), um(q2_ys[3]+bas_dy+0.25)))

    # --- LO_P (M5): SW1.B + SW4.B (cross-connected) ---
    # Route LO on M5 to avoid M4 overlap with IF M4 pads
    lop_hy = sw1_ys[0] + bas_dy - 3.0  # 263.775
    for qy in sw1_ys:
        via_n(mixer, sw1_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, sw1_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, sw1_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(mixer, sw1_px, qy+bas_dy, 'M4', 'Via4', 'M5')
    for qy in sw4_ys:
        via_n(mixer, sw4_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, sw4_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, sw4_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(mixer, sw4_px, qy+bas_dy, 'M4', 'Via4', 'M5')
    # M5 verticals for SW1.B
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(sw1_px-0.25), um(sw1_ys[0]+bas_dy-0.25),
        um(sw1_px+0.25), um(sw1_ys[1]+bas_dy+0.25)))
    # M5 verticals for SW4.B
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(sw4_px-0.25), um(sw4_ys[0]+bas_dy-0.25),
        um(sw4_px+0.25), um(sw4_ys[1]+bas_dy+0.25)))
    # M5 horizontal connecting SW1 and SW4 (at bottom base Y)
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(sw1_px-0.25), um(lop_hy-0.25), um(sw4_px+0.25), um(lop_hy+0.25)))
    # M5 stubs from verticals to horizontal
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(sw1_px-0.25), um(lop_hy-0.25), um(sw1_px+0.25), um(sw1_ys[0]+bas_dy+0.25)))
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(sw4_px-0.25), um(lop_hy-0.25), um(sw4_px+0.25), um(sw4_ys[0]+bas_dy+0.25)))

    # --- LO_N (M5): SW2.B + SW3.B ---
    lon_hy = sw2_ys[1] + bas_dy + 3.0  # 279.775
    for qy in sw2_ys:
        via_n(mixer, sw2_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, sw2_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, sw2_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(mixer, sw2_px, qy+bas_dy, 'M4', 'Via4', 'M5')
    for qy in sw3_ys:
        via_n(mixer, sw3_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, sw3_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, sw3_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(mixer, sw3_px, qy+bas_dy, 'M4', 'Via4', 'M5')
    # M5 verticals for SW2.B
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(sw2_px-0.25), um(sw2_ys[0]+bas_dy-0.25),
        um(sw2_px+0.25), um(lon_hy+0.25)))
    # M5 verticals for SW3.B
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(sw3_px-0.25), um(sw3_ys[0]+bas_dy-0.25),
        um(sw3_px+0.25), um(lon_hy+0.25)))
    # M5 horizontal
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(sw2_px-0.25), um(lon_hy-0.25), um(sw3_px+0.25), um(lon_hy+0.25)))

    # --- IF_P (M4): SW1.C + SW4.C ---
    # Use M4 with offset X verticals to avoid LO M4 pads
    ifp_vl = sw1_px - 3.0   # 113.1 (left of SW1 pins)
    ifp_vr = sw4_px + 3.0   # 186.9 (right of SW4 pins)
    ifp_hy = sw1_ys[1] + col_dy + 3.0  # 283.425
    for qy in sw1_ys:
        via_n(mixer, sw1_px, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, sw1_px, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, sw1_px, qy+col_dy, 'M3', 'Via3', 'M4')
        mixer.shapes(ly['M4']).insert(pya.Box(
            um(ifp_vl-0.25), um(qy+col_dy-0.25), um(sw1_px+0.25), um(qy+col_dy+0.25)))
    for qy in sw4_ys:
        via_n(mixer, sw4_px, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, sw4_px, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, sw4_px, qy+col_dy, 'M3', 'Via3', 'M4')
        mixer.shapes(ly['M4']).insert(pya.Box(
            um(sw4_px-0.25), um(qy+col_dy-0.25), um(ifp_vr+0.25), um(qy+col_dy+0.25)))
    # M4 verticals at offset X
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(ifp_vl-0.25), um(sw1_ys[0]+col_dy-0.25),
        um(ifp_vl+0.25), um(ifp_hy+0.25)))
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(ifp_vr-0.25), um(sw4_ys[0]+col_dy-0.25),
        um(ifp_vr+0.25), um(ifp_hy+0.25)))
    # M4 horizontal connecting both
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(ifp_vl-0.25), um(ifp_hy-0.25), um(ifp_vr+0.25), um(ifp_hy+0.25)))

    # --- IF_N (M4): SW2.C + SW3.C ---
    # Route on M4 with horizontal BELOW IF_P horizontal and offset X verticals
    ifn_vl = sw2_px + 3.0   # 134.1
    ifn_vr = sw3_px - 3.0   # 165.9
    ifn_hy = sw2_ys[0] + col_dy - 3.0  # 267.425 (below IF_P horizontal at 283.425)
    for qy in sw2_ys:
        via_n(mixer, sw2_px, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, sw2_px, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, sw2_px, qy+col_dy, 'M3', 'Via3', 'M4')
        mixer.shapes(ly['M4']).insert(pya.Box(
            um(sw2_px-0.25), um(qy+col_dy-0.25), um(ifn_vl+0.25), um(qy+col_dy+0.25)))
    for qy in sw3_ys:
        via_n(mixer, sw3_px, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(mixer, sw3_px, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(mixer, sw3_px, qy+col_dy, 'M3', 'Via3', 'M4')
        mixer.shapes(ly['M4']).insert(pya.Box(
            um(ifn_vr-0.25), um(qy+col_dy-0.25), um(sw3_px+0.25), um(qy+col_dy+0.25)))
    # M4 verticals at offset X
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(ifn_vl-0.25), um(ifn_hy-0.25),
        um(ifn_vl+0.25), um(sw2_ys[1]+col_dy+0.25)))
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(ifn_vr-0.25), um(ifn_hy-0.25),
        um(ifn_vr+0.25), um(sw3_ys[1]+col_dy+0.25)))
    # M4 horizontal
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(ifn_vl-0.25), um(ifn_hy-0.25), um(ifn_vr+0.25), um(ifn_hy+0.25)))

    print("Nets routed: MIDL, MIDR, TAIL, RF_P, RF_N, LO_P, LO_N, IF_P, IF_N")

    # ----------------------------------------------------------------
    # M5 Port Access Pads
    # Via stacks from internal M3/M4 buses up to M5 with 5µm pads
    # ----------------------------------------------------------------

    # VCC: 3 taps along M3 VCC rail at y=360 (x=60, 150, 240)
    for vcc_tap_x in [60.0, 150.0, 240.0]:
        via_n(mixer, vcc_tap_x, 360.0, 'M3', 'Via3', 'M4')
        via_n(mixer, vcc_tap_x, 360.0, 'M4', 'Via4', 'M5')
        mixer.shapes(ly['M5']).insert(pya.Box(
            um(vcc_tap_x - 2.5), um(360.0 - 2.5),
            um(vcc_tap_x + 2.5), um(360.0 + 2.5)))
    mixer.shapes(ly['M5']).insert(pya.Text("VCC", pya.Trans(um(150.0), um(360.0))))

    # TAIL: tap at (150, 185.6) on M4 bus → M5
    # Short M4 stub from tail_vl (134.1) to tap point at cx=150
    mixer.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl - 0.25), um(tail_hy - 0.25),
        um(150.0 + 0.25), um(tail_hy + 0.25)))
    via_n(mixer, 150.0, tail_hy, 'M4', 'Via4', 'M5')
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(150.0 - 2.5), um(tail_hy - 2.5),
        um(150.0 + 2.5), um(tail_hy + 2.5)))
    mixer.shapes(ly['M5']).insert(pya.Text("TAIL", pya.Trans(um(150.0), um(tail_hy))))

    # RF_P: tap at (123.1, 200) on M4 bus rfp_bus_x=123.1
    via_n(mixer, rfp_bus_x, 200.0, 'M4', 'Via4', 'M5')
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(rfp_bus_x - 2.5), um(200.0 - 2.5),
        um(rfp_bus_x + 2.5), um(200.0 + 2.5)))
    mixer.shapes(ly['M5']).insert(pya.Text("RF_P", pya.Trans(um(rfp_bus_x), um(200.0))))

    # RF_N: tap at (173.0, 200) on M4 bus rfn_bus_x
    via_n(mixer, rfn_bus_x, 200.0, 'M4', 'Via4', 'M5')
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(rfn_bus_x - 2.5), um(200.0 - 2.5),
        um(rfn_bus_x + 2.5), um(200.0 + 2.5)))
    mixer.shapes(ly['M5']).insert(pya.Text("RF_N", pya.Trans(um(rfn_bus_x), um(200.0))))

    # LO_P: already on M5 (lop_hy=263.775), add 5µm pad at (150, 263.775)
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(150.0 - 2.5), um(lop_hy - 2.5),
        um(150.0 + 2.5), um(lop_hy + 2.5)))
    mixer.shapes(ly['M5']).insert(pya.Text("LO_P", pya.Trans(um(150.0), um(lop_hy))))

    # LO_N: already on M5 (lon_hy=279.775), add 5µm pad at (150, 279.775)
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(150.0 - 2.5), um(lon_hy - 2.5),
        um(150.0 + 2.5), um(lon_hy + 2.5)))
    mixer.shapes(ly['M5']).insert(pya.Text("LO_N", pya.Trans(um(150.0), um(lon_hy))))

    # IF_P: tap at (ifp_vl=113.1, ifp_hy=283.425) on M4 bus → M5
    via_n(mixer, ifp_vl, ifp_hy, 'M4', 'Via4', 'M5')
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(ifp_vl - 2.5), um(ifp_hy - 2.5),
        um(ifp_vl + 2.5), um(ifp_hy + 2.5)))
    mixer.shapes(ly['M5']).insert(pya.Text("IF_P", pya.Trans(um(ifp_vl), um(ifp_hy))))

    # IF_N: tap at (ifn_vl=134.1, ifn_hy=267.425) on M4 bus → M5
    via_n(mixer, ifn_vl, ifn_hy, 'M4', 'Via4', 'M5')
    mixer.shapes(ly['M5']).insert(pya.Box(
        um(ifn_vl - 2.5), um(ifn_hy - 2.5),
        um(ifn_vl + 2.5), um(ifn_hy + 2.5)))
    mixer.shapes(ly['M5']).insert(pya.Text("IF_N", pya.Trans(um(ifn_vl), um(ifn_hy))))

    # CPW TLs
    inp_x = cx - pair_gap/2 - 3.9
    inn_x = cx + pair_gap/2 + 3.9

    # TL_RF: 125µm (RF input matching)
    create_cpw(mixer, ly['TM2'], ly['TM2'], inp_x, cy - 80, 125.0, 'down')
    create_cpw(mixer, ly['TM2'], ly['TM2'], inn_x, cy - 80, 125.0, 'down')

    # TL_LO: 49µm (LO feed)
    create_cpw(mixer, ly['TM2'], ly['TM2'], inp_x, cy + 70, 49.0, 'up')
    create_cpw(mixer, ly['TM2'], ly['TM2'], inn_x, cy + 70, 49.0, 'up')

    # Via stacks
    create_via_stack(mixer, ly, inp_x, cy - 80)
    create_via_stack(mixer, ly, inn_x, cy - 80)
    create_via_stack(mixer, ly, inp_x, cy + 70)
    create_via_stack(mixer, ly, inn_x, cy + 70)

    # VCC rail
    mixer.shapes(ly['M3']).insert(pya.Box(um(10), um(cy + 130), um(CELL_W - 10), um(cy + 140)))

    # Port labels
    mixer.shapes(ly['TM2']).insert(pya.Text("RF_P", pya.Trans(um(inp_x), um(cy - 210))))
    mixer.shapes(ly['TM2']).insert(pya.Text("RF_N", pya.Trans(um(inn_x), um(cy - 210))))
    mixer.shapes(ly['TM2']).insert(pya.Text("LO_P", pya.Trans(um(inp_x), um(cy + 125))))
    mixer.shapes(ly['TM2']).insert(pya.Text("LO_N", pya.Trans(um(inn_x), um(cy + 125))))
    mixer.shapes(ly['M3']).insert(pya.Text("VCC", pya.Trans(um(cx), um(cy + 135))))

    if ext_layout is None:
        output = "/home/bthomas3/Videos/77GHz_phased_array/layout/MIXER_77G_XTOR.gds"
        layout.write(output)
        print(f"\nMixer layout: {output}")
        print(f"Cell size: {CELL_W} x {CELL_H} um")
        print(f"Devices: 16x npn13G2L + 3x rppd")


if __name__ == "__main__":
    main()
