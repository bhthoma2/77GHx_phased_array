"""
77 GHz LNA (RXAMP_77GD) — Transistor-Level Layout
Differential cascode with CPW transmission lines on IHP SG13G2
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
CELL_H = 500.0


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
    cmim_idx = layout.cell_by_name("cmim") if layout.has_cell("cmim") else None
    rppd_idx = layout.cell_by_name("rppd") if layout.has_cell("rppd") else None

    lna = layout.create_cell("RXAMP_77GD")
    cx = CELL_W / 2
    cy = CELL_H / 2

    # Ground plane (TM1 with slots) - Region-based to cut holes at via stacks
    slot_pitch = 25.0
    slot_w = 4.0
    via_stack_positions = [(cx - 15.0 - 3.9, cy - 100), (cx + 15.0 + 3.9, cy - 100),
                           (cx - 15.0 - 3.9, cy + 80), (cx + 15.0 + 3.9, cy + 80)]
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
                        lna.shapes(ly['TM1']).insert(pya.Box(um(x), um(y), um(x + sw), um(y + sh)))
                x += slot_pitch
        y += slot_pitch

    # HBTs: differential cascode = 4 transistors × Nx=4 = 16 instances
    hbt_spacing = 10.0
    pair_gap = 30.0

    if npn_idx is not None:
        # Input pair Q1 (left, 4 instances)
        for i in range(4):
            lna.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8), um(cy - 20 + i * hbt_spacing))))
        # Input pair Q2 (right, 4 instances)
        for i in range(4):
            lna.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2), um(cy - 20 + i * hbt_spacing))))
        # Cascode Q3 (left, 4 instances)
        for i in range(4):
            lna.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8), um(cy + 30 + i * hbt_spacing))))
        # Cascode Q4 (right, 4 instances)
        for i in range(4):
            lna.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2), um(cy + 30 + i * hbt_spacing))))

    # Input matching caps (2× 30fF cmim)
    if cmim_idx is not None:
        lna.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx - 50), um(cy - 60))))
        lna.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx + 42), um(cy - 60))))

    # Bias resistor (2kΩ rppd)
    if rppd_idx is not None:
        lna.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx - 0.45), um(cy - 80))))

    # CPW TLs on TM2
    inp_x = cx - pair_gap/2 - 3.9
    inn_x = cx + pair_gap/2 + 3.9

    # TL_input: 97µm stubs (input matching)
    create_cpw(lna, ly['TM2'], ly['TM2'], inp_x, cy - 100, 97.0, 'down')
    create_cpw(lna, ly['TM2'], ly['TM2'], inn_x, cy - 100, 97.0, 'down')

    # TL_load: 210µm (collector load)
    create_cpw(lna, ly['TM2'], ly['TM2'], inp_x, cy + 80, 210.0, 'up')
    create_cpw(lna, ly['TM2'], ly['TM2'], inn_x, cy + 80, 210.0, 'up')

    # TL_degen: 58µm (emitter degeneration)
    create_cpw(lna, ly['TM2'], ly['TM2'], cx, cy - 30, 58.0, 'down')

    # Via stacks at TL endpoints
    create_via_stack(lna, ly, inp_x, cy - 100)
    create_via_stack(lna, ly, inn_x, cy - 100)
    create_via_stack(lna, ly, inp_x, cy + 80)
    create_via_stack(lna, ly, inn_x, cy + 80)

    # === INTRA-BLOCK ROUTING ===
    # LVS: upper M1 (cell_y+5.425) = BASE, lower M1 (cell_y+1.775) = COLLECTOR
    # Emitter on M2 (cell center). NO vertical M2 buses (would short through emitter pins).
    # All inter-device routing on M3+ with offset X buses to avoid interleaving.
    pcx = 3.9
    col_dy = 5.425   # upper = collector
    bas_dy = 1.775   # lower = base
    emi_dy = 3.6     # M2 emitter center

    def via_n(cell, x, y, bot_layer, via_layer, top_layer):
        x, y = snap(x), snap(y)
        ps = um(0.5)
        vs = um(0.19)
        cxi, cyi = um(x), um(y)
        cell.shapes(ly[bot_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))
        cell.shapes(ly[via_layer]).insert(pya.Box(cxi-vs//2, cyi-vs//2, cxi+vs//2, cyi+vs//2))
        cell.shapes(ly[top_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))

    q1_x = cx - pair_gap/2 - 7.8  # 127.2
    q2_x = cx + pair_gap/2         # 165.0
    q1_ys = [cy - 20 + i*hbt_spacing for i in range(4)]
    q2_ys = [cy - 20 + i*hbt_spacing for i in range(4)]
    q3_ys = [cy + 30 + i*hbt_spacing for i in range(4)]
    q4_ys = [cy + 30 + i*hbt_spacing for i in range(4)]
    lx = q1_x + pcx   # 131.1 (left pin center X)
    rx = q2_x + pcx   # 168.9 (right pin center X)

    # --- MIDL: Q1.C + Q3.E on M3 (left cascode midpoint) ---
    # Use offset X for emitter vias (lx-1.0) to separate from other nets at lx
    midl_bus_x = q1_x - 4.0  # 123.2
    emi_via_lx = lx - 1.0    # 130.1 (still within emitter M2 x range 129.7-132.5)
    emi_via_rx = rx + 1.0    # 169.9
    for qy in q1_ys:  # Q1 collectors → M3
        via_n(lna, lx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(lna, lx, qy+col_dy, 'M2', 'Via2', 'M3')
    for qy in q3_ys:  # Q3 emitters → M3 at offset X
        via_n(lna, emi_via_lx, qy+emi_dy, 'M2', 'Via2', 'M3')
    lna.shapes(ly['M3']).insert(pya.Box(
        um(midl_bus_x-0.25), um(q1_ys[0]+col_dy-0.25),
        um(midl_bus_x+0.25), um(q3_ys[3]+emi_dy+0.25)))
    for qy in q1_ys:
        lna.shapes(ly['M3']).insert(pya.Box(
            um(midl_bus_x-0.25), um(qy+col_dy-0.25), um(lx+0.25), um(qy+col_dy+0.25)))
    for qy in q3_ys:
        lna.shapes(ly['M3']).insert(pya.Box(
            um(midl_bus_x-0.25), um(qy+emi_dy-0.25), um(emi_via_lx+0.25), um(qy+emi_dy+0.25)))

    # --- MIDR: Q2.C + Q4.E on M3 (right cascode midpoint) ---
    midr_bus_x = q2_x + 7.8 + 4.0  # 176.8
    for qy in q2_ys:
        via_n(lna, rx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(lna, rx, qy+col_dy, 'M2', 'Via2', 'M3')
    for qy in q4_ys:  # Q4 emitters at offset X
        via_n(lna, emi_via_rx, qy+emi_dy, 'M2', 'Via2', 'M3')
    lna.shapes(ly['M3']).insert(pya.Box(
        um(midr_bus_x-0.25), um(q2_ys[0]+col_dy-0.25),
        um(midr_bus_x+0.25), um(q4_ys[3]+emi_dy+0.25)))
    for qy in q2_ys:
        lna.shapes(ly['M3']).insert(pya.Box(
            um(rx-0.25), um(qy+col_dy-0.25), um(midr_bus_x+0.25), um(qy+col_dy+0.25)))
    for qy in q4_ys:
        lna.shapes(ly['M3']).insert(pya.Box(
            um(emi_via_rx-0.25), um(qy+emi_dy-0.25), um(midr_bus_x+0.25), um(qy+emi_dy+0.25)))

    # --- INP_B: Q1 bases on M4 ---
    inp_bus_x = q1_x - 6.0  # 121.2
    for qy in q1_ys:
        via_n(lna, lx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(lna, lx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(lna, lx, qy+bas_dy, 'M3', 'Via3', 'M4')
    lna.shapes(ly['M4']).insert(pya.Box(
        um(inp_bus_x-0.25), um(q1_ys[0]+bas_dy-0.25),
        um(inp_bus_x+0.25), um(q1_ys[3]+bas_dy+0.25)))
    for qy in q1_ys:
        lna.shapes(ly['M4']).insert(pya.Box(
            um(inp_bus_x-0.25), um(qy+bas_dy-0.25), um(lx+0.25), um(qy+bas_dy+0.25)))

    # --- INN_B: Q2 bases on M4 ---
    inn_bus_x = q2_x + 7.8 + 6.0  # 178.8
    for qy in q2_ys:
        via_n(lna, rx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(lna, rx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(lna, rx, qy+bas_dy, 'M3', 'Via3', 'M4')
    lna.shapes(ly['M4']).insert(pya.Box(
        um(inn_bus_x-0.25), um(q2_ys[0]+bas_dy-0.25),
        um(inn_bus_x+0.25), um(q2_ys[3]+bas_dy+0.25)))
    for qy in q2_ys:
        lna.shapes(ly['M4']).insert(pya.Box(
            um(rx-0.25), um(qy+bas_dy-0.25), um(inn_bus_x+0.25), um(qy+bas_dy+0.25)))

    # --- OUTP_C: Q3 collectors on M4 (different Y from INP_B, no conflict) ---
    for qy in q3_ys:
        via_n(lna, lx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(lna, lx, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(lna, lx, qy+col_dy, 'M3', 'Via3', 'M4')
    lna.shapes(ly['M4']).insert(pya.Box(
        um(inp_bus_x-0.25), um(q3_ys[0]+col_dy-0.25),
        um(inp_bus_x+0.25), um(q3_ys[3]+col_dy+0.25)))
    for qy in q3_ys:
        lna.shapes(ly['M4']).insert(pya.Box(
            um(inp_bus_x-0.25), um(qy+col_dy-0.25), um(lx+0.25), um(qy+col_dy+0.25)))

    # --- OUTN_C: Q4 collectors on M4 ---
    for qy in q4_ys:
        via_n(lna, rx, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(lna, rx, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(lna, rx, qy+col_dy, 'M3', 'Via3', 'M4')
    lna.shapes(ly['M4']).insert(pya.Box(
        um(inn_bus_x-0.25), um(q4_ys[0]+col_dy-0.25),
        um(inn_bus_x+0.25), um(q4_ys[3]+col_dy+0.25)))
    for qy in q4_ys:
        lna.shapes(ly['M4']).insert(pya.Box(
            um(rx-0.25), um(qy+col_dy-0.25), um(inn_bus_x+0.25), um(qy+col_dy+0.25)))

    # --- VCB: Q3/Q4 bases on M5 ---
    for qy in q3_ys:
        via_n(lna, lx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(lna, lx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(lna, lx, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(lna, lx, qy+bas_dy, 'M4', 'Via4', 'M5')
    for qy in q4_ys:
        via_n(lna, rx, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(lna, rx, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(lna, rx, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(lna, rx, qy+bas_dy, 'M4', 'Via4', 'M5')
    lna.shapes(ly['M5']).insert(pya.Box(
        um(lx-0.25), um(q3_ys[0]+bas_dy-0.25), um(lx+0.25), um(q3_ys[3]+bas_dy+0.25)))
    lna.shapes(ly['M5']).insert(pya.Box(
        um(rx-0.25), um(q4_ys[0]+bas_dy-0.25), um(rx+0.25), um(q4_ys[3]+bas_dy+0.25)))
    vcb_y = (q3_ys[1]+q3_ys[2])/2 + bas_dy
    lna.shapes(ly['M5']).insert(pya.Box(
        um(lx-0.25), um(vcb_y-0.25), um(rx+0.25), um(vcb_y+0.25)))

    # --- TAIL: Q1/Q2 emitters on M4 (via M2→Via2→M3→Via3→M4) ---
    # TAIL vertical at OFFSET X (right of lx, left of rx) to avoid INP_B M4 stubs
    tail_vl = lx + 3.0   # 134.1 (right of lx, clear of INP_B stubs going left)
    tail_vr = rx - 3.0   # 165.9 (left of rx, clear of INN_B stubs going right)
    for qy in q1_ys:
        via_n(lna, lx, qy+emi_dy, 'M2', 'Via2', 'M3')
        via_n(lna, lx, qy+emi_dy, 'M3', 'Via3', 'M4')
    for qy in q2_ys:
        via_n(lna, rx, qy+emi_dy, 'M2', 'Via2', 'M3')
        via_n(lna, rx, qy+emi_dy, 'M3', 'Via3', 'M4')
    # Left TAIL vertical at offset X
    lna.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl-0.25), um(q1_ys[0]+emi_dy-0.25), um(tail_vl+0.25), um(q1_ys[3]+emi_dy+0.25)))
    for qy in q1_ys:
        lna.shapes(ly['M4']).insert(pya.Box(
            um(lx-0.25), um(qy+emi_dy-0.25), um(tail_vl+0.25), um(qy+emi_dy+0.25)))
    # Right TAIL vertical at offset X
    lna.shapes(ly['M4']).insert(pya.Box(
        um(tail_vr-0.25), um(q2_ys[0]+emi_dy-0.25), um(tail_vr+0.25), um(q2_ys[3]+emi_dy+0.25)))
    for qy in q2_ys:
        lna.shapes(ly['M4']).insert(pya.Box(
            um(tail_vr-0.25), um(qy+emi_dy-0.25), um(rx+0.25), um(qy+emi_dy+0.25)))
    # Horizontal connecting both TAIL verticals
    tail_y = (q1_ys[1]+q1_ys[2])/2 + emi_dy
    lna.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl-0.25), um(tail_y-0.25), um(tail_vr+0.25), um(tail_y+0.25)))

    # VCC rail (M3)
    vcc_y = cy + 290.0
    lna.shapes(ly['M3']).insert(pya.Box(um(10), um(vcc_y - 5), um(CELL_W - 10), um(vcc_y + 5)))

    # === M5 PORT ACCESS PADS (for top-level connection) ===
    # 5µm M5 pads at defined cell-edge positions with via stacks to internal nets
    port_pad = 5.0  # port pad size on M5

    def port_via(x, y, from_layer, to_layer):
        """Via stack from from_layer to to_layer at (x,y)"""
        stack = [('M3','Via3','M4',0.19,0.5),('M4','Via4','M5',0.19,0.5)]
        started = False
        for bot, via, top_l, vs, ps in stack:
            if bot == from_layer: started = True
            if started:
                via_n(lna, x, y, bot, via, top_l)
            if top_l == to_layer: break

    # VCC ports: 3 taps along VCC rail → M5
    for vx in [60.0, cx, CELL_W - 60.0]:
        port_via(vx, vcc_y, 'M3', 'M5')
        lna.shapes(ly['M5']).insert(pya.Box(
            um(vx - port_pad/2), um(vcc_y - port_pad/2),
            um(vx + port_pad/2), um(vcc_y + port_pad/2)))

    # TAIL port: tap TAIL M4 bus at bottom-center → M5
    tail_port_x = cx
    tail_port_y = q1_ys[0] + emi_dy
    via_n(lna, tail_port_x, tail_port_y, 'M4', 'Via4', 'M5')
    # Connect to TAIL M4 horizontal
    lna.shapes(ly['M4']).insert(pya.Box(
        um(tail_vl - 0.25), um(tail_port_y - 0.25),
        um(tail_port_x + 0.25), um(tail_port_y + 0.25)))
    lna.shapes(ly['M5']).insert(pya.Box(
        um(tail_port_x - port_pad/2), um(tail_port_y - port_pad/2),
        um(tail_port_x + port_pad/2), um(tail_port_y + port_pad/2)))

    # INP port: tap INP_B M4 bus at left edge → M5
    inp_port_y = (q1_ys[0] + q1_ys[3]) / 2 + bas_dy
    via_n(lna, inp_bus_x, inp_port_y, 'M4', 'Via4', 'M5')
    lna.shapes(ly['M4']).insert(pya.Box(
        um(inp_bus_x - 0.25), um(inp_port_y - 0.25),
        um(inp_bus_x + 0.25), um(inp_port_y + 0.25)))
    lna.shapes(ly['M5']).insert(pya.Box(
        um(inp_bus_x - port_pad/2), um(inp_port_y - port_pad/2),
        um(inp_bus_x + port_pad/2), um(inp_port_y + port_pad/2)))

    # INN port: tap INN_B M4 bus at right edge → M5
    via_n(lna, inn_bus_x, inp_port_y, 'M4', 'Via4', 'M5')
    lna.shapes(ly['M4']).insert(pya.Box(
        um(inn_bus_x - 0.25), um(inp_port_y - 0.25),
        um(inn_bus_x + 0.25), um(inp_port_y + 0.25)))
    lna.shapes(ly['M5']).insert(pya.Box(
        um(inn_bus_x - port_pad/2), um(inp_port_y - port_pad/2),
        um(inn_bus_x + port_pad/2), um(inp_port_y + port_pad/2)))

    # OUTP port: tap OUTP_C M4 bus → M5
    outp_port_y = (q3_ys[0] + q3_ys[3]) / 2 + col_dy
    via_n(lna, inp_bus_x, outp_port_y, 'M4', 'Via4', 'M5')
    lna.shapes(ly['M5']).insert(pya.Box(
        um(inp_bus_x - port_pad/2), um(outp_port_y - port_pad/2),
        um(inp_bus_x + port_pad/2), um(outp_port_y + port_pad/2)))

    # OUTN port: tap OUTN_C M4 bus → M5
    via_n(lna, inn_bus_x, outp_port_y, 'M4', 'Via4', 'M5')
    lna.shapes(ly['M5']).insert(pya.Box(
        um(inn_bus_x - port_pad/2), um(outp_port_y - port_pad/2),
        um(inn_bus_x + port_pad/2), um(outp_port_y + port_pad/2)))

    # VCB port: tap VCB M5 bus at center
    vcb_port_y = (q3_ys[0] + q3_ys[3]) / 2 + bas_dy
    lna.shapes(ly['M5']).insert(pya.Box(
        um(cx - port_pad/2), um(vcb_port_y - port_pad/2),
        um(cx + port_pad/2), um(vcb_port_y + port_pad/2)))
    lna.shapes(ly['M5']).insert(pya.Box(
        um(lx - 0.25), um(vcb_port_y - 0.25), um(cx + port_pad/2), um(vcb_port_y + 0.25)))

    # ----------------------------------------------------------------
    # Additional devices for LVS (matching RXAMP_77GD.sch)
    # ----------------------------------------------------------------
    # Q37: Bias transistor (Nx=1)
    if npn_idx is not None:
        lna.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - 40), um(cy - 80))))

    # R29: Emitter degeneration (rsil, w=7, l=38.8, m=4) — placed below tail node
    if rppd_idx is not None:
        lna.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx - 0.45), um(cy - 50))))
        # R30: Bias resistor for B35&36
        lna.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx + 20), um(cy + 70))))
        # R31: Bias resistor (GND)
        lna.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx + 30), um(cy + 70))))
        # R32: Input bias (BIAS6)
        lna.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx - 40), um(cy - 70))))

    # C55/C56: Output AC coupling caps (4x4µm cmim)
    if cmim_idx is not None:
        lna.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx - 55), um(cy + 80))))
        lna.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx + 47), um(cy + 80))))
        # C57-C61: Decoupling caps (large cmim, placed in right region)
        for i in range(5):
            lna.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(CELL_W - 40), um(50 + i * 20))))

    # BIAS6 port
    bias6_x = cx - 40 + 3.9
    bias6_y = cy - 80 + 1.775
    via_n(lna, bias6_x, bias6_y, 'M1', 'Via1', 'M2')
    via_n(lna, bias6_x, bias6_y, 'M2', 'Via2', 'M3')
    via_n(lna, bias6_x, bias6_y, 'M3', 'Via3', 'M4')
    via_n(lna, bias6_x, bias6_y, 'M4', 'Via4', 'M5')
    lna.shapes(ly['M5']).insert(pya.Box(
        um(bias6_x - port_pad/2), um(bias6_y - port_pad/2),
        um(bias6_x + port_pad/2), um(bias6_y + port_pad/2)))

    # Port labels (matched to xschem RXAMP_77GD.sch for LVS)
    lna.shapes(ly['M5']).insert(pya.Text("INP", pya.Trans(um(inp_bus_x), um(inp_port_y))))
    lna.shapes(ly['M5']).insert(pya.Text("INN", pya.Trans(um(inn_bus_x), um(inp_port_y))))
    lna.shapes(ly['M5']).insert(pya.Text("OUTP", pya.Trans(um(inp_bus_x), um(outp_port_y))))
    lna.shapes(ly['M5']).insert(pya.Text("OUTN", pya.Trans(um(inn_bus_x), um(outp_port_y))))
    lna.shapes(ly['M5']).insert(pya.Text("2V4", pya.Trans(um(cx), um(vcc_y))))
    lna.shapes(ly['M5']).insert(pya.Text("GND", pya.Trans(um(tail_port_x), um(tail_port_y))))
    lna.shapes(ly['M5']).insert(pya.Text("B35&36", pya.Trans(um(cx), um(vcb_port_y))))
    lna.shapes(ly['M5']).insert(pya.Text("BIAS6", pya.Trans(um(bias6_x), um(bias6_y))))

    if ext_layout is None:
        output = "/home/bthomas3/Videos/77GHz_phased_array/layout/LNA_77G_XTOR.gds"
        layout.write(output)
        print(f"\nLNA layout: {output}")
        print(f"Cell size: {CELL_W} x {CELL_H} um")
        print(f"Devices: 16x npn13G2L + 2x cmim + 1x rppd")


if __name__ == "__main__":
    main()
