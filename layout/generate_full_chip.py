"""
77 GHz 4×4 Phased Array — Full Chip Layout
IHP SG13G2 PDK, Die size: 2.5 × 2.5 mm

Floorplan:
  ┌─────────────────────────────────────────────┐
  │  PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD    │
  │ P┌───────────────────────────────────────┐P │
  │ A│  [EL00] [EL01] [EL02] [EL03]         │A │
  │ D│  [EL10] [EL11] [EL12] [EL13]         │D │
  │  │         ┌─────────┐                   │  │
  │ P│         │VCO+PLL  │                   │P │
  │ A│         │ILFD+DIV │                   │A │
  │ D│         └─────────┘                   │D │
  │  │  [EL20] [EL21] [EL22] [EL23]         │  │
  │ P│  [EL30] [EL31] [EL32] [EL33]         │P │
  │ A└───────────────────────────────────────┘A │
  │ D PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD D │
  └─────────────────────────────────────────────┘

Each element: LNA + Mixer + Phase Shifter (RX path)
              PA + Phase Shifter (TX path)
Element size: ~300 × 400 µm
"""

import pya

LAYERS = {
    'M1': (8, 0), 'Via1': (19, 0), 'M2': (10, 0), 'Via2': (29, 0),
    'M3': (30, 0), 'Via3': (49, 0), 'M4': (50, 0), 'Via4': (66, 0),
    'M5': (67, 0), 'TopVia1': (125, 0), 'TM1': (126, 0),
    'TopVia2': (133, 0), 'TM2': (134, 0),
}

DBU = 0.001
DIE_W = 2500.0   # µm (2.5mm)
DIE_H = 2500.0
PAD_SIZE = 70.0  # bond pad
PAD_PITCH = 150.0
PAD_MARGIN = 50.0
SEAL_WIDTH = 15.0

ELEM_W = 300.0   # element cell width
ELEM_H = 400.0   # element cell height
VCO_W = 200.0
VCO_H = 400.0
PLL_W = 300.0
PLL_H = 300.0

ARRAY_COLS = 4
ARRAY_ROWS = 4


def um(val):
    return int(val / DBU)


def create_slotted_rect(cell, layer, x0, y0, w, h, slot_pitch=25.0, slot_w=2.0):
    """Rectangle with horizontal slots for DRC compliance"""
    y = y0
    while y < y0 + h:
        sh = min(slot_pitch - slot_w, y0 + h - y)
        if sh > 0:
            cell.shapes(layer).insert(pya.Box(um(x0), um(y), um(x0 + w), um(y + sh)))
        y += slot_pitch


def create_pad(cell, layer, cx, cy, label=""):
    """Create a bond pad with label"""
    ps = PAD_SIZE
    create_slotted_rect(cell, layer, cx - ps/2, cy - ps/2, ps, ps)
    if label:
        cell.shapes(layer).insert(pya.Text(label, pya.Trans(um(cx), um(cy))))


def create_element_cell(layout, ly, name="ELEMENT"):
    """Create a phased array element (LNA + Mixer + PS + PA)"""
    cell = layout.create_cell(name)

    # Outline (M1 boundary marker)
    cell.shapes(ly['M1']).insert(pya.Box(0, 0, um(ELEM_W), um(ELEM_H)))

    # LNA block (top)
    lna_y = ELEM_H - 100
    create_slotted_rect(cell, ly['TM2'], 20, lna_y, 100, 80)
    cell.shapes(ly['TM2']).insert(pya.Text("LNA", pya.Trans(um(70), um(lna_y + 40))))

    # Mixer (middle-top)
    mix_y = lna_y - 100
    create_slotted_rect(cell, ly['TM2'], 20, mix_y, 80, 80)
    cell.shapes(ly['TM2']).insert(pya.Text("MIX", pya.Trans(um(60), um(mix_y + 40))))

    # Phase shifter (middle)
    ps_y = mix_y - 100
    create_slotted_rect(cell, ly['TM2'], 20, ps_y, 260, 80)
    cell.shapes(ly['TM2']).insert(pya.Text("PS", pya.Trans(um(150), um(ps_y + 40))))

    # PA (bottom)
    pa_y = 20
    create_slotted_rect(cell, ly['TM2'], 150, pa_y, 130, 80)
    cell.shapes(ly['TM2']).insert(pya.Text("PA", pya.Trans(um(215), um(pa_y + 40))))

    # IF output connection (M5 trace going down)
    cell.shapes(ly['M5']).insert(pya.Box(um(130), um(mix_y), um(140), um(mix_y + 80)))

    # TL interconnects (TM2 signal lines)
    cell.shapes(ly['TM2']).insert(pya.Box(um(65), um(ps_y + 80), um(70), um(mix_y)))
    cell.shapes(ly['TM2']).insert(pya.Box(um(65), um(lna_y), um(70), um(lna_y - 20 + 100)))

    # Ground plane (TM1)
    create_slotted_rect(cell, ly['TM1'], 5, 5, ELEM_W - 10, ELEM_H - 10)

    return cell


def main():
    layout = pya.Layout()
    layout.dbu = DBU

    ly = {}
    for name, (ln, dt) in LAYERS.items():
        ly[name] = layout.layer(ln, dt)

    # Create top cell
    top = layout.create_cell("PHASED_ARRAY_77G")

    # === Seal ring (TM2 frame around die) ===
    sw = SEAL_WIDTH
    top.shapes(ly['TM2']).insert(pya.Box(um(0), um(0), um(DIE_W), um(sw)))
    top.shapes(ly['TM2']).insert(pya.Box(um(0), um(DIE_H - sw), um(DIE_W), um(DIE_H)))
    top.shapes(ly['TM2']).insert(pya.Box(um(0), um(0), um(sw), um(DIE_H)))
    top.shapes(ly['TM2']).insert(pya.Box(um(DIE_W - sw), um(0), um(DIE_W), um(DIE_H)))

    # === Bond pads (perimeter) ===
    pad_labels_bottom = ["GND", "VCC", "VTUNE", "IF0", "IF1", "IF2", "IF3", "CLK", "GND", "VCC"]
    pad_labels_top = ["GND", "VCC", "TX0", "TX1", "TX2", "TX3", "REF", "PLL_VCC", "GND", "VCC"]
    pad_labels_left = ["GND", "RX0", "RX1", "RX2", "RX3", "LO_OUT", "GND"]
    pad_labels_right = ["GND", "RX4", "RX5", "RX6", "RX7", "BIAS", "GND"]

    # Bottom pads
    for i, lbl in enumerate(pad_labels_bottom):
        x = PAD_MARGIN + PAD_PITCH/2 + i * PAD_PITCH
        create_pad(top, ly['TM2'], x, PAD_MARGIN + PAD_SIZE/2, lbl)

    # Top pads
    for i, lbl in enumerate(pad_labels_top):
        x = PAD_MARGIN + PAD_PITCH/2 + i * PAD_PITCH
        create_pad(top, ly['TM2'], x, DIE_H - PAD_MARGIN - PAD_SIZE/2, lbl)

    # Left pads
    for i, lbl in enumerate(pad_labels_left):
        y = PAD_MARGIN + PAD_SIZE + PAD_PITCH + i * PAD_PITCH
        create_pad(top, ly['TM2'], PAD_MARGIN + PAD_SIZE/2, y, lbl)

    # Right pads
    for i, lbl in enumerate(pad_labels_right):
        y = PAD_MARGIN + PAD_SIZE + PAD_PITCH + i * PAD_PITCH
        create_pad(top, ly['TM2'], DIE_W - PAD_MARGIN - PAD_SIZE/2, y, lbl)

    # === Array elements (4×4) ===
    elem_cell = create_element_cell(layout, ly)

    array_x0 = (DIE_W - ARRAY_COLS * ELEM_W) / 2
    array_y0 = (DIE_H - ARRAY_ROWS * ELEM_H) / 2 + 100  # offset up slightly

    for row in range(ARRAY_ROWS):
        for col in range(ARRAY_COLS):
            x = array_x0 + col * ELEM_W
            y = array_y0 + row * ELEM_H
            # Skip center 2×2 for VCO/PLL
            if row in [1, 2] and col in [1, 2]:
                continue
            inst = top.insert(pya.CellInstArray(
                elem_cell.cell_index(),
                pya.Trans(um(x), um(y))))

    # === VCO + PLL block (center) ===
    vco_x = array_x0 + 1 * ELEM_W + 50
    vco_y = array_y0 + 1 * ELEM_H + 50
    create_slotted_rect(top, ly['TM2'], vco_x, vco_y, PLL_W, PLL_H)
    create_slotted_rect(top, ly['TM1'], vco_x - 5, vco_y - 5, PLL_W + 10, PLL_H + 10)
    top.shapes(ly['TM2']).insert(pya.Text("VCO+PLL+ILFD",
        pya.Trans(um(vco_x + PLL_W/2), um(vco_y + PLL_H/2))))

    # === Wilkinson distribution network (TM2 traces from VCO to elements) ===
    vco_cx = vco_x + PLL_W/2
    vco_cy = vco_y + PLL_H/2
    tw = 5.0  # trace width

    # Radial traces to each element
    for row in range(ARRAY_ROWS):
        for col in range(ARRAY_COLS):
            if row in [1, 2] and col in [1, 2]:
                continue
            ex = array_x0 + col * ELEM_W + ELEM_W/2
            ey = array_y0 + row * ELEM_H + ELEM_H/2
            # Horizontal then vertical routing
            if ex < vco_cx:
                top.shapes(ly['M5']).insert(pya.Box(
                    um(ex), um(min(ey, vco_cy) - tw/2),
                    um(vco_cx), um(min(ey, vco_cy) + tw/2)))
            else:
                top.shapes(ly['M5']).insert(pya.Box(
                    um(vco_cx), um(min(ey, vco_cy) - tw/2),
                    um(ex), um(min(ey, vco_cy) + tw/2)))
            # Vertical segment
            top.shapes(ly['M5']).insert(pya.Box(
                um(ex - tw/2), um(min(ey, vco_cy)),
                um(ex + tw/2), um(max(ey, vco_cy))))

    # === Title ===
    top.shapes(ly['TM2']).insert(pya.Text(
        "77GHz 4x4 PHASED ARRAY VIBROMETER - IHP SG13G2",
        pya.Trans(um(DIE_W/2), um(DIE_H - 30))))

    # Save
    output_path = "/home/bthomas3/Videos/77GHz_phased_array/layout/PHASED_ARRAY_77G.gds"
    layout.write(output_path)
    print(f"Full chip layout: {output_path}")
    print(f"Die size: {DIE_W} x {DIE_H} µm ({DIE_W/1000:.1f} x {DIE_H/1000:.1f} mm)")
    print(f"Array: {ARRAY_COLS}x{ARRAY_ROWS} elements")
    print(f"Element size: {ELEM_W} x {ELEM_H} µm")
    print(f"Total pads: {len(pad_labels_bottom) + len(pad_labels_top) + len(pad_labels_left) + len(pad_labels_right)}")


if __name__ == "__main__":
    main()
