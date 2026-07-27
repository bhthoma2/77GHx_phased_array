"""
77 GHz VCO Layout Generator — IHP SG13G2 PDK
Generates GDS for the cross-coupled VCO with TL stubs

Metal stack (SG13G2):
  Metal1: 8/0    Metal2: 10/0   Metal3: 30/0
  Metal4: 50/0   Metal5: 67/0
  TopMetal1: 126/0  TopMetal2: 134/0
  Via1: 19/0  Via2: 29/0  Via3: 49/0  Via4: 66/0
  TopVia1: 125/0  TopVia2: 133/0

TLs on TopMetal2 (3µm thick Al, lowest loss at 77 GHz)
Ground plane on Metal5 or TopMetal1
"""

import pya

# --- Layer definitions ---
LAYERS = {
    'M1': (8, 0),
    'Via1': (19, 0),
    'M2': (10, 0),
    'Via2': (29, 0),
    'M3': (30, 0),
    'Via3': (49, 0),
    'M4': (50, 0),
    'Via4': (66, 0),
    'M5': (67, 0),
    'TopVia1': (125, 0),
    'TM1': (126, 0),
    'TopVia2': (133, 0),
    'TM2': (134, 0),
}

# --- Design parameters (µm) ---
# TL parameters (microstrip on TopMetal2 over TopMetal1 ground)
TL_WIDTH = 5.0        # Signal line width (µm) — meets TM2.bR rule
TL_GND_WIDTH = 20.0   # Ground plane width each side
TL_GAP = 3.0          # Gap between signal and ground (CPW)

# VCO dimensions
STUB_LEN = 135.0      # Resonator stub length (µm)
CHOKE_LEN = 105.0     # DC feed choke length (µm)
PAIR_SPACING = 30.0   # Spacing between diff pair outputs
CELL_WIDTH = 200.0    # Total cell width
CELL_HEIGHT = 400.0   # Total cell height

# Transistor placement (npn13G2l Nx=2)
HBT_WIDTH = 5.0       # HBT emitter stripe width
HBT_HEIGHT = 10.0     # HBT cell height

DBU = 0.001  # database unit = 1nm


def um(val):
    """Convert µm to database units"""
    return int(val / DBU)


def create_cpw_tl(cell, layer_sig, layer_gnd, x0, y0, length, direction='up'):
    """Create a coplanar waveguide transmission line segment"""
    w = um(TL_WIDTH)
    g = um(TL_GAP)
    gw = um(TL_GND_WIDTH)
    l = um(length)

    if direction == 'up':
        # Signal trace
        cell.shapes(layer_sig).insert(pya.Box(
            um(x0) - w//2, um(y0), um(x0) + w//2, um(y0) + l))
        # Ground left
        cell.shapes(layer_gnd).insert(pya.Box(
            um(x0) - w//2 - g - gw, um(y0),
            um(x0) - w//2 - g, um(y0) + l))
        # Ground right
        cell.shapes(layer_gnd).insert(pya.Box(
            um(x0) + w//2 + g, um(y0),
            um(x0) + w//2 + g + gw, um(y0) + l))
    elif direction == 'right':
        cell.shapes(layer_sig).insert(pya.Box(
            um(x0), um(y0) - w//2, um(x0) + l, um(y0) + w//2))
        cell.shapes(layer_gnd).insert(pya.Box(
            um(x0), um(y0) + w//2 + g,
            um(x0) + l, um(y0) + w//2 + g + gw))
        cell.shapes(layer_gnd).insert(pya.Box(
            um(x0), um(y0) - w//2 - g - gw,
            um(x0) + l, um(y0) - w//2 - g))

    return (x0, y0 + length) if direction == 'up' else (x0 + length, y0)


def create_hbt_symbol(cell, layer, x, y, label="Q"):
    """Place HBT symbol (placeholder rectangle)"""
    w = um(HBT_WIDTH)
    h = um(HBT_HEIGHT)
    cell.shapes(layer).insert(pya.Box(um(x) - w//2, um(y) - h//2,
                                       um(x) + w//2, um(y) + h//2))


def create_mim_cap(cell, layer_top, layer_bot, x, y, w_um, l_um):
    """Create MIM capacitor (TM1 over M5)"""
    cell.shapes(layer_top).insert(pya.Box(
        um(x) - um(w_um)//2, um(y) - um(l_um)//2,
        um(x) + um(w_um)//2, um(y) + um(l_um)//2))
    cell.shapes(layer_bot).insert(pya.Box(
        um(x) - um(w_um)//2 - um(1), um(y) - um(l_um)//2 - um(1),
        um(x) + um(w_um)//2 + um(1), um(y) + um(l_um)//2 + um(1)))


def main():
    layout = pya.Layout()
    layout.dbu = DBU

    # Create layers
    ly = {}
    for name, (ln, dt) in LAYERS.items():
        ly[name] = layout.layer(ln, dt)

    # Top cell
    top = layout.create_cell("VCO_77G")

    # === Ground plane (TopMetal1) — with slots for DRC (Slt.c.TM1) ===
    gnd_margin = 10.0
    slot_pitch = 30.0  # µm between slots
    slot_width = 2.0   # µm slot opening
    gnd_x0 = gnd_margin
    gnd_x1 = CELL_WIDTH - gnd_margin
    gnd_y0 = gnd_margin
    gnd_y1 = CELL_HEIGHT - gnd_margin

    # Create ground plane as strips (avoiding slots in signal path)
    y = gnd_y0
    while y < gnd_y1:
        strip_top = min(y + slot_pitch - slot_width, gnd_y1)
        top.shapes(ly['TM1']).insert(pya.Box(
            um(gnd_x0), um(y), um(gnd_x1), um(strip_top)))
        y += slot_pitch

    # Cut slots in ground plane for TL signal routing
    cx = CELL_WIDTH / 2
    cy = CELL_HEIGHT / 2

    # === Resonator stubs (TopMetal2, extending upward from center) ===
    # OUTP stub (left)
    stub_x_left = cx - PAIR_SPACING/2
    stub_x_right = cx + PAIR_SPACING/2
    stub_y_start = cy + 20

    create_cpw_tl(top, ly['TM2'], ly['TM2'], stub_x_left, stub_y_start,
                  STUB_LEN, 'up')
    create_cpw_tl(top, ly['TM2'], ly['TM2'], stub_x_right, stub_y_start,
                  STUB_LEN, 'up')

    # === DC feed chokes (TopMetal2, extending downward from center) ===
    choke_y_start = cy - 20
    create_cpw_tl(top, ly['TM2'], ly['TM2'], stub_x_left,
                  choke_y_start - CHOKE_LEN, CHOKE_LEN, 'up')
    create_cpw_tl(top, ly['TM2'], ly['TM2'], stub_x_right,
                  choke_y_start - CHOKE_LEN, CHOKE_LEN, 'up')

    # === Cross-coupled HBT pair (Metal1/Metal2 level) ===
    hbt_y = cy
    create_hbt_symbol(top, ly['M1'], cx - 10, hbt_y, "Q1")
    create_hbt_symbol(top, ly['M1'], cx + 10, hbt_y, "Q2")

    # === Varactor caps (MIM: TM1 top plate, M5 bottom) ===
    create_mim_cap(top, ly['TM1'], ly['M5'],
                   stub_x_left + 15, stub_y_start + 10, 5, 5)
    create_mim_cap(top, ly['TM1'], ly['M5'],
                   stub_x_right - 15, stub_y_start + 10, 5, 5)

    # === Supply decoupling cap ===
    create_mim_cap(top, ly['TM1'], ly['M5'],
                   cx, cy - 60, 20, 15)

    # === Pads with slots (TM2, 50×50µm with 2µm slots every 15µm) ===
    pad_size = 50.0

    def slotted_pad(cell, layer, x0, y0, size):
        """Create a pad with horizontal slots for DRC compliance"""
        sp = 15.0  # slot pitch
        sw = 2.0   # slot width
        py = y0
        while py < y0 + size:
            h = min(sp - sw, y0 + size - py)
            cell.shapes(layer).insert(pya.Box(um(x0), um(py), um(x0 + size), um(py + h)))
            py += sp

    # VCC pad (top)
    slotted_pad(top, ly['TM2'], cx - pad_size/2, CELL_HEIGHT - pad_size - 10, pad_size)
    # GND pads (bottom corners)
    slotted_pad(top, ly['TM2'], 10, 10, pad_size)
    slotted_pad(top, ly['TM2'], CELL_WIDTH - 10 - pad_size, 10, pad_size)
    # Output pads (left and right)
    slotted_pad(top, ly['TM2'], 10, cy - pad_size/2, pad_size)
    slotted_pad(top, ly['TM2'], CELL_WIDTH - 10 - pad_size, cy - pad_size/2, pad_size)
    # VTUNE pad (bottom center)
    slotted_pad(top, ly['TM2'], cx - pad_size/2, 10, pad_size)

    # === Labels ===
    top.shapes(ly['TM2']).insert(pya.Text("VCC", pya.Trans(um(cx), um(CELL_HEIGHT - 35))))
    top.shapes(ly['TM2']).insert(pya.Text("OUTP", pya.Trans(um(35), um(cy))))
    top.shapes(ly['TM2']).insert(pya.Text("OUTN", pya.Trans(um(CELL_WIDTH - 35), um(cy))))
    top.shapes(ly['TM2']).insert(pya.Text("VTUNE", pya.Trans(um(cx), um(35))))
    top.shapes(ly['TM2']).insert(pya.Text("GND", pya.Trans(um(35), um(35))))
    top.shapes(ly['TM2']).insert(pya.Text("GND", pya.Trans(um(CELL_WIDTH - 35), um(35))))

    # Save GDS
    output_path = "/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G.gds"
    layout.write(output_path)
    print(f"VCO layout written to: {output_path}")
    print(f"Cell size: {CELL_WIDTH} x {CELL_HEIGHT} µm")
    print(f"Resonator stubs: {STUB_LEN} µm (TopMetal2 CPW)")
    print(f"DC chokes: {CHOKE_LEN} µm (TopMetal2 CPW)")
    print(f"Ground plane: TopMetal1")


if __name__ == "__main__":
    main()
