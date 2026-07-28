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
    # PLACEMENT - side-by-side fingers, generous spacing between groups
    # =================================================================
    # Each Nx=2 device: two fingers at (x, y) and (x+NPN_DX, y)
    # Groups placed far apart (30um+ vertical gaps) to avoid cross-shorts

    # Row 1 (y=260): Q1, Q2 (stage 1 diff pair)
    q1_origins = [(20, 260), (20 + NPN_DX, 260)]
    q2_origins = [(55, 260), (55 + NPN_DX, 260)]

    # Row 2 (y=220): Q5, Q6 (tail current sources)
    q5_origins = [(20, 220), (20 + NPN_DX, 220)]
    q6_origins = [(55, 220), (55 + NPN_DX, 220)]

    # Row 3 (y=160): Q3, Q4 (stage 2 diff pair)
    q3_origins = [(20, 160), (20 + NPN_DX, 160)]
    q4_origins = [(55, 160), (55 + NPN_DX, 160)]

    # Q7 (single finger) - isolated
    q7_origins = [(100, 220)]

    all_q = [q1_origins, q2_origins, q3_origins, q4_origins, q5_origins, q6_origins, q7_origins]
    q_pins = []
    if npn_idx is not None:
        for qgroup in all_q:
            group_pins = []
            for (x, y) in qgroup:
                ifa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(x), um(y))))
                group_pins.append(npn_pins(x, y))
            q_pins.append(group_pins)

    # Resistors - placed with large spacing, away from transistors
    # R1,R2 above Q1,Q2 row; R3,R4 above Q3,Q4 row; R5,R6,R7 to the right
    r1 = create_rppd(ifa, layout, 130, 300, 3.0, 8.33)   # VCC->out1p
    r2 = create_rppd(ifa, layout, 145, 300, 3.0, 8.33)   # VCC->out1n
    r3 = create_rppd(ifa, layout, 165, 300, 3.0, 8.33)   # VCC->OUTP
    r4 = create_rppd(ifa, layout, 180, 300, 3.0, 8.33)   # VCC->OUTN
    r5 = create_rppd(ifa, layout, 200, 280, 3.0, 18.23)  # VCC->BIAS
    r6 = create_rppd(ifa, layout, 130, 180, 3.0, 5.0)    # BIAS_E->GND
    r7 = create_rppd(ifa, layout, 145, 180, 3.0, 5.0)    # tail1_e->GND

    # Bypass caps - far right
    if cmim_idx is not None:
        ifa.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(220), um(300))))
        ifa.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(220), um(280))))

    # =================================================================
    # ROUTING - Use M2 for inter-device nets, M1 only for local pair connections
    # Strategy: For each net, connect M1 pins to a dedicated M2 bus via Via1
    # =================================================================

    if npn_idx is None:
        if ext_layout is None:
            output = f"{OUT_DIR}IFA_77G_XTOR.gds"
            layout.write(output)
        return ifa

    # q_pins indices: [0]=Q1, [1]=Q2, [2]=Q3, [3]=Q4, [4]=Q5, [5]=Q6, [6]=Q7

    def place_via1(x, y):
        box(ifa, lv1, x - 0.22, y - 0.22, x + 0.22, y + 0.22)

    def m1_wire_h(y, x1, x2, w=0.88):
        """Horizontal M1 wire."""
        hw = w / 2
        box(ifa, lm1, min(x1, x2), y - hw, max(x1, x2), y + hw)

    def m1_wire_v(x, y1, y2, w=0.88):
        """Vertical M1 wire."""
        hw = w / 2
        box(ifa, lm1, x - hw, min(y1, y2), x + hw, max(y1, y2))

    def m2_wire_h(y, x1, x2, w=0.88):
        """Horizontal M2 wire."""
        hw = w / 2
        box(ifa, lm2, min(x1, x2), y - hw, max(x1, x2), y + hw)

    def m2_wire_v(x, y1, y2, w=0.88):
        """Vertical M2 wire."""
        hw = w / 2
        box(ifa, lm2, x - hw, min(y1, y2), x + hw, max(y1, y2))

    def m3_wire_h(y, x1, x2, w=0.88):
        hw = w / 2
        box(ifa, lm3, min(x1, x2), y - hw, max(x1, x2), y + hw)

    def m3_wire_v(x, y1, y2, w=0.88):
        hw = w / 2
        box(ifa, lm3, x - hw, min(y1, y2), x + hw, max(y1, y2))

    def place_via2(x, y):
        box(ifa, lv2, x - 0.22, y - 0.22, x + 0.22, y + 0.22)

    # --- Helper: connect M1 pin to M2 bus at given routing y ---
    def pin_to_m2_bus(pin_x, pin_y, bus_y, bus_x=None):
        """Connect M1 pin at (pin_x, pin_y) up to M2 horizontal bus at bus_y.
        Returns the x coordinate used on the bus."""
        # Place via at pin location
        place_via1(pin_x, pin_y)
        # M2 vertical from pin to bus_y
        if bus_x is None:
            bus_x = pin_x
        m2_wire_v(pin_x, pin_y, bus_y)
        if abs(bus_x - pin_x) > 0.01:
            m2_wire_h(bus_y, pin_x, bus_x)
        return bus_x

    # --- INP net: Q1.B(×2) --- just horizontal M1 between pair
    # Q1 bases are at same y (261.775), different x
    b1a, b1b = q_pins[0][0]['B'], q_pins[0][1]['B']
    m1_wire_h(b1a[1], b1a[0], b1b[0])

    # --- INN net: Q2.B(×2) --- just horizontal M1 between pair
    b2a, b2b = q_pins[1][0]['B'], q_pins[1][1]['B']
    m1_wire_h(b2a[1], b2a[0], b2b[0])

    # --- out1p net: Q1.C(×2), Q3.B(×2), R1.M ---
    # Q1.C pair: horizontal M1 connection (same y=265.425)
    c1a, c1b = q_pins[0][0]['C'], q_pins[0][1]['C']
    m1_wire_h(c1a[1], c1a[0], c1b[0])
    # Q3.B pair: horizontal M1 connection (same y=161.775)
    b3a, b3b = q_pins[2][0]['B'], q_pins[2][1]['B']
    m1_wire_h(b3a[1], b3a[0], b3b[0])
    # Route on M2 bus at y=270 to connect Q1.C, Q3.B, R1.M
    out1p_bus_y = 270.0
    # Q1.C[0] -> via -> M2
    place_via1(c1a[0], c1a[1])
    m2_wire_v(c1a[0], c1a[1], out1p_bus_y)
    # Q3.B[0] -> via -> M2
    place_via1(b3a[0], b3a[1])
    m2_wire_v(b3a[0], b3a[1], out1p_bus_y)
    # R1.M -> via -> M2
    place_via1(r1['M'][0], r1['M'][1])
    m2_wire_v(r1['M'][0], r1['M'][1], out1p_bus_y)
    # Horizontal M2 bus connecting all three
    xs = sorted([c1a[0], b3a[0], r1['M'][0]])
    m2_wire_h(out1p_bus_y, xs[0], xs[-1])

    # --- out1n net: Q2.C(×2), Q4.B(×2), R2.M ---
    c2a, c2b = q_pins[1][0]['C'], q_pins[1][1]['C']
    m1_wire_h(c2a[1], c2a[0], c2b[0])
    b4a, b4b = q_pins[3][0]['B'], q_pins[3][1]['B']
    m1_wire_h(b4a[1], b4a[0], b4b[0])
    out1n_bus_y = 272.0
    place_via1(c2a[0], c2a[1])
    m2_wire_v(c2a[0], c2a[1], out1n_bus_y)
    place_via1(b4a[0], b4a[1])
    m2_wire_v(b4a[0], b4a[1], out1n_bus_y)
    place_via1(r2['M'][0], r2['M'][1])
    m2_wire_v(r2['M'][0], r2['M'][1], out1n_bus_y)
    xs = sorted([c2a[0], b4a[0], r2['M'][0]])
    m2_wire_h(out1n_bus_y, xs[0], xs[-1])

    # --- OUTP net: Q3.C(×2), R3.M ---
    c3a, c3b = q_pins[2][0]['C'], q_pins[2][1]['C']
    m1_wire_h(c3a[1], c3a[0], c3b[0])
    outp_bus_y = 274.0
    place_via1(c3a[0], c3a[1])
    m2_wire_v(c3a[0], c3a[1], outp_bus_y)
    place_via1(r3['M'][0], r3['M'][1])
    m2_wire_v(r3['M'][0], r3['M'][1], outp_bus_y)
    xs = sorted([c3a[0], r3['M'][0]])
    m2_wire_h(outp_bus_y, xs[0], xs[-1])

    # --- OUTN net: Q4.C(×2), R4.M ---
    c4a, c4b = q_pins[3][0]['C'], q_pins[3][1]['C']
    m1_wire_h(c4a[1], c4a[0], c4b[0])
    outn_bus_y = 276.0
    place_via1(c4a[0], c4a[1])
    m2_wire_v(c4a[0], c4a[1], outn_bus_y)
    place_via1(r4['M'][0], r4['M'][1])
    m2_wire_v(r4['M'][0], r4['M'][1], outn_bus_y)
    xs = sorted([c4a[0], r4['M'][0]])
    m2_wire_h(outn_bus_y, xs[0], xs[-1])

    # --- tail1 net: Q1.E(×2), Q2.E(×2), Q5.C(×2) ---
    # Q1.E and Q2.E are on M2 already. Q5.C is on M1 needs via.
    # E pins: Q1 at y=263.6, Q2 at y=263.6, Q5 at y=223.6
    e1a, e1b = q_pins[0][0]['E'], q_pins[0][1]['E']
    e2a, e2b = q_pins[1][0]['E'], q_pins[1][1]['E']
    # Connect Q1.E pair on M2
    m2_wire_h(e1a[1], e1a[0], e1b[0])
    # Connect Q2.E pair on M2
    m2_wire_h(e2a[1], e2a[0], e2b[0])
    # Connect Q1.E to Q2.E on M2 (same y)
    m2_wire_h(e1a[1], e1b[0], e2a[0])
    # Q5.C pair on M1
    c5a, c5b = q_pins[4][0]['C'], q_pins[4][1]['C']
    m1_wire_h(c5a[1], c5a[0], c5b[0])
    # Via Q5.C[0] to M2, then M2 to Q1.E bus
    place_via1(c5a[0], c5a[1])
    m2_wire_v(c5a[0], c5a[1], e1a[1])
    m2_wire_h(e1a[1], c5a[0], e1a[0])

    # --- tail2 net: Q3.E(×2), Q4.E(×2), Q6.C(×2) ---
    e3a, e3b = q_pins[2][0]['E'], q_pins[2][1]['E']
    e4a, e4b = q_pins[3][0]['E'], q_pins[3][1]['E']
    m2_wire_h(e3a[1], e3a[0], e3b[0])
    m2_wire_h(e4a[1], e4a[0], e4b[0])
    m2_wire_h(e3a[1], e3b[0], e4a[0])
    c6a, c6b = q_pins[5][0]['C'], q_pins[5][1]['C']
    m1_wire_h(c6a[1], c6a[0], c6b[0])
    place_via1(c6a[0], c6a[1])
    m2_wire_v(c6a[0], c6a[1], e3a[1])
    m2_wire_h(e3a[1], c6a[0], e3a[0])

    # --- BIAS net: Q5.B(×2), Q6.B(×2), Q7.C, Q7.B, R5.M ---
    # All on M1. Use M2 bus at y=215 to interconnect.
    b5a, b5b = q_pins[4][0]['B'], q_pins[4][1]['B']
    b6a, b6b = q_pins[5][0]['B'], q_pins[5][1]['B']
    q7c = q_pins[6][0]['C']
    q7b = q_pins[6][0]['B']
    # Connect Q5.B pair on M1
    m1_wire_h(b5a[1], b5a[0], b5b[0])
    # Connect Q6.B pair on M1
    m1_wire_h(b6a[1], b6a[0], b6b[0])
    # Connect Q7.C to Q7.B on M1 (same x, vertical) - diode
    m1_wire_v(q7c[0], q7b[1], q7c[1])
    # M2 bus for BIAS at y=215
    bias_bus_y = 215.0
    # Q5.B -> via -> M2
    place_via1(b5a[0], b5a[1])
    m2_wire_v(b5a[0], b5a[1], bias_bus_y)
    # Q6.B -> via -> M2
    place_via1(b6a[0], b6a[1])
    m2_wire_v(b6a[0], b6a[1], bias_bus_y)
    # Q7.C -> via -> M2 (use Q7.C since it's already connected to Q7.B by M1)
    place_via1(q7c[0], q7c[1])
    m2_wire_v(q7c[0], q7c[1], bias_bus_y)
    # R5.M -> via -> M2
    place_via1(r5['M'][0], r5['M'][1])
    m2_wire_v(r5['M'][0], r5['M'][1], bias_bus_y)
    # Horizontal M2 BIAS bus
    bias_xs = sorted([b5a[0], b6a[0], q7c[0], r5['M'][0]])
    m2_wire_h(bias_bus_y, bias_xs[0], bias_xs[-1])

    # --- tail1_e net: Q5.E(×2), R7.P ---
    # Q5.E on M2, R7.P on M1
    e5a, e5b = q_pins[4][0]['E'], q_pins[4][1]['E']
    m2_wire_h(e5a[1], e5a[0], e5b[0])
    # Via from R7.P to M2
    place_via1(r7['P'][0], r7['P'][1])
    m2_wire_v(r7['P'][0], r7['P'][1], e5a[1])
    m2_wire_h(e5a[1], r7['P'][0], e5a[0])

    # --- BIAS_E net: Q7.E, R6.P ---
    # Q7.E on M2, R6.P on M1
    q7e = q_pins[6][0]['E']
    place_via1(r6['P'][0], r6['P'][1])
    m2_wire_v(r6['P'][0], r6['P'][1], q7e[1])
    m2_wire_h(q7e[1], r6['P'][0], q7e[0])

    # --- GND net: Q6.E(×2), R6.M, R7.M ---
    # Q6.E on M2, R6.M and R7.M on M1
    e6a, e6b = q_pins[5][0]['E'], q_pins[5][1]['E']
    m2_wire_h(e6a[1], e6a[0], e6b[0])
    # Connect R6.M and R7.M on M1
    r6m = r6['M']
    r7m = r7['M']
    m1_wire_h(r6m[1], r6m[0], r7m[0]) if abs(r6m[1] - r7m[1]) < 0.1 else None
    if abs(r6m[1] - r7m[1]) >= 0.1:
        # vertical route between them
        m1_wire_v(r6m[0], r6m[1], r7m[1])
        m1_wire_h(r7m[1], r6m[0], r7m[0])
    # Via from R6.M to M2 to connect to Q6.E
    place_via1(r6m[0], r6m[1])
    m2_wire_v(r6m[0], r6m[1], e6a[1])
    m2_wire_h(e6a[1], r6m[0], e6a[0])

    # --- VCC net: R1.P, R2.P, R3.P, R4.P, R5.P, C1.c0, C2.c0 ---
    # All R.P are on M1. Connect with M1 horizontal bus (all at same y since same rppd y)
    vcc_pins = [r1['P'], r2['P'], r3['P'], r4['P'], r5['P']]
    # They may be at different y due to different resistor lengths
    # Use M2 bus for VCC at y=320
    vcc_bus_y = 320.0
    for vp in vcc_pins:
        place_via1(vp[0], vp[1])
        m2_wire_v(vp[0], vp[1], vcc_bus_y)
    vcc_xs = sorted([vp[0] for vp in vcc_pins])
    m2_wire_h(vcc_bus_y, vcc_xs[0], vcc_xs[-1])

    # Caps: c0=VCC(top), c1=GND(bottom)
    # cmim cell: from PDK analysis, c0 pin at top M3/M4, c1 at bottom
    # For LVS the cap pins are typically on MIM layers but connected via M3/M4
    # The cmim cell has pins accessible on M4 or M5
    # For now connect via M2 bus extended to cap region
    if cmim_idx is not None:
        # cmim 7x7um: c0 (top plate) typically at (x+3.5, y+top), c1 at (x+3.5, y+bot)
        # Based on PDK, cap_cmim pins are on M5 layer
        # We'll connect VCC M2 bus to cap c0 region and GND to c1
        cap1_x = 220 + 3.5
        cap1_c0_y = 300 + 6.5  # approximate top
        cap1_c1_y = 300 + 0.5  # approximate bottom
        cap2_c0_y = 280 + 6.5
        cap2_c1_y = 280 + 0.5
        # Extend VCC bus to caps
        m2_wire_h(vcc_bus_y, vcc_xs[-1], cap1_x)
        m2_wire_v(cap1_x, vcc_bus_y, cap1_c0_y)
        m2_wire_v(cap1_x, cap2_c0_y, cap1_c0_y)
        # GND bus to cap bottoms
        gnd_bus_y = 178.0
        m2_wire_h(gnd_bus_y, r6m[0], cap1_x)
        m2_wire_v(cap1_x, gnd_bus_y, cap1_c1_y)
        m2_wire_v(cap1_x, cap2_c1_y, cap1_c1_y)

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