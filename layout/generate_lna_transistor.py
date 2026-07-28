"""
77 GHz LNA (RXAMP_77GD) — Transistor-Level Layout
Differential cascode with CPW transmission lines on IHP SG13G2
"""

import sys
sys.path.insert(0, "/home/bthomas3/Videos/77GHz_phased_array/layout")
from pdk_devices import create_rppd
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

    # (Caps and resistors placed in routing section below)

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
    # Additional devices for LVS (matching LNA_77G_XTOR.spice)
    # ----------------------------------------------------------------
    # Q37: Bias transistor (Nx=1), C=GND, B=GND, E=net12
    q37_x = cx - 40
    q37_y = cy - 100
    if npn_idx is not None:
        lna.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q37_x), um(q37_y))))

    # --- Parameterized rppd resistors ---
    # Helper to connect parallel stripes' M1 pads
    def connect_rppd_stripes(res_x, res_y, w_um, l_um, m):
        """Draw M1 wires connecting all parallel stripe P and M pads"""
        if m <= 1:
            return
        total_w = m * w_um + (m - 1) * 0.5
        # P pad Y range: res_y + l_um to res_y + l_um + 0.3
        p_y1 = res_y + l_um
        p_y2 = res_y + l_um + 0.3
        # M pad Y range: res_y - 0.3 to res_y
        m_y1 = res_y - 0.3
        m_y2 = res_y
        # M1 wire spanning all stripes
        lna.shapes(ly['M1']).insert(pya.Box(
            um(res_x), um(p_y1), um(res_x + total_w), um(p_y2)))
        lna.shapes(ly['M1']).insert(pya.Box(
            um(res_x), um(m_y1), um(res_x + total_w), um(m_y2)))

    # R29: w=7.0u, l=38.8u, m=4, P=net3, M=GND
    r29_x = cx - 20.0
    r29_y = cy - 160.0
    r29_pins = create_rppd(lna, layout, r29_x, r29_y, 7.0, 38.8, m=4)
    connect_rppd_stripes(r29_x, r29_y, 7.0, 38.8, 4)

    # R30: w=3.0u, l=18.23u, m=2, P=2V4, M=B35&36
    r30_x = cx + 40.0
    r30_y = cy + 100.0
    r30_pins = create_rppd(lna, layout, r30_x, r30_y, 3.0, 18.23, m=2)
    connect_rppd_stripes(r30_x, r30_y, 3.0, 18.23, 2)

    # R31: w=3.0u, l=18.23u, m=1, P=B35&36, M=GND
    r31_x = cx + 55.0
    r31_y = cy + 100.0
    r31_pins = create_rppd(lna, layout, r31_x, r31_y, 3.0, 18.23, m=1)

    # R32: w=3.0u, l=18.23u, m=2, P=GND, M=GND (dummy)
    r32_x = cx + 70.0
    r32_y = cy + 100.0
    r32_pins = create_rppd(lna, layout, r32_x, r32_y, 3.0, 18.23, m=2)
    connect_rppd_stripes(r32_x, r32_y, 3.0, 18.23, 2)

    # R33: w=2.5u, l=10.53u, m=14, P=net12, M=GND
    r33_x = cx - 60.0
    r33_y = cy - 130.0
    r33_pins = create_rppd(lna, layout, r33_x, r33_y, 2.5, 10.53, m=14)
    connect_rppd_stripes(r33_x, r33_y, 2.5, 10.53, 14)

    # --- Caps: 9 cmim (7u x 7u) ---
    # cmim pins: c0 on M5 at cell_origin + (3.495, 3.495), c1 on TM1 at same center
    # C53: c0=net1(Q33.B), c1=INP
    c53_x = cx - 55.0
    c53_y = cy - 60.0
    # C54: c0=GND, c1=net2(Q34.B)
    c54_x = cx + 47.0
    c54_y = cy - 60.0
    # C55: c0=OUTP, c1=net6(Q35.C)
    c55_x = cx - 55.0
    c55_y = cy + 80.0
    # C56: c0=2V4, c1=net7(Q36.C)
    c56_x = cx + 47.0
    c56_y = cy + 80.0
    # C57-C61: VCC bypass chain
    c57_61_x = CELL_W - 40.0
    c57_61_ys = [50.0 + i * 20.0 for i in range(5)]

    if cmim_idx is not None:
        lna.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(c53_x), um(c53_y))))
        lna.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(c54_x), um(c54_y))))
        lna.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(c55_x), um(c55_y))))
        lna.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(c56_x), um(c56_y))))
        for i in range(5):
            lna.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(c57_61_x), um(c57_61_ys[i]))))

    # cmim pin center offset from cell origin
    cmim_c0_dx = 3.495  # c0 on M5
    cmim_c0_dy = 3.495
    # c1 on TM1 same center

    # ----------------------------------------------------------------
    # ROUTING: Connect resistors, caps, Q37 to internal nets
    # ----------------------------------------------------------------
    # NOTE on create_rppd pin convention:
    #   'P' = top M1 pad (high Y), 'M' = bottom M1 pad (low Y)

    # Helper: M1 pad to M5 via stack
    def via_m1_to_m5(x, y):
        via_n(lna, x, y, 'M1', 'Via1', 'M2')
        via_n(lna, x, y, 'M2', 'Via2', 'M3')
        via_n(lna, x, y, 'M3', 'Via3', 'M4')
        via_n(lna, x, y, 'M4', 'Via4', 'M5')

    def via_m1_to_m4(x, y):
        via_n(lna, x, y, 'M1', 'Via1', 'M2')
        via_n(lna, x, y, 'M2', 'Via2', 'M3')
        via_n(lna, x, y, 'M3', 'Via3', 'M4')

    def via_m4_to_m5(x, y):
        via_n(lna, x, y, 'M4', 'Via4', 'M5')

    def m5_wire(x1, y1, x2, y2, w=0.5):
        lna.shapes(ly['M5']).insert(pya.Box(
            um(min(x1,x2)-w/2), um(min(y1,y2)-w/2),
            um(max(x1,x2)+w/2), um(max(y1,y2)+w/2)))

    def m4_wire(x1, y1, x2, y2, w=0.5):
        lna.shapes(ly['M4']).insert(pya.Box(
            um(min(x1,x2)-w/2), um(min(y1,y2)-w/2),
            um(max(x1,x2)+w/2), um(max(y1,y2)+w/2)))

    def m3_wire(x1, y1, x2, y2, w=0.5):
        lna.shapes(ly['M3']).insert(pya.Box(
            um(min(x1,x2)-w/2), um(min(y1,y2)-w/2),
            um(max(x1,x2)+w/2), um(max(y1,y2)+w/2)))

    def m1_wire(x1, y1, x2, y2, w=0.5):
        lna.shapes(ly['M1']).insert(pya.Box(
            um(min(x1,x2)-w/2), um(min(y1,y2)-w/2),
            um(max(x1,x2)+w/2), um(max(y1,y2)+w/2)))

    # --- R29: P=net3 (tail emitter bus), M=GND ---
    # R29.P connects to TAIL (M4 bus). Bring R29.P up to M4, connect to tail bus.
    r29_px, r29_py = r29_pins['P']
    r29_mx, r29_my = r29_pins['M']
    via_m1_to_m4(r29_px, r29_py)
    # Connect R29.P to tail bus: tail bus is at tail_y on M4 between tail_vl and tail_vr
    m4_wire(r29_px, r29_py, r29_px, tail_y)
    m4_wire(r29_px, tail_y, tail_vl, tail_y)
    # R29.M = GND: bring to M5 GND plane or ground pad
    # Use a GND bus at bottom of cell on M5
    gnd_y = 20.0
    via_m1_to_m5(r29_mx, r29_my)
    m5_wire(r29_mx, r29_my, r29_mx, gnd_y)

    # --- R33: P=net12 (Q37.E), M=GND ---
    r33_px, r33_py = r33_pins['P']
    r33_mx, r33_my = r33_pins['M']
    # Q37 emitter at (q37_x + 3.9, q37_y + 3.6) on M2
    q37_ex = q37_x + pcx
    q37_ey = q37_y + emi_dy
    # Connect Q37.E (M2) to R33.P (M1) via M3
    via_n(lna, q37_ex, q37_ey, 'M2', 'Via2', 'M3')
    via_m1_to_m4(r33_px, r33_py)
    via_n(lna, q37_ex, q37_ey, 'M3', 'Via3', 'M4')
    m4_wire(r33_px, r33_py, q37_ex, r33_py)
    m4_wire(q37_ex, r33_py, q37_ex, q37_ey)
    # R33.M = GND
    via_m1_to_m5(r33_mx, r33_my)
    m5_wire(r33_mx, r33_my, r33_mx, gnd_y)

    # --- Q37: C=GND, B=GND ---
    q37_cx = q37_x + pcx
    q37_cy_col = q37_y + col_dy  # collector on M1
    q37_by = q37_y + bas_dy      # base on M1
    # Q37 collector to GND
    via_m1_to_m5(q37_cx, q37_cy_col)
    m5_wire(q37_cx, q37_cy_col, q37_cx, gnd_y)
    # Q37 base to GND
    via_m1_to_m5(q37_cx, q37_by)
    m5_wire(q37_cx, q37_by, q37_cx, gnd_y)

    # --- R30: P=2V4, M=B35&36 ---
    r30_px, r30_py = r30_pins['P']
    r30_mx, r30_my = r30_pins['M']
    # R30.P to VCC (2V4) rail on M3 at vcc_y
    via_m1_to_m4(r30_px, r30_py)
    via_n(lna, r30_px, r30_py, 'M4', 'Via4', 'M5')
    # Connect to VCC on M5 (VCC rail is on M3; bring up)
    # Actually VCC rail is M3 at vcc_y. Let's connect on M3:
    via_n(lna, r30_px, r30_py, 'M1', 'Via1', 'M2')
    via_n(lna, r30_px, r30_py, 'M2', 'Via2', 'M3')
    m3_wire(r30_px, r30_py, r30_px, vcc_y)
    # R30.M to B35&36 (VCB bus on M5)
    via_m1_to_m5(r30_mx, r30_my)
    m5_wire(r30_mx, r30_my, r30_mx, vcb_y)
    m5_wire(r30_mx, vcb_y, lx, vcb_y)  # connect to VCB M5 bus

    # --- R31: P=B35&36, M=GND ---
    r31_px, r31_py = r31_pins['P']
    r31_mx, r31_my = r31_pins['M']
    via_m1_to_m5(r31_px, r31_py)
    m5_wire(r31_px, r31_py, r31_px, vcb_y)
    m5_wire(r31_px, vcb_y, r30_mx, vcb_y)  # to VCB bus
    # R31.M = GND
    via_m1_to_m5(r31_mx, r31_my)
    m5_wire(r31_mx, r31_my, r31_mx, gnd_y)

    # --- R32: P=GND, M=GND (dummy) ---
    r32_px, r32_py = r32_pins['P']
    r32_mx, r32_my = r32_pins['M']
    via_m1_to_m5(r32_px, r32_py)
    m5_wire(r32_px, r32_py, r32_px, gnd_y)
    via_m1_to_m5(r32_mx, r32_my)
    m5_wire(r32_mx, r32_my, r32_mx, gnd_y)

    # --- GND bus on M5 at bottom ---
    lna.shapes(ly['M5']).insert(pya.Box(um(10), um(gnd_y - 3), um(CELL_W - 10), um(gnd_y + 3)))

    # --- Cap routing ---
    # C53: c0(M5)=net1(Q33.B bus on M4→M5), c1(TM1)=INP
    c53_c0x = c53_x + cmim_c0_dx
    c53_c0y = c53_y + cmim_c0_dy
    # Connect C53.c0 (M5) to Q1 base bus (INP_B on M4 at inp_bus_x)
    # Bring INP_B M4 bus up to M5 at a point, then wire on M5 to C53.c0
    inp_b_m5_y = inp_port_y  # already have M5 pad at inp_bus_x
    m5_wire(inp_bus_x, inp_b_m5_y, c53_c0x, inp_b_m5_y)
    m5_wire(c53_c0x, inp_b_m5_y, c53_c0x, c53_c0y)

    # C54: c0(M5)=GND, c1(TM1)=net2(Q34.B)
    c54_c0x = c54_x + cmim_c0_dx
    c54_c0y = c54_y + cmim_c0_dy
    # c0 to GND
    m5_wire(c54_c0x, c54_c0y, c54_c0x, gnd_y)
    # c1(TM1) to Q2 base bus: INN_B M4→M5
    # c1 on TM1 at same center. Need TM1 wire to INN_B M5.
    inn_b_m5_y = inp_port_y
    c54_c1x = c54_x + cmim_c0_dx  # same center
    c54_c1y = c54_y + cmim_c0_dy
    # TM1 wire from c54 to a via stack down to M5, then to INN_B
    # Actually c1 is on TM1. We need to bring INN_B up to TM1, or bring c1 down.
    # Use TopVia1 (M5→TM1) at inn_bus_x, inp_port_y
    via_n(lna, inn_bus_x, inp_port_y, 'M5', 'TopVia1', 'TM1')
    lna.shapes(ly['TM1']).insert(pya.Box(
        um(min(inn_bus_x, c54_c1x)-0.25), um(min(inp_port_y, c54_c1y)-0.25),
        um(max(inn_bus_x, c54_c1x)+0.25), um(inp_port_y+0.25)))
    lna.shapes(ly['TM1']).insert(pya.Box(
        um(c54_c1x-0.25), um(min(inp_port_y, c54_c1y)-0.25),
        um(c54_c1x+0.25), um(max(inp_port_y, c54_c1y)+0.25)))

    # C55: c0(M5)=OUTP, c1(TM1)=net6(Q35.C)
    c55_c0x = c55_x + cmim_c0_dx
    c55_c0y = c55_y + cmim_c0_dy
    # Connect c0(M5) to OUTP (which is on M4 at inp_bus_x promoted to M5)
    m5_wire(inp_bus_x, outp_port_y, c55_c0x, outp_port_y)
    m5_wire(c55_c0x, outp_port_y, c55_c0x, c55_c0y)
    # c1(TM1) = net6 = Q35.C bus on M4. Need via M4→M5→TM1
    via_n(lna, inp_bus_x, outp_port_y, 'M5', 'TopVia1', 'TM1')
    # Actually c1 needs to connect to net6 not OUTP. net6 = Q35.C = OUTP_C bus.
    # Since c0=OUTP and c1=net6, and OUTP IS net6 from the cap's perspective...
    # Wait: XC55 OUTP net6 cap_cmim → c0=OUTP, c1=net6. But net6=Q35.C.
    # OUTP is the PORT on net6. So OUTP=net6. c0 and c1 are both on net6!? No.
    # Actually in the spice: XC55 OUTP net6 → these are two different nets separated by the cap.
    # OUTP is the external port, net6 is Q35.C. The cap couples them.
    # So c0(M5)=OUTP port, c1(TM1)=net6=Q35.C collector bus.
    # The Q35.C bus is on M4 at inp_bus_x. Bring it to TM1:
    c55_c1x = c55_x + cmim_c0_dx
    c55_c1y = c55_y + cmim_c0_dy
    outp_c_via_x = inp_bus_x - 3.0  # offset to avoid shorting c0
    via_m1_to_m5(outp_c_via_x, outp_port_y)
    via_n(lna, outp_c_via_x, outp_port_y, 'M5', 'TopVia1', 'TM1')
    m4_wire(inp_bus_x, outp_port_y, outp_c_via_x, outp_port_y)
    lna.shapes(ly['TM1']).insert(pya.Box(
        um(min(outp_c_via_x, c55_c1x)-0.25), um(min(outp_port_y, c55_c1y)-0.25),
        um(max(outp_c_via_x, c55_c1x)+0.25), um(outp_port_y+0.25)))
    lna.shapes(ly['TM1']).insert(pya.Box(
        um(c55_c1x-0.25), um(min(outp_port_y, c55_c1y)-0.25),
        um(c55_c1x+0.25), um(max(outp_port_y, c55_c1y)+0.25)))

    # C56: c0(M5)=2V4, c1(TM1)=net7(Q36.C)
    c56_c0x = c56_x + cmim_c0_dx
    c56_c0y = c56_y + cmim_c0_dy
    # c0 to VCC rail via M5
    m5_wire(c56_c0x, c56_c0y, c56_c0x, vcc_y)
    # Connect VCC M3 rail to M5 at c56_c0x
    via_n(lna, c56_c0x, vcc_y, 'M3', 'Via3', 'M4')
    via_n(lna, c56_c0x, vcc_y, 'M4', 'Via4', 'M5')
    # c1(TM1) = net7 = Q36.C = OUTN_C bus on M4 at inn_bus_x
    c56_c1x = c56_x + cmim_c0_dx
    c56_c1y = c56_y + cmim_c0_dy
    outn_c_via_x = inn_bus_x + 3.0
    via_m1_to_m5(outn_c_via_x, outp_port_y)
    via_n(lna, outn_c_via_x, outp_port_y, 'M5', 'TopVia1', 'TM1')
    m4_wire(inn_bus_x, outp_port_y, outn_c_via_x, outp_port_y)
    lna.shapes(ly['TM1']).insert(pya.Box(
        um(min(outn_c_via_x, c56_c1x)-0.25), um(min(outp_port_y, c56_c1y)-0.25),
        um(max(outn_c_via_x, c56_c1x)+0.25), um(outp_port_y+0.25)))
    lna.shapes(ly['TM1']).insert(pya.Box(
        um(c56_c1x-0.25), um(min(outp_port_y, c56_c1y)-0.25),
        um(c56_c1x+0.25), um(max(outp_port_y, c56_c1y)+0.25)))

    # C57-C61: VCC bypass chain on M5 (c0) and TM1 (c1)
    # C57: c0=2V4, c1=net8; C58: c0=net8, c1=net9; ... C61: c0=net11, c1=GND
    # IMPORTANT: Route VCC/GND connections HORIZONTALLY first to avoid
    # vertical M5 wires passing through other caps' M5 plates.
    bypass_route_x = c57_61_x - 5.0  # x=255, clear of cap M5 (259.4-267.6)

    # Connect c0 of C57 to VCC: go left on M5 to bypass_route_x, then up to VCC
    c57_c0x = c57_61_x + cmim_c0_dx
    c57_c0y = c57_61_ys[0] + cmim_c0_dy
    m5_wire(c57_c0x, c57_c0y, bypass_route_x, c57_c0y)
    m5_wire(bypass_route_x, c57_c0y, bypass_route_x, vcc_y)
    via_n(lna, bypass_route_x, vcc_y, 'M3', 'Via3', 'M4')
    via_n(lna, bypass_route_x, vcc_y, 'M4', 'Via4', 'M5')

    # Chain: c1 of Cn connects to c0 of Cn+1 (TM1 to M5 of next)
    # Route via bypass_route_x to avoid passing through other caps
    for i in range(4):  # C57-C60, connect c1[i] to c0[i+1]
        c1x = c57_61_x + cmim_c0_dx
        c1y = c57_61_ys[i] + cmim_c0_dy
        c0_next_x = c57_61_x + cmim_c0_dx
        c0_next_y = c57_61_ys[i+1] + cmim_c0_dy
        # Use TopVia1 at bypass_route_x between the two caps
        mid_y = (c1y + c0_next_y) / 2
        via_n(lna, bypass_route_x, mid_y, 'M5', 'TopVia1', 'TM1')
        # TM1 wire from c1 to via
        lna.shapes(ly['TM1']).insert(pya.Box(
            um(min(c1x, bypass_route_x)-0.25), um(min(c1y, mid_y)-0.25),
            um(max(c1x, bypass_route_x)+0.25), um(c1y+0.25)))
        lna.shapes(ly['TM1']).insert(pya.Box(
            um(bypass_route_x-0.25), um(min(c1y, mid_y)-0.25),
            um(bypass_route_x+0.25), um(max(c1y, mid_y)+0.25)))
        # M5 wire from via to c0_next
        m5_wire(bypass_route_x, mid_y, bypass_route_x, c0_next_y)
        m5_wire(bypass_route_x, c0_next_y, c0_next_x, c0_next_y)

    # C61 c1 to GND: route left then down
    c61_c1x = c57_61_x + cmim_c0_dx
    c61_c1y = c57_61_ys[4] + cmim_c0_dy
    via_n(lna, bypass_route_x, c61_c1y, 'M5', 'TopVia1', 'TM1')
    lna.shapes(ly['TM1']).insert(pya.Box(
        um(min(c61_c1x, bypass_route_x)-0.25), um(c61_c1y-0.25),
        um(max(c61_c1x, bypass_route_x)+0.25), um(c61_c1y+0.25)))
    m5_wire(bypass_route_x, c61_c1y, bypass_route_x, gnd_y)

    # C53 c1 (TM1) = INP port: leave as external TM1 pad
    c53_c1x = c53_x + cmim_c0_dx
    c53_c1y = c53_y + cmim_c0_dy
    # INP is already a port label on M5. Need to NOT short c0 and c1.
    # c0 connects to net1 on M5, c1 on TM1 is the INP port.
    # Add INP label on TM1
    lna.shapes(ly['TM1']).insert(pya.Text("INP", pya.Trans(um(c53_c1x), um(c53_c1y))))

    # --- OUTP port: separate from net6 ---
    # OUTP is c0 of C55 on M5. It's a different net from net6 (which is c1 on TM1).
    # So OUTP port should be at c55_c0x, c55_c0y on M5.

    # --- OUTN port: c0 of C56 is 2V4, not OUTN ---
    # Wait, looking at schematic again: XC56 2V4 net7 → OUTN doesn't appear!
    # The task description says OUTN should be there. Let me check ports:
    # Ports: 2V4 INP INN GND sub! OUTP OUTN, B35&36, BIAS6
    # OUTP = first pin of C55. OUTN = ... not explicitly connected to a device?
    # Actually OUTN might just be net7. But the spice shows C56 c0=2V4, not OUTN.
    # Let me just place port labels matching the subckt.

    # === PORT LABELS ===
    # Place port labels on M5 (or TM1 for through-cap ports)
    # Clear previous approach - use definitive port positions
    # 2V4: VCC rail
    lna.shapes(ly['M5']).insert(pya.Text("2V4", pya.Trans(um(cx), um(vcc_y))))
    # GND: GND bus
    lna.shapes(ly['M5']).insert(pya.Text("GND", pya.Trans(um(cx), um(gnd_y))))
    # INP: on TM1 at C53 c1
    # (already added above)
    # INN: on M5 connecting to Q2 bases (since C54 c1=net2 on TM1, and port INN...
    # Actually INN is not in the device netlist! The .subckt line has INN but no device connects to it.
    # This likely means INN connects to net2 directly (maybe through C54 differently).
    # For now, add INN on TM1 at C54 c1 position:
    lna.shapes(ly['TM1']).insert(pya.Text("INN", pya.Trans(um(c54_c1x), um(c54_c1y))))
    # OUTP: on M5 at C55 c0
    lna.shapes(ly['M5']).insert(pya.Text("OUTP", pya.Trans(um(c55_c0x), um(c55_c0y))))
    # OUTN: on M5... C56 c0=2V4. OUTN must be somewhere else.
    # Looking at the schematic, OUTN likely = net7 after the cap. But spice shows no OUTN device connection.
    # For LVS, if OUTN is a port on net7, and net7 = Q36.C, then OUTN should label net7.
    # Actually the task says ".subckt LNA_77G_XTOR 2V4 INP INN GND sub! OUTP OUTN"
    # But looking at spice: OUTP appears in C55. OUTN doesn't appear anywhere!
    # Unless the commented subckt definition implies OUTN = some net. Let me just skip OUTN port for now.
    # Actually re-reading: the task says C56: "actually OUTN" - so maybe the spice is wrong and c0 should be OUTN.
    # But since we're matching the spice golden, c0=2V4. So C56 c0 connects to VCC.
    # OUTN could be a floating port or equal to net7. For LVS matching, we need OUTN in layout = OUTN in spice.
    # Since OUTN doesn't appear in the netlist, it might be an unused port. Skip for now.
    # B35&36:
    lna.shapes(ly['M5']).insert(pya.Text("B35&36", pya.Trans(um(cx), um(vcb_port_y))))
    # BIAS6: Q37 area - but BIAS6 isn't in the spice netlist either...
    # Only ports in the spice: 2V4, INP, INN, GND, sub!, OUTP, OUTN, B35&36, BIAS6
    # BIAS6 isn't connected to anything in the netlist. It might be net12.
    # Actually looking again: BIAS6 is an iopin but never used. Skip or add as floating.

    if ext_layout is None:
        output = "/home/bthomas3/Videos/77GHz_phased_array/layout/LNA_77G_XTOR.gds"
        layout.write(output)
        print(f"\nLNA layout: {output}")
        print(f"Cell size: {CELL_W} x {CELL_H} um")
        print(f"Devices: 17x npn13G2L + 5x rppd + 9x cmim")


if __name__ == "__main__":
    main()
