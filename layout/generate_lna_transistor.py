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
    #   'P' = top M1 pad (high Y) → LVS extracts as "M"
    #   'M' = bottom M1 pad (low Y) → LVS extracts as "P"
    # So: schematic P → code['M'] (bottom), schematic M → code['P'] (top)

    # Wire helpers
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

    def m2_wire(x1, y1, x2, y2, w=0.5):
        lna.shapes(ly['M2']).insert(pya.Box(
            um(min(x1,x2)-w/2), um(min(y1,y2)-w/2),
            um(max(x1,x2)+w/2), um(max(y1,y2)+w/2)))

    def m1_wire(x1, y1, x2, y2, w=0.5):
        lna.shapes(ly['M1']).insert(pya.Box(
            um(min(x1,x2)-w/2), um(min(y1,y2)-w/2),
            um(max(x1,x2)+w/2), um(max(y1,y2)+w/2)))

    def via_m1_to_m3(x, y):
        via_n(lna, x, y, 'M1', 'Via1', 'M2')
        via_n(lna, x, y, 'M2', 'Via2', 'M3')

    def via_m2_to_m3(x, y):
        via_n(lna, x, y, 'M2', 'Via2', 'M3')

    def via_m1_to_m4(x, y):
        via_n(lna, x, y, 'M1', 'Via1', 'M2')
        via_n(lna, x, y, 'M2', 'Via2', 'M3')
        via_n(lna, x, y, 'M3', 'Via3', 'M4')

    def via_m1_to_m5(x, y):
        via_n(lna, x, y, 'M1', 'Via1', 'M2')
        via_n(lna, x, y, 'M2', 'Via2', 'M3')
        via_n(lna, x, y, 'M3', 'Via3', 'M4')
        via_n(lna, x, y, 'M4', 'Via4', 'M5')

    # --- GND bus on M5 at bottom ---
    gnd_y = 20.0
    lna.shapes(ly['M5']).insert(pya.Box(um(10), um(gnd_y - 3), um(CELL_W - 10), um(gnd_y + 3)))

    # === M4 VERTICAL TRACK ASSIGNMENTS (all at safe X > 166.4, clear of existing M4) ===
    # Existing M4: INP_B at x=121.2, TAIL verticals at 134.1/165.9, INN_B at 178.8
    # TAIL horizontal at y=248.6 from x=134.1 to 165.9 (must not cross!)
    gnd_trk_x = 240.0    # GND (far right, clear of all transistor/cap routing)
    vcb_trk_x = 244.0    # VCB (B35&36)
    net12_trk_x = 248.0  # net12 (Q37.E ↔ R33)
    vcc_trk_x = 252.0    # VCC (2V4)

    # --- GND M4 vertical: from gnd_y to 370 ---
    # This is safe at x=200 (existing TAIL horizontal only spans x=134.1-165.9)
    gnd_m4_top = 370.0
    m4_wire(gnd_trk_x, gnd_y, gnd_trk_x, gnd_m4_top)
    # Connect GND M4 track to GND M5 bus at bottom
    via_n(lna, gnd_trk_x, gnd_y, 'M4', 'Via4', 'M5')

    # --- VCB M4 vertical: from vcb_y up to R30.P connection (~370) ---
    # R30.P connects at r30_py+2, R31.M connects at r31 M pin Y (~349.85)
    # VCB bus at vcb_y (~296.8). Track spans full range.
    vcb_m4_bot = vcb_y - 1.0
    vcb_m4_top = 372.0  # above R30.P route point
    m4_wire(vcb_trk_x, vcb_m4_bot, vcb_trk_x, vcb_m4_top)
    # Connect VCB M4 track to VCB M5 bus at vcb_y
    via_n(lna, vcb_trk_x, vcb_y, 'M4', 'Via4', 'M5')
    # M5 stub from vcb_trk_x to existing VCB M5 bus (which runs from lx to rx)
    m5_wire(rx, vcb_y, vcb_trk_x, vcb_y)

    # --- net12 M4 vertical: from R33 area up to Q37.E ---
    q37_ex = q37_x + pcx     # 113.9
    q37_ey = q37_y + emi_dy  # 153.6
    r33_px, r33_py = r33_pins['P']  # top, GND (schematic M)
    r33_mx, r33_my = r33_pins['M']  # bottom, net12 (schematic P)
    net12_m4_bot = r33_my - 1.0
    net12_m4_top = q37_ey + 1.0
    m4_wire(net12_trk_x, net12_m4_bot, net12_trk_x, net12_m4_top)

    # --- R29 pin extraction ---
    r29_px, r29_py = r29_pins['P']  # top, GND (schematic M)
    r29_mx, r29_my = r29_pins['M']  # bottom, tail/net3 (schematic P)

    # --- R29.M (tail): direct M4 vertical to existing TAIL bus (no track extension) ---
    via_m1_to_m4(r29_mx, r29_my)
    m4_wire(r29_mx, r29_my, r29_mx, tail_y)
    # Short M4 horizontal to connect to tail_vl
    m4_wire(r29_mx, tail_y, tail_vl, tail_y)

    # --- VCC M4 vertical: from R30 area up to vcc_y ---
    r30_px, r30_py = r30_pins['P']  # top, VCB (schematic M)
    r30_mx, r30_my = r30_pins['M']  # bottom, VCC (schematic P)
    vcc_m4_bot = r30_my - 1.0
    m4_wire(vcc_trk_x, vcc_m4_bot, vcc_trk_x, vcc_y)
    # Connect VCC M4 track to VCC M3 rail at vcc_y
    via_n(lna, vcc_trk_x, vcc_y, 'M3', 'Via3', 'M4')

    # ================================================================
    # Q37 ROUTING: C=GND, B=GND, E=net12
    # ================================================================
    q37_cx = q37_x + pcx      # 113.9
    q37_cy_col = q37_y + col_dy  # 155.425 (collector on M1)
    q37_by = q37_y + bas_dy      # 151.775 (base on M1)

    # Q37.B and Q37.C: ESCAPE ROUTING to avoid M2 pad shorting to emitter M2
    # Route M1 LEFT to x=100 before via stack (14um from emitter M2 at x=113.9)
    q37_esc_x = 100.0
    # Q37.C: M1 escape left, then via stack at escape point
    m1_wire(q37_cx, q37_cy_col, q37_esc_x, q37_cy_col)
    via_m1_to_m3(q37_esc_x, q37_cy_col)
    m3_wire(q37_esc_x, q37_cy_col, gnd_trk_x, q37_cy_col)
    via_n(lna, gnd_trk_x, q37_cy_col, 'M3', 'Via3', 'M4')
    # Q37.B: M1 escape left, then via stack
    m1_wire(q37_cx, q37_by, q37_esc_x, q37_by)
    via_m1_to_m3(q37_esc_x, q37_by)
    m3_wire(q37_esc_x, q37_by, gnd_trk_x, q37_by)
    via_n(lna, gnd_trk_x, q37_by, 'M3', 'Via3', 'M4')

    # Q37.E (M2) → net12 track
    via_m2_to_m3(q37_ex, q37_ey)
    m3_wire(q37_ex, q37_ey, net12_trk_x, q37_ey)
    via_n(lna, net12_trk_x, q37_ey, 'M3', 'Via3', 'M4')

    # ================================================================
    # R29 ROUTING: code['M'](bottom)=tail/net3, code['P'](top)=GND
    # ================================================================
    # R29.M already routed above (direct M4 to tail bus)

    # R29.P (top) → GND via M3 horizontal to gnd_trk_x
    via_m1_to_m3(r29_px, r29_py)
    m3_wire(r29_px, r29_py, gnd_trk_x, r29_py)
    via_n(lna, gnd_trk_x, r29_py, 'M3', 'Via3', 'M4')

    # ================================================================
    # R33 ROUTING: code['M'](bottom)=net12/Q37.E, code['P'](top)=GND
    # ================================================================
    # R33.M (bottom) → net12 track
    via_m1_to_m3(r33_mx, r33_my)
    m3_wire(r33_mx, r33_my, net12_trk_x, r33_my)
    via_n(lna, net12_trk_x, r33_my, 'M3', 'Via3', 'M4')

    # R33.P (top) → GND track
    via_m1_to_m3(r33_px, r33_py)
    m3_wire(r33_px, r33_py, gnd_trk_x, r33_py)
    via_n(lna, gnd_trk_x, r33_py, 'M3', 'Via3', 'M4')

    # ================================================================
    # R30 ROUTING: code['M'](bottom)=VCC/2V4, code['P'](top)=VCB/B35&36
    # ================================================================
    # R30.M (bottom) → VCC: M1 escape left, then M3 vertical to VCC rail
    r30_m_esc_x = 185.0
    m1_wire(r30_mx, r30_my, r30_m_esc_x, r30_my)
    via_m1_to_m3(r30_m_esc_x, r30_my)
    m3_wire(r30_m_esc_x, r30_my, r30_m_esc_x, vcc_y)

    # R30.P (top) → VCB track: OFFSET Y to y=370 to avoid crossing GND wires at r30_py
    r30_p_route_y = r30_py + 2.0  # stagger to avoid crossing R31.P/R32.P GND wires
    via_n(lna, r30_px, r30_py, 'M1', 'Via1', 'M2')
    m2_wire(r30_px, r30_py, r30_px, r30_p_route_y)
    via_n(lna, r30_px, r30_p_route_y, 'M2', 'Via2', 'M3')
    m3_wire(r30_px, r30_p_route_y, vcb_trk_x, r30_p_route_y)
    via_n(lna, vcb_trk_x, r30_p_route_y, 'M3', 'Via3', 'M4')

    # ================================================================
    # R31 ROUTING: code['M'](bottom)=VCB/B35&36, code['P'](top)=GND
    # ================================================================
    r31_px, r31_py = r31_pins['P']  # top, GND
    r31_mx, r31_my = r31_pins['M']  # bottom, VCB

    # R31.M (bottom) → VCB track: offset Y to avoid M3 overlap with R30.M at y=349.85
    r31_m_route_y = r31_my - 2.5  # 347.35 (clear of R30.M M3 at 349.85)
    via_n(lna, r31_mx, r31_my, 'M1', 'Via1', 'M2')
    m2_wire(r31_mx, r31_my, r31_mx, r31_m_route_y)
    via_n(lna, r31_mx, r31_m_route_y, 'M2', 'Via2', 'M3')
    m3_wire(r31_mx, r31_m_route_y, vcb_trk_x, r31_m_route_y)
    via_n(lna, vcb_trk_x, r31_m_route_y, 'M3', 'Via3', 'M4')

    # R31.P (top) → GND track (short M3, only from x=206.5 to 200)
    via_m1_to_m3(r31_px, r31_py)
    m3_wire(r31_px, r31_py, gnd_trk_x, r31_py)
    via_n(lna, gnd_trk_x, r31_py, 'M3', 'Via3', 'M4')

    # ================================================================
    # R32 ROUTING: code['M'](bottom)=GND, code['P'](top)=GND
    # ================================================================
    r32_px, r32_py = r32_pins['P']  # top, GND
    r32_mx, r32_my = r32_pins['M']  # bottom, GND

    # R32.M (bottom) → GND track: OFFSET Y to avoid R31.M VCB at y=347.35 and R30.M at y=349.85
    r32_m_route_y = r32_my - 5.0  # 344.85 (clear of both)
    via_n(lna, r32_mx, r32_my, 'M1', 'Via1', 'M2')
    m2_wire(r32_mx, r32_my, r32_mx, r32_m_route_y)
    via_n(lna, r32_mx, r32_m_route_y, 'M2', 'Via2', 'M3')
    m3_wire(r32_mx, r32_m_route_y, gnd_trk_x, r32_m_route_y)
    via_n(lna, gnd_trk_x, r32_m_route_y, 'M3', 'Via3', 'M4')

    # R32.P (top) → GND track: same Y as R31.P (both GND, overlap is OK)
    via_m1_to_m3(r32_px, r32_py)
    m3_wire(r32_px, r32_py, gnd_trk_x, r32_py)
    via_n(lna, gnd_trk_x, r32_py, 'M3', 'Via3', 'M4')

    # ================================================================
    # CAP ROUTING
    # ================================================================
    # C53: c0(M5)=net1(Q1.B bus), c1(TM1)=INP
    c53_c0x = c53_x + cmim_c0_dx
    c53_c0y = c53_y + cmim_c0_dy
    # Connect C53.c0 (M5) to Q1 base bus — touch cap M5 TOP edge from above
    inp_b_m5_y = inp_port_y
    c53_m5_top = c53_y + 7.59
    m5_wire(inp_bus_x, inp_b_m5_y, c53_c0x, inp_b_m5_y)
    m5_wire(c53_c0x, inp_b_m5_y, c53_c0x, c53_m5_top)

    # C54: c0(M5)=GND, c1(TM1)=net2(Q2.B)
    c54_c0x = c54_x + cmim_c0_dx
    c54_c0y = c54_y + cmim_c0_dy
    # c0(M5) to GND: M5 wire touching cap M5 TOP edge (outside MIM), then Via4 above cap
    # Cap M5 top at c54_y + 7.59. Via4 ABOVE cap at c54_y + 9.0
    c54_m5_top = c54_y + 7.59
    c54_via4_y = c54_m5_top + 2.0
    via_n(lna, c54_c0x, c54_via4_y, 'M4', 'Via4', 'M5')
    m5_wire(c54_c0x, c54_m5_top, c54_c0x, c54_via4_y)
    m4_wire(c54_c0x, c54_via4_y, gnd_trk_x, c54_via4_y)
    via_n(lna, gnd_trk_x, c54_via4_y, 'M3', 'Via3', 'M4')

    # C54 c1(TM1) = net2(Q2.B) — use text label (TM1 into MIM breaks cap recognition)
    c54_c1x = c54_x + cmim_c0_dx
    c54_c1y = c54_y + cmim_c0_dy

    # C55: c0(M5)=OUTP, c1(TM1)=net6(Q3.C)
    c55_c0x = c55_x + cmim_c0_dx
    c55_c0y = c55_y + cmim_c0_dy
    c55_m5_bot = c55_y - 0.6  # cap M5 bottom edge
    m5_wire(inp_bus_x, outp_port_y, c55_c0x, outp_port_y)
    m5_wire(c55_c0x, outp_port_y, c55_c0x, c55_m5_bot)
    # c1(TM1) = net6 = Q3.C — text label only (TM1 into MIM breaks cap recognition)
    c55_c1x = c55_x + cmim_c0_dx
    c55_c1y = c55_y + cmim_c0_dy

    # C56: c0(M5)=2V4, c1(TM1)=net7(Q4.C)
    c56_c0x = c56_x + cmim_c0_dx
    c56_c0y = c56_y + cmim_c0_dy
    # c0(M5) to VCC: M5 wire touching cap M5 TOP edge, Via4 above cap, M4 to VCC rail
    c56_m5_top = c56_y + 7.59
    c56_via4_y = c56_m5_top + 2.0
    via_n(lna, c56_c0x, c56_via4_y, 'M4', 'Via4', 'M5')
    m5_wire(c56_c0x, c56_m5_top, c56_c0x, c56_via4_y)
    m4_wire(c56_c0x, c56_via4_y, c56_c0x, vcc_y)
    via_n(lna, c56_c0x, vcc_y, 'M3', 'Via3', 'M4')
    # c1(TM1) = net7 = Q4.C — text label only (TM1 into MIM breaks cap recognition)
    c56_c1x = c56_x + cmim_c0_dx
    c56_c1y = c56_y + cmim_c0_dy

    # C57-C61: VCC bypass chain on M5 (c0) and TM1 (c1)
    bypass_route_x = c57_61_x - 5.0  # x=255, clear of cap M5 plates

    # C57 c0 to VCC: horizontal M5 stub to bypass_route_x, then M4 vertical to vcc_y
    c57_c0x = c57_61_x + cmim_c0_dx
    c57_c0y = c57_61_ys[0] + cmim_c0_dy
    m5_wire(c57_c0x, c57_c0y, bypass_route_x, c57_c0y)
    via_n(lna, bypass_route_x, c57_c0y, 'M4', 'Via4', 'M5')
    m4_wire(bypass_route_x, c57_c0y, bypass_route_x, vcc_y)
    via_n(lna, bypass_route_x, vcc_y, 'M3', 'Via3', 'M4')

    # Chain: c1 of Cn connects to c0 of Cn+1
    for i in range(4):
        c1x = c57_61_x + cmim_c0_dx
        c1y = c57_61_ys[i] + cmim_c0_dy
        c0_next_x = c57_61_x + cmim_c0_dx
        c0_next_y = c57_61_ys[i+1] + cmim_c0_dy
        mid_y = (c1y + c0_next_y) / 2
        via_n(lna, bypass_route_x, mid_y, 'M5', 'TopVia1', 'TM1')
        lna.shapes(ly['TM1']).insert(pya.Box(
            um(min(c1x, bypass_route_x)-0.25), um(min(c1y, mid_y)-0.25),
            um(max(c1x, bypass_route_x)+0.25), um(c1y+0.25)))
        lna.shapes(ly['TM1']).insert(pya.Box(
            um(bypass_route_x-0.25), um(min(c1y, mid_y)-0.25),
            um(bypass_route_x+0.25), um(max(c1y, mid_y)+0.25)))
        m5_wire(bypass_route_x, mid_y, bypass_route_x, c0_next_y)
        m5_wire(bypass_route_x, c0_next_y, c0_next_x, c0_next_y)

    # C61 c1 to GND (use DIFFERENT X to avoid shorting to VCC M4 at bypass_route_x)
    bypass_gnd_x = bypass_route_x + 4.0  # 259, separate from VCC at 255
    c61_c1x = c57_61_x + cmim_c0_dx
    c61_c1y = c57_61_ys[4] + cmim_c0_dy
    via_n(lna, bypass_gnd_x, c61_c1y, 'M5', 'TopVia1', 'TM1')
    lna.shapes(ly['TM1']).insert(pya.Box(
        um(min(c61_c1x, bypass_gnd_x)-0.25), um(c61_c1y-0.25),
        um(max(c61_c1x, bypass_gnd_x)+0.25), um(c61_c1y+0.25)))
    # Connect bypass GND M5 to GND bus via M4 at separate X
    via_n(lna, bypass_gnd_x, c61_c1y, 'M4', 'Via4', 'M5')
    m4_wire(bypass_gnd_x, c61_c1y, bypass_gnd_x, gnd_y)
    via_n(lna, bypass_gnd_x, gnd_y, 'M4', 'Via4', 'M5')

    # C53 c1 (TM1) = INP port
    c53_c1x = c53_x + cmim_c0_dx
    c53_c1y = c53_y + cmim_c0_dy
    lna.shapes(ly['TM1']).insert(pya.Text("INP", pya.Trans(um(c53_c1x), um(c53_c1y))))

    # === PORT LABELS ===
    lna.shapes(ly['M5']).insert(pya.Text("2V4", pya.Trans(um(cx), um(vcc_y))))
    lna.shapes(ly['M5']).insert(pya.Text("GND", pya.Trans(um(cx), um(gnd_y))))
    lna.shapes(ly['TM1']).insert(pya.Text("INN", pya.Trans(um(c54_c1x), um(c54_c1y))))
    lna.shapes(ly['M5']).insert(pya.Text("OUTP", pya.Trans(um(c55_c0x), um(c55_c0y))))
    lna.shapes(ly['M5']).insert(pya.Text("B35&36", pya.Trans(um(cx), um(vcb_port_y))))

    if ext_layout is None:
        output = "/home/bthomas3/Videos/77GHz_phased_array/layout/LNA_77G_XTOR.gds"
        layout.write(output)
        print(f"\nLNA layout: {output}")
        print(f"Cell size: {CELL_W} x {CELL_H} um")
        print(f"Devices: 17x npn13G2L + 5x rppd + 9x cmim")


if __name__ == "__main__":
    main()
