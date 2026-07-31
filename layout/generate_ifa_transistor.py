"""
IF Amplifier (IFA) — Transistor-Level Layout
2-stage differential amplifier with BJT current sources on IHP SG13G2
Matches IFA_77G_XTOR.spice: 7×npn13G2l(6×Nx=2 + 1×Nx=1) + 7×rppd + 2×cap_cmim

Routing strategy: Use M2 for inter-device routing to avoid shorting M1 pins.
npn pins: C(M1) at (x+3.9, y+5.425), B(M1) at (x+3.9, y+1.775), E(M2) at (x+3.9, y+3.6)
Fingers placed side-by-side (same y, x offset 9um) so horizontal M1 connects same-pin-type safely.
"""

import sys
import pya

sys.path.insert(0, "/home/bthomas3/Videos/77GHz_phased_array/layout")
from pdk_devices import create_rppd

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"

LAYERS = {
    'M1': (8, 0), 'Via1': (19, 0), 'M2': (10, 0), 'Via2': (29, 0),
    'M3': (30, 0), 'Via3': (49, 0), 'M4': (50, 0), 'Via4': (66, 0),
    'M5': (67, 0), 'TopVia1': (125, 0), 'TM1': (126, 0),
    'TopVia2': (133, 0), 'TM2': (134, 0),
}

DBU = 0.001
CELL_W = 300.0
CELL_H = 400.0
OUT_DIR = "/home/bthomas3/Videos/77GHz_phased_array/layout/"

# npn13G2L pin offsets from cell origin (um)
NPN_C = (3.9, 5.425)   # Collector on M1
NPN_B = (3.9, 1.775)   # Base on M1
NPN_E = (3.9, 3.6)     # Emitter on M2
NPN_W = 7.8            # Cell width
NPN_DX = 9.0           # Finger-to-finger x spacing for Nx=2


def um(val):
    snapped = round(val / 0.005) * 0.005
    return int(snapped / DBU)


def box(cell, layer, x1, y1, x2, y2):
    """Insert box with coords in um."""
    cell.shapes(layer).insert(pya.Box(um(x1), um(y1), um(x2), um(y2)))


def npn_pins(ox, oy):
    """Return absolute pin positions for npn placed at (ox, oy)."""
    return {
        'C': (ox + NPN_C[0], oy + NPN_C[1]),
        'B': (ox + NPN_B[0], oy + NPN_B[1]),
        'E': (ox + NPN_E[0], oy + NPN_E[1]),
    }


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

    ifa = layout.create_cell("IFA_77G_XTOR")
    lm1 = ly['M1']
    lm2 = ly['M2']
    lv1 = ly['Via1']
    lm3 = ly['M3']
    lv2 = ly['Via2']
    W = 0.44  # wire half-width for routing

    # =================================================================
    # PLACEMENT - wide spacing to avoid routing shorts
    # =================================================================
    # Each Nx=2 device: two fingers at (x, y) and (x+NPN_DX, y)
    # Groups placed far apart (60um+ gaps) to prevent M1/M2 shorts

    # Row 1 (y=300): Q1, Q2 (stage 1 diff pair) - widely separated
    q1_origins = [(30, 300), (30 + NPN_DX, 300)]
    q2_origins = [(90, 300), (90 + NPN_DX, 300)]

    # Row 2 (y=220): Q5, Q6 (tail current sources)
    q5_origins = [(30, 220), (30 + NPN_DX, 220)]
    q6_origins = [(90, 220), (90 + NPN_DX, 220)]

    # Row 3 (y=140): Q3, Q4 (stage 2 diff pair)
    q3_origins = [(30, 140), (30 + NPN_DX, 140)]
    q4_origins = [(90, 140), (90 + NPN_DX, 140)]

    # Q7 (single finger) - isolated far right
    q7_origins = [(160, 220)]

    all_q = [q1_origins, q2_origins, q3_origins, q4_origins, q5_origins, q6_origins, q7_origins]
    q_pins = []
    if npn_idx is not None:
        for qgroup in all_q:
            group_pins = []
            for (x, y) in qgroup:
                ifa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(x), um(y))))
                group_pins.append(npn_pins(x, y))
            q_pins.append(group_pins)

    # Resistors - placed far right, away from all transistor routing
    # Spread Y positions to avoid M5 bridge overlaps (different Y per net)
    r1 = create_rppd(ifa, layout, 200, 330, 3.0, 8.33)   # VCC->out1p
    r2 = create_rppd(ifa, layout, 200, 345, 3.0, 8.33)   # VCC->out1n
    r3 = create_rppd(ifa, layout, 200, 360, 3.0, 8.33)   # VCC->OUTP
    r4 = create_rppd(ifa, layout, 200, 375, 3.0, 8.33)   # VCC->OUTN
    r5 = create_rppd(ifa, layout, 200, 50, 3.0, 18.23)   # VCC->BIAS
    r6 = create_rppd(ifa, layout, 220, 80, 3.0, 5.0)     # BIAS_E->GND
    r7 = create_rppd(ifa, layout, 220, 100, 3.0, 5.0)    # tail1_e->GND

    # Bypass caps - far right
    if cmim_idx is not None:
        ifa.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(220), um(300))))
        ifa.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(220), um(280))))

    # =================================================================
    # ROUTING - M1 for local pair, M2 for same-row, M3 for inter-row
    # Key: NEVER route M2 vertically between rows (shorts to emitters)
    # =================================================================

    if npn_idx is None:
        if ext_layout is None:
            output = f"{OUT_DIR}IFA_77G_XTOR.gds"
            layout.write(output)
        return ifa

    # q_pins indices: [0]=Q1, [1]=Q2, [2]=Q3, [3]=Q4, [4]=Q5, [5]=Q6, [6]=Q7

    def place_via1(x, y):
        box(ifa, lv1, x - 0.095, y - 0.095, x + 0.095, y + 0.095)
        box(ifa, lm1, x - 0.25, y - 0.25, x + 0.25, y + 0.25)
        box(ifa, lm2, x - 0.25, y - 0.25, x + 0.25, y + 0.25)

    def place_via2(x, y):
        box(ifa, lv2, x - 0.095, y - 0.095, x + 0.095, y + 0.095)
        box(ifa, lm2, x - 0.25, y - 0.25, x + 0.25, y + 0.25)
        box(ifa, lm3, x - 0.25, y - 0.25, x + 0.25, y + 0.25)

    def m1_wire_h(y, x1, x2, w=0.5):
        hw = w / 2
        box(ifa, lm1, min(x1, x2), y - hw, max(x1, x2), y + hw)

    def m1_wire_v(x, y1, y2, w=0.5):
        hw = w / 2
        box(ifa, lm1, x - hw, min(y1, y2), x + hw, max(y1, y2))

    def m2_wire_h(y, x1, x2, w=0.5):
        hw = w / 2
        box(ifa, lm2, min(x1, x2), y - hw, max(x1, x2), y + hw)

    def m2_wire_v(x, y1, y2, w=0.5):
        hw = w / 2
        box(ifa, lm2, x - hw, min(y1, y2), x + hw, max(y1, y2))

    def m3_wire_h(y, x1, x2, w=0.5):
        hw = w / 2
        box(ifa, lm3, min(x1, x2), y - hw, max(x1, x2), y + hw)

    def m3_wire_v(x, y1, y2, w=0.5):
        hw = w / 2
        box(ifa, lm3, x - hw, min(y1, y2), x + hw, max(y1, y2))

    def place_via3(x, y):
        box(ifa, ly['Via3'], x - 0.095, y - 0.095, x + 0.095, y + 0.095)
        box(ifa, lm3, x - 0.25, y - 0.25, x + 0.25, y + 0.25)
        box(ifa, lm4, x - 0.25, y - 0.25, x + 0.25, y + 0.25)

    lm4 = ly['M4']

    def m4_wire_h(y, x1, x2, w=0.5):
        hw = w / 2
        box(ifa, lm4, min(x1, x2), y - hw, max(x1, x2), y + hw)

    def m4_wire_v(x, y1, y2, w=0.5):
        hw = w / 2
        box(ifa, lm4, x - hw, min(y1, y2), x + hw, max(y1, y2))

    # Escape X positions: far from any transistor emitter M2
    # Left column (x=30): escape to x=15 (15um left of cell, 18.9um from emitter at 33.9)
    # Right column (x=90): escape to x=112 (12um right of last finger at 99.9+)
    # Q7 (x=160): escape to x=178 (14um right of pin at 163.9)
    # Resistor area (x=200+): already far from transistors, no escape needed
    ESC_L = 15.0
    ESC_R = 112.0
    ESC_Q7 = 178.0

    def m1_to_m3_esc(px, py, esc_x):
        """Route M1 pin horizontally to escape point, then via stack to M3."""
        m1_wire_h(py, px, esc_x)
        place_via1(esc_x, py)
        place_via2(esc_x, py)
        return (esc_x, py)

    def m1_to_m3(px, py):
        """Bring M1 pin up to M3 directly (for pins already far from transistors)."""
        place_via1(px, py)
        place_via2(px, py)

    def m2_to_m3_esc(px, py, esc_x):
        """Route M2 emitter to escape point, then via to M3."""
        m2_wire_h(py, px, esc_x)
        place_via2(esc_x, py)
        return (esc_x, py)

    def m2_to_m3(px, py):
        """Bring M2 pin up to M3 directly."""
        place_via2(px, py)

    def m3_to_m4(px, py):
        """Bring M3 to M4."""
        place_via3(px, py)

    # =================================================================
    # ROUTING ARCHITECTURE: M3=horizontal, M4=vertical
    # Nets can cross without shorting (different layers)
    # M1: local pair connections only
    # M2: emitter pair connections (same row only)
    # M3: all horizontal inter-group routing
    # M4: all vertical inter-group routing
    # =================================================================

    # --- INP net: Q1.B(×2) --- M1 local
    b1a, b1b = q_pins[0][0]['B'], q_pins[0][1]['B']
    m1_wire_h(b1a[1], b1a[0], b1b[0])

    # --- INN net: Q2.B(×2) --- M1 local
    b2a, b2b = q_pins[1][0]['B'], q_pins[1][1]['B']
    m1_wire_h(b2a[1], b2a[0], b2b[0])

    # --- tail1 net: Q1.E(×2), Q2.E(×2), Q5.C(×2) ---
    e1a, e1b = q_pins[0][0]['E'], q_pins[0][1]['E']
    e2a, e2b = q_pins[1][0]['E'], q_pins[1][1]['E']
    m2_wire_h(e1a[1], e1a[0], e2b[0])  # M2 horizontal same row
    c5a, c5b = q_pins[4][0]['C'], q_pins[4][1]['C']
    m1_wire_h(c5a[1], c5a[0], c5b[0])
    # Escape Q5.C to left, Q1.E to left
    m1_to_m3_esc(c5a[0], c5a[1], ESC_L)
    m2_to_m3_esc(e1a[0], e1a[1], ESC_L - 2)
    tail1_vx = 4.0
    m3_wire_h(c5a[1], ESC_L, tail1_vx)
    m3_to_m4(tail1_vx, c5a[1])
    m3_wire_h(e1a[1], ESC_L - 2, tail1_vx)
    m3_to_m4(tail1_vx, e1a[1])
    m4_wire_v(tail1_vx, min(c5a[1], e1a[1]), max(c5a[1], e1a[1]))

    # --- tail2 net: Q3.E(×2), Q4.E(×2), Q6.C(×2) ---
    e3a, e3b = q_pins[2][0]['E'], q_pins[2][1]['E']
    e4a, e4b = q_pins[3][0]['E'], q_pins[3][1]['E']
    m2_wire_h(e3a[1], e3a[0], e4b[0])  # M2 horizontal same row
    c6a, c6b = q_pins[5][0]['C'], q_pins[5][1]['C']
    m1_wire_h(c6a[1], c6a[0], c6b[0])
    # Escape Q6.C to right, Q3.E to right
    m1_to_m3_esc(c6a[0], c6a[1], ESC_R)
    m2_to_m3_esc(e3a[0], e3a[1], ESC_R + 2)
    tail2_vx = 126.0
    m3_wire_h(c6a[1], ESC_R, tail2_vx)
    m3_to_m4(tail2_vx, c6a[1])
    m3_wire_h(e3a[1], ESC_R + 2, tail2_vx)
    m3_to_m4(tail2_vx, e3a[1])
    m4_wire_v(tail2_vx, min(c6a[1], e3a[1]), max(c6a[1], e3a[1]))

    # --- out1p net: Q1.C(×2), Q3.B(×2), R1.M ---
    c1a, c1b = q_pins[0][0]['C'], q_pins[0][1]['C']
    m1_wire_h(c1a[1], c1a[0], c1b[0])
    b3a, b3b = q_pins[2][0]['B'], q_pins[2][1]['B']
    m1_wire_h(b3a[1], b3a[0], b3b[0])
    m1_to_m3_esc(c1a[0], c1a[1], ESC_L)
    m1_to_m3_esc(b3a[0], b3a[1], ESC_L)
    m1_to_m3(r1['P'][0], r1['P'][1])
    out1p_vx = 6.0
    m3_wire_h(c1a[1], ESC_L, out1p_vx)
    m3_to_m4(out1p_vx, c1a[1])
    m3_wire_h(b3a[1], ESC_L, out1p_vx)
    m3_to_m4(out1p_vx, b3a[1])
    m3_wire_h(r1['P'][1], r1['P'][0], out1p_vx)
    m3_to_m4(out1p_vx, r1['P'][1])
    ys = sorted([c1a[1], b3a[1], r1['P'][1]])
    m4_wire_v(out1p_vx, ys[0], ys[-1])

    # --- out1n net: Q2.C(×2), Q4.B(×2), R2.M ---
    c2a, c2b = q_pins[1][0]['C'], q_pins[1][1]['C']
    m1_wire_h(c2a[1], c2a[0], c2b[0])
    b4a, b4b = q_pins[3][0]['B'], q_pins[3][1]['B']
    m1_wire_h(b4a[1], b4a[0], b4b[0])
    m1_to_m3_esc(c2a[0], c2a[1], ESC_R)
    m1_to_m3_esc(b4a[0], b4a[1], ESC_R)
    m1_to_m3(r2['P'][0], r2['P'][1])
    out1n_vx = 130.0
    m3_wire_h(c2a[1], ESC_R, out1n_vx)
    m3_to_m4(out1n_vx, c2a[1])
    m3_wire_h(b4a[1], ESC_R, out1n_vx)
    m3_to_m4(out1n_vx, b4a[1])
    m3_wire_h(r2['P'][1], r2['P'][0], out1n_vx)
    m3_to_m4(out1n_vx, r2['P'][1])
    ys = sorted([c2a[1], b4a[1], r2['P'][1]])
    m4_wire_v(out1n_vx, ys[0], ys[-1])

    # --- OUTP net: Q3.C(×2), R3.M ---
    c3a, c3b = q_pins[2][0]['C'], q_pins[2][1]['C']
    m1_wire_h(c3a[1], c3a[0], c3b[0])
    m1_to_m3_esc(c3a[0], c3a[1], ESC_L)
    m1_to_m3(r3['P'][0], r3['P'][1])
    outp_vx = 8.0
    m3_wire_h(c3a[1], ESC_L, outp_vx)
    m3_to_m4(outp_vx, c3a[1])
    m3_wire_h(r3['P'][1], r3['P'][0], outp_vx)
    m3_to_m4(outp_vx, r3['P'][1])
    ys = sorted([c3a[1], r3['P'][1]])
    m4_wire_v(outp_vx, ys[0], ys[-1])

    # --- OUTN net: Q4.C(×2), R4.M ---
    c4a, c4b = q_pins[3][0]['C'], q_pins[3][1]['C']
    m1_wire_h(c4a[1], c4a[0], c4b[0])
    m1_to_m3_esc(c4a[0], c4a[1], ESC_R)
    m1_to_m3(r4['P'][0], r4['P'][1])
    outn_vx = 134.0
    m3_wire_h(c4a[1], ESC_R, outn_vx)
    m3_to_m4(outn_vx, c4a[1])
    m3_wire_h(r4['P'][1], r4['P'][0], outn_vx)
    m3_to_m4(outn_vx, r4['P'][1])
    ys = sorted([c4a[1], r4['P'][1]])
    m4_wire_v(outn_vx, ys[0], ys[-1])

    # --- BIAS net: Q5.B(×2), Q6.B(×2), Q7.C, Q7.B, R5.M ---
    b5a, b5b = q_pins[4][0]['B'], q_pins[4][1]['B']
    b6a, b6b = q_pins[5][0]['B'], q_pins[5][1]['B']
    q7c = q_pins[6][0]['C']
    q7b = q_pins[6][0]['B']
    m1_wire_h(b5a[1], b5a[0], b5b[0])
    m1_wire_h(b6a[1], b6a[0], b6b[0])
    m1_to_m3_esc(b5a[0], b5a[1], ESC_L)
    m1_to_m3_esc(b6a[0], b6a[1], ESC_R)
    m1_to_m3_esc(q7c[0], q7c[1], ESC_Q7)
    m1_to_m3_esc(q7b[0], q7b[1], ESC_Q7 - 4)
    m1_to_m3(r5['P'][0], r5['P'][1])
    bias_vx = 138.0
    m3_wire_h(b5a[1], ESC_L, bias_vx)
    m3_to_m4(bias_vx, b5a[1])
    m3_wire_h(b6a[1], ESC_R, bias_vx)
    m3_to_m4(bias_vx, b6a[1])
    m3_wire_h(q7c[1], ESC_Q7, bias_vx)
    m3_to_m4(bias_vx, q7c[1])
    m3_wire_h(q7b[1], ESC_Q7 - 4, bias_vx)
    m3_to_m4(bias_vx, q7b[1])
    m3_wire_h(r5['P'][1], r5['P'][0], bias_vx)
    m3_to_m4(bias_vx, r5['P'][1])
    bias_ys = sorted([b5a[1], b6a[1], q7c[1], q7b[1], r5['P'][1]])
    m4_wire_v(bias_vx, bias_ys[0], bias_ys[-1])

    # --- tail1_e net: Q5.E(×2), R7.M ---
    e5a, e5b = q_pins[4][0]['E'], q_pins[4][1]['E']
    m2_wire_h(e5a[1], e5a[0], e5b[0])
    m2_to_m3_esc(e5a[0], e5a[1], ESC_L - 4)
    m1_to_m3(r7['M'][0], r7['M'][1])
    t1e_vx = 2.0
    m3_wire_h(e5a[1], ESC_L - 4, t1e_vx)
    m3_to_m4(t1e_vx, e5a[1])
    m3_wire_h(r7['M'][1], r7['M'][0], t1e_vx)
    m3_to_m4(t1e_vx, r7['M'][1])
    ys = sorted([e5a[1], r7['M'][1]])
    m4_wire_v(t1e_vx, ys[0], ys[-1])

    # --- BIAS_E net: Q7.E, R6.M ---
    q7e = q_pins[6][0]['E']
    m2_to_m3_esc(q7e[0], q7e[1], ESC_Q7 + 2)
    m1_to_m3(r6['M'][0], r6['M'][1])
    biase_vx = 192.0
    m3_wire_h(q7e[1], ESC_Q7 + 2, biase_vx)
    m3_to_m4(biase_vx, q7e[1])
    m3_wire_h(r6['M'][1], r6['M'][0], biase_vx)
    m3_to_m4(biase_vx, r6['M'][1])
    ys = sorted([q7e[1], r6['M'][1]])
    m4_wire_v(biase_vx, ys[0], ys[-1])

    # --- GND net: Q6.E(×2), R6.P, R7.P ---
    e6a, e6b = q_pins[5][0]['E'], q_pins[5][1]['E']
    m2_wire_h(e6a[1], e6a[0], e6b[0])
    m2_to_m3_esc(e6b[0], e6b[1], ESC_R + 4)
    m1_to_m3(r6['P'][0], r6['P'][1])
    m1_to_m3(r7['P'][0], r7['P'][1])
    gnd_vx = 142.0
    m3_wire_h(e6b[1], ESC_R + 4, gnd_vx)
    m3_to_m4(gnd_vx, e6b[1])
    m3_wire_h(r6['P'][1], r6['P'][0], gnd_vx)
    m3_to_m4(gnd_vx, r6['P'][1])
    m3_wire_h(r7['P'][1], r7['P'][0], gnd_vx)
    m3_to_m4(gnd_vx, r7['P'][1])
    gnd_ys = sorted([e6b[1], r6['P'][1], r7['P'][1]])
    m4_wire_v(gnd_vx, gnd_ys[0], gnd_ys[-1])

    # --- VCC net: R1.P, R2.P, R3.P, R4.P, R5.P ---
    vcc_pins = [r1['M'], r2['M'], r3['M'], r4['M'], r5['M']]
    for vp in vcc_pins:
        m1_to_m3(vp[0], vp[1])
    vcc_vx = 196.0
    for vp in vcc_pins:
        m3_wire_h(vp[1], vp[0], vcc_vx)
        m3_to_m4(vcc_vx, vp[1])
    vcc_ys = sorted([vp[1] for vp in vcc_pins])
    m4_wire_v(vcc_vx, vcc_ys[0], vcc_ys[-1])

    # --- Bypass caps: C53, C54 at (220, 300) and (220, 280) ---
    # cmim cell has vmim (129,0) internal vias connecting M5↔TM1
    # c0 = mim_top (TM1 plate), c1 = mim_btm (M5 plate) per extraction terminal order
    # Schematic: XC1 VCC GND → c0(TM1)=VCC, c1(M5)=GND
    # VCO approach: M5 wire touching cap M5 TOP edge (outside MIM), TM1 text label
    cap_origins = [(220.0, 300.0), (220.0, 280.0)]

    # GND → c1 (M5 bottom plate): M5 wire touching cap M5 TOP edge
    # CRITICAL: GND M4 horizontal must NOT cross VCC M4 vertical at x=196
    # Solution: Via4 at gnd_vx=142 (on GND M4 vertical), then M5 horizontal to cap
    gnd_m5_x = 225.0
    gnd_via4_y = cap_origins[0][1] + 7.59 + 2.0  # 309.59
    m4_wire_v(gnd_vx, gnd_ys[-1], gnd_via4_y)
    # Single Via4 at GND M4 vertical top (x=142), then M5 horizontal to each cap
    box(ifa, ly['Via4'], gnd_vx - 0.095, gnd_via4_y - 0.095, gnd_vx + 0.095, gnd_via4_y + 0.095)
    box(ifa, lm4, gnd_vx - 0.25, gnd_via4_y - 0.25, gnd_vx + 0.25, gnd_via4_y + 0.25)
    box(ifa, ly['M5'], gnd_vx - 0.25, gnd_via4_y - 0.25, gnd_vx + 0.25, gnd_via4_y + 0.25)
    for cx_cap, cy_cap in cap_origins:
        cap_m5_top = cy_cap + 7.59
        # M5 horizontal from gnd_vx to cap X, then vertical down to cap M5 top edge
        box(ifa, ly['M5'], gnd_vx - 0.25, gnd_via4_y - 0.25, gnd_m5_x + 0.25, gnd_via4_y + 0.25)
        box(ifa, ly['M5'], gnd_m5_x - 0.25, cap_m5_top, gnd_m5_x + 0.25, gnd_via4_y + 0.25)

    # VCC → c0 (TM1 top plate): use text label (same as VCO approach)
    # Physical TM1 routing into cap area breaks device recognition (enters MIM area)
    # Instead: place "VCC" text on TM1 text layer (126,25) at cap TM1 plate
    ly_tm1_txt = layout.layer(126, 25)
    ly_m5_txt = layout.layer(67, 25)
    for cx_cap, cy_cap in cap_origins:
        ifa.shapes(ly_tm1_txt).insert(pya.Text("VCC", pya.Trans(um(cx_cap + 3.5), um(cy_cap + 3.5))))
    # Also label the GND M5 connection
    for cx_cap, cy_cap in cap_origins:
        ifa.shapes(ly_m5_txt).insert(pya.Text("GND", pya.Trans(um(gnd_m5_x), um(cy_cap + 7.59 + 1.0))))
    # Label VCC on the rppd VCC M4 rail (M4 text layer 50,25)
    ly_m4_txt = layout.layer(50, 25)
    ifa.shapes(ly_m4_txt).insert(pya.Text("VCC", pya.Trans(um(vcc_vx), um(vcc_ys[2]))))

    # --- Port labels on TM2 ---
    ly_tm2 = ly['TM2']
    cx = CELL_W / 2
    cy = CELL_H / 2
    label_positions = {
        'INP': (cx - 60, cy + 50),
        'INN': (cx + 60, cy + 50),
        'OUTP': (cx - 60, cy - 50),
        'OUTN': (cx + 60, cy - 50),
        'VCC': (cx, cy + 120),
        'GND': (cx, cy - 120),
    }
    for name, (px, py) in label_positions.items():
        ifa.shapes(ly_tm2).insert(pya.Text(name, pya.Trans(um(px), um(py))))

    if ext_layout is None:
        output = f"{OUT_DIR}IFA_77G_XTOR.gds"
        layout.write(output)
        print(f"IFA layout: {output}")
        print(f"Cell: {CELL_W}x{CELL_H}um")
        print(f"Devices: 13xnpn13G2L(fingers) + 7xrppd + 2xcmim")

    return ifa


if __name__ == "__main__":
    main()