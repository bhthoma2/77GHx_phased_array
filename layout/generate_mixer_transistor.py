"""
77 GHz Mixer (MIXER_77G_XTOR) — Transistor-Level Layout
Gilbert cell matching MIXER_77G_XTOR.spice schematic for LVS.

Schematic devices:
  Q20(Nx=4): C=ELOL, B=RFP_I, E=GND
  Q21(Nx=4): C=ELOR, B=RFN_I, E=GND
  Q22(Nx=4): C=2V4, B=LOP_I, E=ELOL
  Q23(Nx=4): C=IFN, B=LON_I, E=ELOL
  Q24(Nx=4): C=IFN, B=LOP_I, E=ELOR
  Q25(Nx=4): C=IFP, B=LON_I, E=ELOR
  Q26(Nx=1): C=BIAS, B=BIAS, E=BIAS_MID
  Q27(Nx=1): C=BIAS_MID, B=BIAS_MID, E=GND
  R21(w=3u,l=18.23u,m=2): P=2V4, M=2V4
  R22(w=3u,l=18.23u,m=2): P=2V4, M=2V4
  R23(w=3u,l=27.48u,m=1): P=2V4, M=net1
  R24(w=3u,l=27.48u,m=1): P=2V4, M=2V4
  C37-C40: AC coupling (w=7u,l=7u)
  C41-C43: VCC bypass (w=7u,l=7u)
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
CELL_H = 450.0


def um(val):
    snapped = round(val / 0.005) * 0.005
    return int(snapped / DBU)


def snap(val):
    return round(val / 0.005) * 0.005


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

    mixer = layout.create_cell("MIXER_77G_XTOR")
    cx = CELL_W / 2
    cy = CELL_H / 2

    # Helper: single via between two metal layers
    def via_n(x, y, bot_layer, via_layer, top_layer):
        x, y = snap(x), snap(y)
        ps, vs = um(0.5), um(0.19)
        cxi, cyi = um(x), um(y)
        mixer.shapes(ly[bot_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))
        mixer.shapes(ly[via_layer]).insert(pya.Box(cxi-vs//2, cyi-vs//2, cxi+vs//2, cyi+vs//2))
        mixer.shapes(ly[top_layer]).insert(pya.Box(cxi-ps//2, cyi-ps//2, cxi+ps//2, cyi+ps//2))

    # Helper: horizontal M-layer wire
    def hwire(layer, x1, x2, y, hw=0.25):
        mixer.shapes(ly[layer]).insert(pya.Box(um(min(x1,x2)-hw), um(y-hw), um(max(x1,x2)+hw), um(y+hw)))

    # Helper: vertical M-layer wire
    def vwire(layer, x, y1, y2, hw=0.25):
        mixer.shapes(ly[layer]).insert(pya.Box(um(x-hw), um(min(y1,y2)-hw), um(x+hw), um(max(y1,y2)+hw)))

    # ================================================================
    # DEVICE PLACEMENT
    # ================================================================
    # npn13G2L pin offsets from cell origin:
    #   C at (3.9, 5.425) on M1
    #   B at (3.9, 1.775) on M1
    #   E at (3.9, 3.6)   on M2
    pcx = 3.9
    col_dy = 5.425
    bas_dy = 1.775
    emi_dy = 3.6

    hbt_sp = 10.0  # vertical spacing between fingers
    pair_gap = 30.0

    # --- RF transconductor pair: Q20 (left, 4 fingers), Q21 (right, 4 fingers) ---
    q20_x = cx - pair_gap/2 - 7.8   # cell origin X for Q20 column
    q21_x = cx + pair_gap/2          # cell origin X for Q21 column
    q20_ys = [cy - 60 + i*hbt_sp for i in range(4)]
    q21_ys = [cy - 60 + i*hbt_sp for i in range(4)]

    # --- LO switching quad (4 devices × 4 fingers each) ---
    # Q22: C=2V4, B=LOP_I, E=ELOL  (left-inner)
    # Q23: C=IFN, B=LON_I, E=ELOL  (left-outer)
    # Q24: C=IFN, B=LOP_I, E=ELOR  (right-outer)
    # Q25: C=IFP, B=LON_I, E=ELOR  (right-inner)
    lo_base_y = cy + 50
    q22_x = cx - pair_gap/2 - 7.8       # same column as Q20
    q23_x = cx - pair_gap/2 - 7.8 - 15  # outer left
    q24_x = cx + pair_gap/2 + 15         # outer right
    q25_x = cx + pair_gap/2              # same column as Q21

    q22_ys = [lo_base_y + i*hbt_sp for i in range(4)]
    q23_ys = [lo_base_y + i*hbt_sp for i in range(4)]
    q24_ys = [lo_base_y + i*hbt_sp for i in range(4)]
    q25_ys = [lo_base_y + i*hbt_sp for i in range(4)]

    # --- Bias transistors: Q26 (Nx=1), Q27 (Nx=1) ---
    q26_x = cx - 50
    q26_y = cy + 110
    q27_x = cx + 40
    q27_y = cy - 100

    # Place all npn instances
    if npn_idx is not None:
        for qy in q20_ys:
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q20_x), um(qy))))
        for qy in q21_ys:
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q21_x), um(qy))))
        for qy in q22_ys:
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q22_x), um(qy))))
        for qy in q23_ys:
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q23_x), um(qy))))
        for qy in q24_ys:
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q24_x), um(qy))))
        for qy in q25_ys:
            mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q25_x), um(qy))))
        mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q26_x), um(q26_y))))
        mixer.insert(pya.CellInstArray(npn_idx, pya.Trans(um(q27_x), um(q27_y))))

    print("Placed 26 npn13G2L instances (4+4+4+4+4+4+1+1)")

    # Pin center positions
    q20_px = q20_x + pcx
    q21_px = q21_x + pcx
    q22_px = q22_x + pcx
    q23_px = q23_x + pcx
    q24_px = q24_x + pcx
    q25_px = q25_x + pcx
    q26_px = q26_x + pcx
    q27_px = q27_x + pcx

    # ================================================================
    # RESISTORS (parameterized rppd via pdk_devices)
    # ================================================================
    # R21: w=3.0u, l=18.23u, m=2, P=2V4, M=2V4
    r21_x, r21_y = 40.0, cy + 130
    r21_pins = create_rppd(mixer, layout, r21_x, r21_y, 3.0, 18.23, m=2)

    # R22: w=3.0u, l=18.23u, m=2, P=2V4, M=2V4
    r22_x, r22_y = 60.0, cy + 130
    r22_pins = create_rppd(mixer, layout, r22_x, r22_y, 3.0, 18.23, m=2)

    # R23: w=3.0u, l=27.48u, m=1, P=2V4, M=net1
    r23_x, r23_y = 80.0, cy + 130
    r23_pins = create_rppd(mixer, layout, r23_x, r23_y, 3.0, 27.48, m=1)

    # R24: w=3.0u, l=27.48u, m=1, P=2V4, M=2V4
    r24_x, r24_y = 92.0, cy + 130
    r24_pins = create_rppd(mixer, layout, r24_x, r24_y, 3.0, 27.48, m=1)

    print("Placed 4 rppd (parameterized)")

    # ================================================================
    # CAPACITORS (cmim)
    # ================================================================
    if cmim_idx is not None:
        # C37: LOP — LOP_I
        mixer.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx - 55), um(cy + 55))))
        # C38: LON — LON_I
        mixer.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx + 42), um(cy + 55))))
        # C39: RFP — RFP_I
        mixer.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx - 55), um(cy - 80))))
        # C40: RFN — RFN_I
        mixer.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx + 42), um(cy - 80))))
        # C41-C43: 2V4 — GND (supply bypass, near VCC rail)
        for i in range(3):
            mixer.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(200 + i * 20), um(cy + 150))))
    print("Placed 7 cap_cmim")

    # ================================================================
    # ROUTING — Match schematic net connectivity
    # ================================================================

    # --- Net ELOL (M3): Q20.C + Q22.E + Q23.E ---
    elol_bus_x = q23_px - 5.0
    # Q20.C: M1 → M3
    for qy in q20_ys:
        via_n(q20_px, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(q20_px, qy+col_dy, 'M2', 'Via2', 'M3')
    # Q22.E (M2) → M3
    for qy in q22_ys:
        via_n(q22_px, qy+emi_dy, 'M2', 'Via2', 'M3')
    # Q23.E (M2) → M3
    for qy in q23_ys:
        via_n(q23_px, qy+emi_dy, 'M2', 'Via2', 'M3')
    # M3 vertical bus
    elol_y_min = q20_ys[0] + col_dy
    elol_y_max = q23_ys[3] + emi_dy
    vwire('M3', elol_bus_x, elol_y_min, elol_y_max)
    # Stubs to Q20.C
    for qy in q20_ys:
        hwire('M3', elol_bus_x, q20_px, qy+col_dy)
    # Stubs to Q22.E
    for qy in q22_ys:
        hwire('M3', elol_bus_x, q22_px, qy+emi_dy)
    # Stubs to Q23.E
    for qy in q23_ys:
        hwire('M3', elol_bus_x, q23_px, qy+emi_dy)

    # --- Net ELOR (M3): Q21.C + Q24.E + Q25.E ---
    elor_bus_x = q24_px + 5.0
    for qy in q21_ys:
        via_n(q21_px, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(q21_px, qy+col_dy, 'M2', 'Via2', 'M3')
    for qy in q24_ys:
        via_n(q24_px, qy+emi_dy, 'M2', 'Via2', 'M3')
    for qy in q25_ys:
        via_n(q25_px, qy+emi_dy, 'M2', 'Via2', 'M3')
    elor_y_min = q21_ys[0] + col_dy
    elor_y_max = q24_ys[3] + emi_dy
    vwire('M3', elor_bus_x, elor_y_min, elor_y_max)
    for qy in q21_ys:
        hwire('M3', q21_px, elor_bus_x, qy+col_dy)
    for qy in q24_ys:
        hwire('M3', q24_px, elor_bus_x, qy+emi_dy)
    for qy in q25_ys:
        hwire('M3', q25_px, elor_bus_x, qy+emi_dy)

    # --- Net GND (M4): Q20.E + Q21.E + Q27.E ---
    # Route emitters to OFFSET X positions to avoid overlap with base M4 stubs
    gnd_hy = q20_ys[0] + emi_dy - 5.0
    q20_esc_x = 120.0   # left escape for Q20 emitters
    q21_esc_x = 180.0   # right escape for Q21 emitters
    q27_esc_x = 200.0   # right escape for Q27 emitter
    # Q20.E: route M2 left to escape, via up to M4
    for qy in q20_ys:
        hwire('M2', q20_esc_x, q20_px, qy+emi_dy)
        via_n(q20_esc_x, qy+emi_dy, 'M2', 'Via2', 'M3')
        via_n(q20_esc_x, qy+emi_dy, 'M3', 'Via3', 'M4')
    # Q21.E: route M2 right to escape, via up to M4
    for qy in q21_ys:
        hwire('M2', q21_px, q21_esc_x, qy+emi_dy)
        via_n(q21_esc_x, qy+emi_dy, 'M2', 'Via2', 'M3')
        via_n(q21_esc_x, qy+emi_dy, 'M3', 'Via3', 'M4')
    # Q27.E: route M2 right to escape, via up to M4
    hwire('M2', q27_px, q27_esc_x, q27_y+emi_dy)
    via_n(q27_esc_x, q27_y+emi_dy, 'M2', 'Via2', 'M3')
    via_n(q27_esc_x, q27_y+emi_dy, 'M3', 'Via3', 'M4')
    # M4 vertical buses at escape positions
    vwire('M4', q20_esc_x, gnd_hy, q20_ys[3]+emi_dy)
    vwire('M4', q21_esc_x, gnd_hy, q21_ys[3]+emi_dy)
    # M4 horizontal connecting all GND columns
    hwire('M4', q20_esc_x, q27_esc_x, gnd_hy)
    # Q27 vertical to GND bus
    vwire('M4', q27_esc_x, q27_y+emi_dy, gnd_hy)

    # --- Net RFP_I (M4): Q20.B ---
    rfp_bus_x = q20_px - 5.0
    for qy in q20_ys:
        via_n(q20_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(q20_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(q20_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        hwire('M4', rfp_bus_x, q20_px, qy+bas_dy)
    vwire('M4', rfp_bus_x, q20_ys[0]+bas_dy, q20_ys[3]+bas_dy)

    # --- Net RFN_I (M4): Q21.B ---
    rfn_bus_x = q21_px + 5.0
    for qy in q21_ys:
        via_n(q21_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(q21_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(q21_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        hwire('M4', q21_px, rfn_bus_x, qy+bas_dy)
    vwire('M4', rfn_bus_x, q21_ys[0]+bas_dy, q21_ys[3]+bas_dy)

    # --- Net LOP_I (M5): Q22.B + Q24.B ---
    lop_hy = q22_ys[0] + bas_dy - 3.0
    for qy in q22_ys:
        via_n(q22_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(q22_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(q22_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(q22_px, qy+bas_dy, 'M4', 'Via4', 'M5')
    for qy in q24_ys:
        via_n(q24_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(q24_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(q24_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(q24_px, qy+bas_dy, 'M4', 'Via4', 'M5')
    vwire('M5', q22_px, q22_ys[0]+bas_dy, q22_ys[3]+bas_dy)
    vwire('M5', q24_px, q24_ys[0]+bas_dy, q24_ys[3]+bas_dy)
    hwire('M5', q22_px, q24_px, lop_hy)
    vwire('M5', q22_px, lop_hy, q22_ys[0]+bas_dy)
    vwire('M5', q24_px, lop_hy, q24_ys[0]+bas_dy)

    # --- Net LON_I (M5): Q23.B + Q25.B ---
    lon_hy = q23_ys[3] + bas_dy + 3.0
    for qy in q23_ys:
        via_n(q23_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(q23_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(q23_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(q23_px, qy+bas_dy, 'M4', 'Via4', 'M5')
    for qy in q25_ys:
        via_n(q25_px, qy+bas_dy, 'M1', 'Via1', 'M2')
        via_n(q25_px, qy+bas_dy, 'M2', 'Via2', 'M3')
        via_n(q25_px, qy+bas_dy, 'M3', 'Via3', 'M4')
        via_n(q25_px, qy+bas_dy, 'M4', 'Via4', 'M5')
    vwire('M5', q23_px, q23_ys[0]+bas_dy, q23_ys[3]+bas_dy)
    vwire('M5', q25_px, q25_ys[0]+bas_dy, q25_ys[3]+bas_dy)
    hwire('M5', q23_px, q25_px, lon_hy)
    vwire('M5', q23_px, q23_ys[3]+bas_dy, lon_hy)
    vwire('M5', q25_px, q25_ys[3]+bas_dy, lon_hy)

    # --- Net 2V4 (M3 rail): Q22.C + R21.P + R21.M + R22.P + R22.M + R23.P + R24.P + R24.M + C41-C43.c0 ---
    # VCC/2V4 rail on M3 at top of cell
    vcc_rail_y = cy + 125
    mixer.shapes(ly['M3']).insert(pya.Box(um(10), um(vcc_rail_y), um(CELL_W - 10), um(vcc_rail_y + 2.0)))
    # Q22.C → escape RIGHT to x=136 on M1, then via to M4, M4 vertical to VCC rail
    q22c_esc_x = 136.0
    for qy in q22_ys:
        hwire('M1', q22_px, q22c_esc_x, qy+col_dy)
        via_n(q22c_esc_x, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(q22c_esc_x, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(q22c_esc_x, qy+col_dy, 'M3', 'Via3', 'M4')
    vwire('M4', q22c_esc_x, q22_ys[0]+col_dy, vcc_rail_y)
    # Connect M4 to M3 VCC rail at top
    via_n(q22c_esc_x, vcc_rail_y, 'M3', 'Via3', 'M4')
    # R21, R22, R23, R24 top pins (P) connect to VCC rail via M1 stubs
    # R21.M, R22.M, R24.M also connect to VCC rail
    # The rppd P pin is at top, M pin is at bottom
    # Route resistor pins to VCC rail on M1→M3
    for pins in [r21_pins, r22_pins, r24_pins]:
        px, py = pins['P']
        via_n(px, py, 'M1', 'Via1', 'M2')
        via_n(px, py, 'M2', 'Via2', 'M3')
        vwire('M3', px, py, vcc_rail_y)
        mx, my = pins['M']
        via_n(mx, my, 'M1', 'Via1', 'M2')
        via_n(mx, my, 'M2', 'Via2', 'M3')
        vwire('M3', mx, my, vcc_rail_y)
    # R23.M (bottom pin = schematic P = 2V4) connects to VCC rail
    mx, my = r23_pins['M']
    via_n(mx, my, 'M1', 'Via1', 'M2')
    via_n(mx, my, 'M2', 'Via2', 'M3')
    vwire('M3', mx, my, vcc_rail_y)
    # R23.P (top pin = schematic M = net1) is floating — no routing needed

    # --- Net IFN (M4): Q23.C + Q24.C ---
    # Escape collectors to offset X to avoid crossing base/emitter M3/M4 pads
    ifn_hy = q23_ys[0] + col_dy - 3.0
    q23c_esc_x = 108.0  # left of ELOL bus (111.1)
    q24c_esc_x = 192.0  # right of ELOR bus (188.9)
    for qy in q23_ys:
        hwire('M1', q23c_esc_x, q23_px, qy+col_dy)
        via_n(q23c_esc_x, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(q23c_esc_x, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(q23c_esc_x, qy+col_dy, 'M3', 'Via3', 'M4')
    for qy in q24_ys:
        hwire('M1', q24_px, q24c_esc_x, qy+col_dy)
        via_n(q24c_esc_x, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(q24c_esc_x, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(q24c_esc_x, qy+col_dy, 'M3', 'Via3', 'M4')
    vwire('M4', q23c_esc_x, ifn_hy, q23_ys[3]+col_dy)
    vwire('M4', q24c_esc_x, ifn_hy, q24_ys[3]+col_dy)
    hwire('M4', q23c_esc_x, q24c_esc_x, ifn_hy)

    # --- Net IFP (M4): Q25.C ---
    # Escape RIGHT to avoid crossing base M3/M4 pads in column
    q25c_esc_x = 175.0
    for qy in q25_ys:
        hwire('M1', q25_px, q25c_esc_x, qy+col_dy)
        via_n(q25c_esc_x, qy+col_dy, 'M1', 'Via1', 'M2')
        via_n(q25c_esc_x, qy+col_dy, 'M2', 'Via2', 'M3')
        via_n(q25c_esc_x, qy+col_dy, 'M3', 'Via3', 'M4')
    vwire('M4', q25c_esc_x, q25_ys[0]+col_dy, q25_ys[3]+col_dy)

    # --- Net BIAS (M3): Q26.C + Q26.B (diode-connected) ---
    # Escape Q26.C and Q26.B on M1 LEFT to x=95, via there to M3
    q26_esc_x = 95.0
    hwire('M1', q26_esc_x, q26_px, q26_y+col_dy)
    via_n(q26_esc_x, q26_y+col_dy, 'M1', 'Via1', 'M2')
    via_n(q26_esc_x, q26_y+col_dy, 'M2', 'Via2', 'M3')
    hwire('M1', q26_esc_x, q26_px, q26_y+bas_dy)
    via_n(q26_esc_x, q26_y+bas_dy, 'M1', 'Via1', 'M2')
    via_n(q26_esc_x, q26_y+bas_dy, 'M2', 'Via2', 'M3')
    # Connect C and B on M3 (vertical at escape X)
    vwire('M3', q26_esc_x, q26_y+bas_dy, q26_y+col_dy)

    # --- Net BIAS_MID (M3): Q26.E + Q27.C + Q27.B ---
    # Q26.E: via M2→M3 at pin position (no M1 conflict)
    via_n(q26_px, q26_y+emi_dy, 'M2', 'Via2', 'M3')
    # Q27.C and Q27.B: escape on M1 RIGHT to x=205, via there to M3
    q27_esc_x = 205.0
    hwire('M1', q27_px, q27_esc_x, q27_y+col_dy)
    via_n(q27_esc_x, q27_y+col_dy, 'M1', 'Via1', 'M2')
    via_n(q27_esc_x, q27_y+col_dy, 'M2', 'Via2', 'M3')
    hwire('M1', q27_px, q27_esc_x, q27_y+bas_dy)
    via_n(q27_esc_x, q27_y+bas_dy, 'M1', 'Via1', 'M2')
    via_n(q27_esc_x, q27_y+bas_dy, 'M2', 'Via2', 'M3')
    # Connect Q27.C and Q27.B on M3 (diode) at escape X
    vwire('M3', q27_esc_x, q27_y+bas_dy, q27_y+col_dy)
    # Connect Q26.E to Q27.C/B net via M3 horizontal
    bm_route_y = q26_y + emi_dy
    hwire('M3', q26_px, q27_esc_x, bm_route_y)
    vwire('M3', q27_esc_x, q27_y+col_dy, bm_route_y)

    # ================================================================
    # PORT LABELS (for LVS extraction)
    # ================================================================
    # GND port label on M4 GND bus
    mixer.shapes(ly['M4']).insert(pya.Text("GND", pya.Trans(um(cx), um(gnd_hy))))
    # 2V4 port on M3 VCC rail
    mixer.shapes(ly['M3']).insert(pya.Text("2V4", pya.Trans(um(cx), um(vcc_rail_y + 1.0))))
    # RFP_I — connect to cap C39 (need label on the net connecting Q20.B and C39)
    mixer.shapes(ly['M4']).insert(pya.Text("RFP_I", pya.Trans(um(rfp_bus_x), um(q20_ys[2]+bas_dy))))
    # RFN_I
    mixer.shapes(ly['M4']).insert(pya.Text("RFN_I", pya.Trans(um(rfn_bus_x), um(q21_ys[2]+bas_dy))))

    # External port labels (these become top-level ports in extraction)
    # RFP, RFN on caps C39, C40 far side
    # LOP, LON on caps C37, C38 far side
    # IFP on Q25.C net, IFN on Q23.C+Q24.C net
    mixer.shapes(ly['M4']).insert(pya.Text("IFP", pya.Trans(um(q25c_esc_x), um(q25_ys[0]+col_dy))))
    mixer.shapes(ly['M4']).insert(pya.Text("IFN", pya.Trans(um(cx), um(ifn_hy))))

    # LOP/LON port labels on M5 LO nets
    mixer.shapes(ly['M5']).insert(pya.Text("LOP_I", pya.Trans(um(cx), um(lop_hy))))
    mixer.shapes(ly['M5']).insert(pya.Text("LON_I", pya.Trans(um(cx), um(lon_hy))))

    # BIAS label
    mixer.shapes(ly['M3']).insert(pya.Text("BIAS", pya.Trans(um(q26_esc_x), um(q26_y+col_dy))))
    # BIAS_MID label
    mixer.shapes(ly['M3']).insert(pya.Text("BIAS_MID", pya.Trans(um(q27_esc_x), um(q27_y+col_dy))))

    print("Routing complete")

    # ================================================================
    # OUTPUT
    # ================================================================
    if ext_layout is None:
        output = "/home/bthomas3/Videos/77GHz_phased_array/layout/MIXER_77G_XTOR.gds"
        layout.write(output)
        print(f"\nMixer layout: {output}")
        print(f"Cell size: {CELL_W} x {CELL_H} um")
        print(f"Devices: 26x npn13G2L + 4x rppd + 7x cmim")


if __name__ == "__main__":
    main()
