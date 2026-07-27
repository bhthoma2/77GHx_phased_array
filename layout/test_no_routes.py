"""
77 GHz Phased Array Vibrometer — Top-Level Chip Assembly
Single TX/RX channel on IHP SG13G2 (130nm SiGe BiCMOS)
Die size: ~2.0 x 2.0 mm

Signal flow:
  RX: ANT_RX → LNA → Mixer(RF) ← VCO(LO)
  TX: VCO → TXPA → ANT_TX
  CLK: VCO → ILFD → DIV_OUT

Floorplan (2000 x 2000 µm):
  +------------------------------------------+
  |  PAD RING                                |
  |  +------+  +--------+  +------+         |
  |  | LNA  |  | MIXER  |  | VCO  |         |
  |  +------+  +--------+  +------+         |
  |                                          |
  |  +------+             +--------+         |
  |  | ILFD |             | TXPA   |         |
  |  +------+             +--------+         |
  +------------------------------------------+
"""

import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"
OUT_DIR = "/home/bthomas3/Videos/77GHz_phased_array/layout/"

LAYERS = {
    'M1': (8, 0), 'Via1': (19, 0), 'M2': (10, 0), 'Via2': (29, 0),
    'M3': (30, 0), 'Via3': (49, 0), 'M4': (50, 0), 'Via4': (66, 0),
    'M5': (67, 0), 'TopVia1': (125, 0), 'TM1': (126, 0),
    'TopVia2': (133, 0), 'TM2': (134, 0),
}
DBU = 0.001
DIE_W = 2000.0
DIE_H = 2000.0
PAD_SIZE = 70.0
PAD_PITCH = 150.0
PAD_OFFSET = 50.0


def um(val):
    return int(round(val / 0.005) * 0.005 / DBU)


def snap(val):
    return round(val / 0.005) * 0.005


def main():
    layout = pya.Layout()
    layout.dbu = DBU

    # Read all block GDS files
    block_files = {
        'VCO': OUT_DIR + 'VCO_77G_XTOR.gds',
        'LNA': OUT_DIR + 'LNA_77G_XTOR.gds',
        'MIXER': OUT_DIR + 'MIXER_77G_XTOR.gds',
        'TXPA': OUT_DIR + 'TXPA_77G_XTOR.gds',
        'ILFD': OUT_DIR + 'ILFD_77G_XTOR.gds',
    }
    block_cells = {
        'VCO': 'VCO_77G_XTOR',
        'LNA': 'RXAMP_77GD',
        'MIXER': 'MIXER_77GD',
        'TXPA': 'TXAMP_77GD',
        'ILFD': 'ILFD_77GD',
    }
    block_sizes = {
        'VCO': (250.0, 450.0),
        'LNA': (300.0, 500.0),
        'MIXER': (300.0, 450.0),
        'TXPA': (350.0, 550.0),
        'ILFD': (300.0, 600.0),
    }

    # Load PDK first
    layout.read(PDK_GDS)

    # Load each block GDS
    for name, gds_path in block_files.items():
        layout.read(gds_path)

    ly = {}
    for lname, (ln, dt) in LAYERS.items():
        ly[lname] = layout.layer(ln, dt)

    # Create top cell
    top = layout.create_cell("PHASED_ARRAY_77G_TOP")

    # --- BLOCK PLACEMENT ---
    # Row 1 (upper): LNA, MIXER, VCO
    # Row 2 (lower): ILFD, (space), TXPA
    row1_y = 1100.0  # bottom of row 1
    row2_y = 300.0   # bottom of row 2
    margin = 200.0   # from left edge

    placements = {
        'LNA':   (margin, row1_y),
        'MIXER': (margin + 350.0, row1_y + 25.0),
        'VCO':   (margin + 700.0, row1_y + 25.0),
        'ILFD':  (margin, row2_y),
        'TXPA':  (margin + 700.0, row2_y),
    }

    for name, (px, py) in placements.items():
        cell_name = block_cells[name]
        idx = layout.cell_by_name(cell_name)
        if idx is not None:
            top.insert(pya.CellInstArray(idx, pya.Trans(um(px), um(py))))
        else:
            print(f"WARNING: Cell {cell_name} not found, skipping {name}")

    # --- BOND PADS ---
    # Create a generic pad cell (70×70 µm TM2 + opening)
    pad_cell = layout.create_cell("BONDPAD_70")
    pad_cell.shapes(ly['TM2']).insert(pya.Box(0, 0, um(PAD_SIZE), um(PAD_SIZE)))
    pad_cell.shapes(ly['TM1']).insert(pya.Box(um(5), um(5), um(PAD_SIZE-5), um(PAD_SIZE-5)))

    # Pad assignments (name, side, index)
    # Bottom pads (south): GND, VCC, TAIL_BIAS, VCB_BIAS, GND
    # Left pads (west): ANT_RX_P, ANT_RX_N, GND, LNA_BIAS, GND
    # Top pads (north): DIV_OUT_P, DIV_OUT_N, GND, VCC, GND
    # Right pads (east): ANT_TX_P, ANT_TX_N, GND, IF_P, IF_N

    pad_defs = {
        'south': ['GND', 'VCC', 'TAIL_BIAS', 'VCB_BIAS', 'LO_TUNE', 'VCC', 'GND',
                  'INJ_P', 'INJ_N', 'GND'],
        'west':  ['GND', 'ANT_RX_P', 'ANT_RX_N', 'GND', 'LNA_VCC', 'GND',
                  'RF_MON_P', 'RF_MON_N', 'GND', 'GND'],
        'north': ['GND', 'DIV_P', 'DIV_N', 'GND', 'VCC', 'GND',
                  'IF_P', 'IF_N', 'GND', 'GND'],
        'east':  ['GND', 'ANT_TX_P', 'ANT_TX_N', 'GND', 'PA_VCC', 'GND',
                  'VCO_VCC', 'GND', 'VTUNE', 'GND'],
    }

    pad_idx = layout.cell_by_name("BONDPAD_70")
    pad_positions = {}
    pad_margin = 20.0  # margin from die edge to ensure pads fully inside

    for side, names in pad_defs.items():
        n = len(names)
        for i, pname in enumerate(names):
            if side == 'south':
                px = pad_margin + 100.0 + i * PAD_PITCH
                py = pad_margin
            elif side == 'north':
                px = pad_margin + 100.0 + i * PAD_PITCH
                py = DIE_H - pad_margin - PAD_SIZE
            elif side == 'west':
                px = pad_margin
                py = pad_margin + 100.0 + i * PAD_PITCH
            elif side == 'east':
                px = DIE_W - pad_margin - PAD_SIZE
                py = pad_margin + 100.0 + i * PAD_PITCH
            top.insert(pya.CellInstArray(pad_idx, pya.Trans(um(px), um(py))))
            pad_positions[f"{side}_{i}_{pname}"] = (px + PAD_SIZE/2, py + PAD_SIZE/2)
            # Label on M3 (avoid TM2 DRC interactions)
            top.shapes(ly['M3']).insert(pya.Text(pname, pya.Trans(um(px+PAD_SIZE/2), um(py+PAD_SIZE/2))))

    # --- POWER DISTRIBUTION ---
    # VCC mesh on M4 (horizontal stripes every 200µm) — M5 reserved for signal routing
    # Gaps where blocks are placed to avoid shorting to internal M4 routing
    vcc_stripe_w = 3.0
    _pl = placements
    block_boxes = [
        (_pl['LNA'][0], _pl['LNA'][1], _pl['LNA'][0] + 300, _pl['LNA'][1] + 500),
        (_pl['MIXER'][0], _pl['MIXER'][1], _pl['MIXER'][0] + 300, _pl['MIXER'][1] + 450),
        (_pl['VCO'][0], _pl['VCO'][1], _pl['VCO'][0] + 250, _pl['VCO'][1] + 450),
        (_pl['TXPA'][0], _pl['TXPA'][1], _pl['TXPA'][0] + 350, _pl['TXPA'][1] + 550),
        (_pl['ILFD'][0], _pl['ILFD'][1], _pl['ILFD'][0] + 300, _pl['ILFD'][1] + 600),
    ]
    margin = 5.0
    sig_margin = 5.0
    signal_channels = [
        (875.0 - 1.5 - sig_margin, 875.0 + 1.5 + sig_margin),
        (1165.0 - 1.5 - sig_margin, 1165.0 + 1.5 + sig_margin),
        (525.0 - 1.5 - sig_margin, 525.0 + 1.5 + sig_margin),
    ]
    for y in range(300, 1800, 200):
        segments = [(150.0, DIE_W - 150.0)]
        for bx1, by1, bx2, by2 in block_boxes:
            if by1 - margin <= y + vcc_stripe_w and by2 + margin >= y:
                new_segs = []
                for sx, ex in segments:
                    if bx1 - margin > sx:
                        new_segs.append((sx, min(ex, bx1 - margin)))
                    if bx2 + margin < ex:
                        new_segs.append((max(sx, bx2 + margin), ex))
                segments = [(s, e) for s, e in new_segs if e > s]
        for cx1, cx2 in signal_channels:
            new_segs = []
            for sx, ex in segments:
                if cx1 > sx:
                    new_segs.append((sx, min(ex, cx1)))
                if cx2 < ex:
                    new_segs.append((max(sx, cx2), ex))
            segments = [(s, e) for s, e in new_segs if e > s]
        for sx, ex in segments:
            top.shapes(ly['M4']).insert(pya.Box(um(sx), um(y), um(ex), um(y + vcc_stripe_w)))

    # GND mesh on TM1 (slotted ground plane covering die)
    # Slots every 25µm for DRC compliance
    gnd_y = 100.0
    slot_pitch = 25.0
    while gnd_y < DIE_H - 100:
        seg_h = min(22.0, DIE_H - 100 - gnd_y)
        if seg_h > 0:
            top.shapes(ly['TM1']).insert(pya.Box(
                um(100), um(gnd_y), um(DIE_W-100), um(gnd_y+seg_h)))
        gnd_y += slot_pitch

    # --- INTER-BLOCK SIGNAL ROUTING ---
    # Route on M5 (5µm wide traces) with via stacks to connect block ports.
    # Via stacks placed in top cell overlap with block internal bus metals.
    route_w = 3.0  # 3µm wide M5 signal traces (ensures min spacing between adjacent routes)

    def via_stack_top(x, y, bot_layer, top_layer):
        """Place via stack from bot_layer to top_layer at (x,y) in top cell"""
        x, y = snap(x), snap(y)
        stack = [
            ('M3', 'Via3', 'M4', 0.19, 0.5),
            ('M4', 'Via4', 'M5', 0.19, 0.5),
            ('M5', 'TopVia1', 'TM1', 0.42, 5.0),
            ('TM1', 'TopVia2', 'TM2', 0.9, 5.0),
        ]
        started = False
        for bot, via, top_l, vs, ps in stack:
            if bot == bot_layer:
                started = True
            if started:
                cx, cy = um(x), um(y)
                v = um(snap(vs))
                p = um(snap(ps))
                top.shapes(ly[bot]).insert(pya.Box(cx-p//2, cy-p//2, cx+p//2, cy+p//2))
                top.shapes(ly[via]).insert(pya.Box(cx-v//2, cy-v//2, cx+v//2, cy+v//2))
                top.shapes(ly[top_l]).insert(pya.Box(cx-p//2, cy-p//2, cx+p//2, cy+p//2))
            if top_l == top_layer:
                break

    # Block positions
    vco_x, vco_y = placements['VCO']     # (900, 1125)
    mix_x, mix_y = placements['MIXER']   # (550, 1125)
    lna_x, lna_y = placements['LNA']     # (200, 1100)
    txpa_x, txpa_y = placements['TXPA']  # (900, 300)
    ilfd_x, ilfd_y = placements['ILFD']  # (200, 300)

    # === INTER-BLOCK SIGNAL ROUTING ===
    # CRITICAL: Routes must stay in CHANNELS between blocks (never cross block
    # interiors on M5, which have internal M5 routing that would short).
    #
    # Block bounding boxes:
    #   LNA:  (200,1100)-(500,1600)    Mixer: (550,1125)-(850,1575)
    #   VCO:  (900,1125)-(1150,1575)   TXPA:  (900,300)-(1250,850)
    #   ILFD: (200,300)-(500,900)
    #
    # Available routing channels:
    #   Horizontal: y=900-1100 (between upper and lower rows)
    #               y=1575-2000 (above upper row)
    #   Vertical:   x=500-550 (LNA-Mixer gap)
    #               x=850-900 (Mixer-VCO gap)
    #               x=1150-2000 (right of VCO/TXPA)
    #               x=0-200 (left of LNA/ILFD)

    # Port positions (absolute coordinates)
    vco_outp_x = vco_x + 144.0    # 1044
    vco_outn_x = vco_x + 139.0    # 1039
    vco_port_y = vco_y + 219.0    # 1344

    mix_lop_y = mix_y + 263.775   # 1388.775
    mix_lon_y = mix_y + 279.775   # 1404.775
    mix_lo_x = mix_x + 150.0     # 700

    mix_rfp_x = mix_x + 123.1    # 673.1
    mix_rfn_x = mix_x + 173.0    # 723.0
    mix_rf_y = mix_y + 200.0     # 1325.0

    lna_outp_x = lna_x + 121.2   # 321.2
    lna_outn_x = lna_x + 178.8   # 378.8
    lna_port_y = lna_y + 310.0   # 1410.0

    txpa_inp_x = txpa_x + 143.7  # 1043.7
    txpa_inn_x = txpa_x + 206.3  # 1106.3
    txpa_port_y = txpa_y + 250.0 # 550.0

    ilfd_injp_x = ilfd_x + 125.7 # 325.7
    ilfd_injn_x = ilfd_x + 174.3 # 374.3
    ilfd_port_y = ilfd_y + 266.0  # 566.0

    # === INTER-BLOCK ROUTING (Over-Under Topology) ===
    ENABLE_ROUTES = False
    # OUTP signals route on M5; OUTN signals route on M4 in channel regions.
    # This eliminates all same-layer crossings between differential pairs.
    # Single channel X positions work because P and N are on different layers.
    lo_chan_x = 875.0   # LO channel (Mixer-VCO gap x=850-900)
    rf_chan_x = 525.0   # RF channel (LNA-Mixer gap x=500-550)
    tx_chan_x = 1165.0  # TX channel (right of VCO/TXPA, x=1150+)


    # === 5. POWER CONNECTIONS: Block VCC M3 rails → M5 VCC mesh ===
    # Each block has an M3 VCC rail near its top. Place via stacks (M3→M5)
    # at multiple points along each block's VCC rail to connect to M5 mesh.
    def vcc_taps(block_x, block_y, rail_y_in_cell, cell_w, n_taps=4):
        """Connect block M3 VCC rail to M5 VCC mesh with n_taps via stacks"""
        abs_rail_y = block_y + rail_y_in_cell
        for i in range(n_taps):
            tap_x = block_x + cell_w * (i + 1) / (n_taps + 1)
            via_stack_top(tap_x, abs_rail_y, 'M3', 'M4')

    # Exact VCC rail Y centers within each block (from generate scripts):
    # LNA: Box(10, cy+285, W-10, cy+295) → cy=250, center y=540, W=300
    # Mixer: Box(10, cy+130, W-10, cy+140) → cy=225, center y=360, W=300
    # TXPA: Box(10, cy+325, W-10, cy+335) → cy=275, center y=605, W=350
    # ILFD: Box(10, cy+295, W-10, cy+305) → cy=300, center y=600, W=300
    # VCO: no M3 VCC rail (uses TM1 for Cdecap VCC)
    vcc_taps(lna_x, lna_y, 540.0, 300.0, 5)
    vcc_taps(mix_x, mix_y, 360.0, 300.0, 5)
    vcc_taps(txpa_x, txpa_y, 605.0, 350.0, 6)
    vcc_taps(ilfd_x, ilfd_y, 600.0, 300.0, 5)

    # === 6. GROUND CONNECTIONS: TM1 GND plane → M1 substrate rings ===
    # Place via stacks from TM1 down to M1 at block corners for substrate ground
    def gnd_taps(block_x, block_y, cell_w, cell_h):
        """Connect TM1 ground plane to M1 at block corners"""
        corners = [
            (block_x + 15, block_y + 15),
            (block_x + cell_w - 15, block_y + 15),
            (block_x + 15, block_y + cell_h - 15),
            (block_x + cell_w - 15, block_y + cell_h - 15),
        ]
        for gx, gy in corners:
            # Full stack: M1→Via1→M2→Via2→M3→Via3→M4→Via4→M5→TopVia1→TM1
            via_stack_top(gx, gy, 'M3', 'TM1')
            # Also need M1→M3 portion
            gx_s, gy_s = snap(gx), snap(gy)
            cx_i, cy_i = um(gx_s), um(gy_s)
            ps = um(0.5)
            vs = um(0.19)
            # M1 pad
            top.shapes(ly['M1']).insert(pya.Box(cx_i-ps//2, cy_i-ps//2, cx_i+ps//2, cy_i+ps//2))
            top.shapes(ly['Via1']).insert(pya.Box(cx_i-vs//2, cy_i-vs//2, cx_i+vs//2, cy_i+vs//2))
            top.shapes(ly['M2']).insert(pya.Box(cx_i-ps//2, cy_i-ps//2, cx_i+ps//2, cy_i+ps//2))
            top.shapes(ly['Via2']).insert(pya.Box(cx_i-vs//2, cy_i-vs//2, cx_i+vs//2, cy_i+vs//2))
            top.shapes(ly['M3']).insert(pya.Box(cx_i-ps//2, cy_i-ps//2, cx_i+ps//2, cy_i+ps//2))

    gnd_taps(lna_x, lna_y, 300.0, 500.0)
    gnd_taps(mix_x, mix_y, 300.0, 450.0)
    gnd_taps(vco_x, vco_y, 250.0, 450.0)
    gnd_taps(txpa_x, txpa_y, 350.0, 550.0)
    gnd_taps(ilfd_x, ilfd_y, 300.0, 600.0)

    # === 7. PAD-TO-SIGNAL/POWER ROUTING ===
    # Connect bond pads (TM2) to internal signals via TM2→TopVia2→TM1→TopVia1→M5
    def pad_to_m5(pad_cx, pad_cy):
        """Place via stack from TM2 pad down to M5"""
        via_stack_top(pad_cx, pad_cy, 'M5', 'TM2')

    # Power pads → M5 VCC mesh (connect pad to nearest VCC stripe)
    # VCC pads: south_1, south_5, north_4, east_4 (PA_VCC), east_6 (VCO_VCC), west_4 (LNA_VCC)
    # GND pads connect to TM1 ground (already overlapping since pads have TM1)

    # Route signal pads to block ports with M5 traces
    # ANT_RX pads (west_1, west_2) → LNA input
    ant_rxp_pad = pad_positions.get('west_1_ANT_RX_P', (55.0, 270.0))
    ant_rxn_pad = pad_positions.get('west_2_ANT_RX_N', (55.0, 420.0))
    pad_to_m5(ant_rxp_pad[0], ant_rxp_pad[1])
    pad_to_m5(ant_rxn_pad[0], ant_rxn_pad[1])

    # ANT_TX pads (east_1, east_2) → TXPA output
    ant_txp_pad = pad_positions.get('east_1_ANT_TX_P', (1945.0, 270.0))
    ant_txn_pad = pad_positions.get('east_2_ANT_TX_N', (1945.0, 420.0))
    pad_to_m5(ant_txp_pad[0], ant_txp_pad[1])
    pad_to_m5(ant_txn_pad[0], ant_txn_pad[1])

    # IF output pads (north_6, north_7) → Mixer IF output
    ifp_pad = pad_positions.get('north_6_IF_P', (1020.0, 1945.0))
    ifn_pad = pad_positions.get('north_7_IF_N', (1170.0, 1945.0))
    pad_to_m5(ifp_pad[0], ifp_pad[1])
    pad_to_m5(ifn_pad[0], ifn_pad[1])

    # VTUNE pad (east_8) → VCO tuning
    vtune_pad = pad_positions.get('east_8_VTUNE', (1945.0, 1320.0))
    pad_to_m5(vtune_pad[0], vtune_pad[1])

    # DIV output pads (north_1, north_2) → ILFD output
    divp_pad = pad_positions.get('north_1_DIV_P', (270.0, 1945.0))
    divn_pad = pad_positions.get('north_2_DIV_N', (420.0, 1945.0))
    pad_to_m5(divp_pad[0], divp_pad[1])
    pad_to_m5(divn_pad[0], divn_pad[1])

    # M5 traces from pads to block ports (visible routing)
    # ANT_RX_P pad → LNA INP (M4 bus at lna_x+121.2, lna_y+217)
    lna_inp_x = lna_x + 121.2
    lna_inp_y = lna_y + 217.0
    via_stack_top(lna_inp_x, lna_inp_y, 'M4', 'M5')
    top.shapes(ly['M5']).insert(pya.Box(
        um(ant_rxp_pad[0] - route_w/2), um(ant_rxp_pad[1] - route_w/2),
        um(lna_inp_x + route_w/2), um(ant_rxp_pad[1] + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(lna_inp_x - route_w/2), um(lna_inp_y - route_w/2),
        um(lna_inp_x + route_w/2), um(ant_rxp_pad[1] + route_w/2)))

    # ANT_RX_N pad → LNA INN (M4 bus at lna_x+178.8, lna_y+217)
    lna_inn_x = lna_x + 178.8
    via_stack_top(lna_inn_x, lna_inp_y, 'M4', 'M5')
    top.shapes(ly['M5']).insert(pya.Box(
        um(ant_rxn_pad[0] - route_w/2), um(ant_rxn_pad[1] - route_w/2),
        um(lna_inn_x + route_w/2), um(ant_rxn_pad[1] + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(lna_inn_x - route_w/2), um(lna_inp_y - route_w/2),
        um(lna_inn_x + route_w/2), um(ant_rxn_pad[1] + route_w/2)))

    # ANT_TX_P pad → TXPA OUTP (M4 bus at txpa_x+143.7, txpa_y+380)
    txpa_outp_x = txpa_x + 143.7
    txpa_outp_y = txpa_y + 380.0
    via_stack_top(txpa_outp_x, txpa_outp_y, 'M4', 'M5')
    top.shapes(ly['M5']).insert(pya.Box(
        um(txpa_outp_x - route_w/2), um(txpa_outp_y - route_w/2),
        um(ant_txp_pad[0] + route_w/2), um(txpa_outp_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(ant_txp_pad[0] - route_w/2), um(txpa_outp_y - route_w/2),
        um(ant_txp_pad[0] + route_w/2), um(ant_txp_pad[1] + route_w/2)))

    # ANT_TX_N pad → TXPA OUTN (M4 bus at txpa_x+206.3, txpa_y+380)
    txpa_outn_x = txpa_x + 206.3
    via_stack_top(txpa_outn_x, txpa_outp_y, 'M4', 'M5')
    top.shapes(ly['M5']).insert(pya.Box(
        um(txpa_outn_x - route_w/2), um(txpa_outp_y + 10 - route_w/2),
        um(ant_txn_pad[0] + route_w/2), um(txpa_outp_y + 10 + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(ant_txn_pad[0] - route_w/2), um(txpa_outp_y + 10 - route_w/2),
        um(ant_txn_pad[0] + route_w/2), um(ant_txn_pad[1] + route_w/2)))

    print("Power, ground, and pad connections added")

    # --- DIE SEAL RING (M1 perimeter, single closed ring to avoid corner spacing) ---
    seal_w = 5.0
    # Use a single polygon (ring) to avoid M1.b spacing at corners
    outer = pya.Box(um(0), um(0), um(DIE_W), um(DIE_H))
    inner = pya.Box(um(seal_w), um(seal_w), um(DIE_W-seal_w), um(DIE_H-seal_w))
    ring = pya.Region(outer) - pya.Region(inner)
    top.shapes(ly['M1']).insert(ring)

    # --- OUTPUT ---
    output = OUT_DIR + "test_no_routes.gds"
    layout.write(output)
    print(f"Top-level chip: {output}")
    print(f"Die size: {DIE_W} x {DIE_H} µm ({DIE_W/1000:.1f} x {DIE_H/1000:.1f} mm)")
    print(f"Blocks placed: VCO, LNA, MIXER, TXPA, ILFD")
    print(f"Pads: {sum(len(v) for v in pad_defs.values())} total")
    print(f"Inter-block routes: LO (VCO→Mixer), RF (LNA→Mixer), TX (VCO→TXPA), INJ (VCO→ILFD)")


if __name__ == "__main__":
    main()