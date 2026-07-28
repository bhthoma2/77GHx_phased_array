"""
IF Amplifier (IFA) — Transistor-Level Layout
2-stage differential amplifier with BJT current sources on IHP SG13G2
Matches IFA_77G_LVS.sch: 7×npn13G2l + 7×rppd + 2×cap_cmim
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
CELL_W = 250.0
CELL_H = 350.0
OUT_DIR = "/home/bthomas3/Videos/77GHz_phased_array/layout/"


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
    rppd_idx = layout.cell_by_name("rppd") if layout.has_cell("rppd") else None

    ifa = layout.create_cell("IFA_77GD")
    cx = CELL_W / 2
    cy = CELL_H / 2

    hbt_spacing = 10.0
    pair_gap = 30.0

    if npn_idx is not None:
        # Stage 1 diff pair: Q1 (left, 2 instances), Q2 (right, 2 instances)
        for i in range(2):
            ifa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8), um(cy + 40 + i * hbt_spacing))))
        for i in range(2):
            ifa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2), um(cy + 40 + i * hbt_spacing))))

        # Stage 2 diff pair: Q3 (left, 2 instances), Q4 (right, 2 instances)
        for i in range(2):
            ifa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - pair_gap/2 - 7.8), um(cy - 60 + i * hbt_spacing))))
        for i in range(2):
            ifa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + pair_gap/2), um(cy - 60 + i * hbt_spacing))))

        # Tail current source Q5 (stage 1)
        ifa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - 5), um(cy + 20))))
        # Tail current source Q6 (stage 2)
        ifa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx - 5), um(cy - 80))))
        # Bias reference Q7 (diode-connected)
        ifa.insert(pya.CellInstArray(npn_idx, pya.Trans(um(cx + 60), um(cy - 20))))

    # Load resistors R1-R4 (500Ω each)
    if rppd_idx is not None:
        # R1: Stage 1 left load
        ifa.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx - 45), um(cy + 80))))
        # R2: Stage 1 right load
        ifa.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx + 37), um(cy + 80))))
        # R3: Stage 2 left load
        ifa.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx - 45), um(cy - 30))))
        # R4: Stage 2 right load
        ifa.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx + 37), um(cy - 30))))
        # R5: Bias resistor (VCC to Q7 base/collector)
        ifa.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx + 60), um(cy + 10))))
        # R6: Q7 emitter degeneration
        ifa.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx + 60), um(cy - 50))))
        # R7: Tail degeneration
        ifa.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx - 5), um(cy - 100))))

    # Bypass caps C1, C2
    if cmim_idx is not None:
        ifa.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx + 85), um(cy + 60))))
        ifa.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx + 85), um(cy + 30))))

    # --- Port labels on TM2 ---
    ly_tm2 = ly['TM2']
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

    # Ground plane (TM1, slotted)
    slot_pitch = 25.0
    slot_w = 4.0
    y = 5.0
    while y < CELL_H - 5:
        sh = min(slot_pitch - slot_w, CELL_H - 5 - y)
        if sh > 0:
            x = 5.0
            while x < CELL_W - 5:
                sw = min(slot_pitch - slot_w, CELL_W - 5 - x)
                if sw > 0:
                    ifa.shapes(ly['TM1']).insert(pya.Box(um(x), um(y), um(x + sw), um(y + sh)))
                x += slot_pitch
        y += slot_pitch

    # M3 power ring
    ring_w = 5.0
    ifa.shapes(ly['M3']).insert(pya.Box(um(10), um(10), um(CELL_W-10), um(10+ring_w)))
    ifa.shapes(ly['M3']).insert(pya.Box(um(10), um(CELL_H-10-ring_w), um(CELL_W-10), um(CELL_H-10)))
    ifa.shapes(ly['M3']).insert(pya.Box(um(10), um(10), um(10+ring_w), um(CELL_H-10)))
    ifa.shapes(ly['M3']).insert(pya.Box(um(CELL_W-10-ring_w), um(10), um(CELL_W-10), um(CELL_H-10)))

    if ext_layout is None:
        output = f"{OUT_DIR}IFA_77G_XTOR.gds"
        layout.write(output)
        print(f"IFA layout: {output}")
        print(f"Cell: {CELL_W}×{CELL_H}µm")
        print(f"Devices: 7×npn13G2L + 7×rppd + 2×cmim")

    return ifa


if __name__ == "__main__":
    main()