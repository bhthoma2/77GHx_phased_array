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
import sys
sys.path.insert(0, "/home/bthomas3/Videos/77GHz_phased_array/layout")
import generate_vco_transistor as gen_vco
import generate_lna_transistor as gen_lna
import generate_mixer_transistor as gen_mixer
import generate_txpa_transistor as gen_txpa
import generate_ilfd_transistor as gen_ilfd
import generate_bias_network as gen_bias

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

    block_cells = {
        'VCO': 'VCO_77G_XTOR',
        'LNA': 'RXAMP_77GD',
        'MIXER': 'MIXER_77GD',
        'TXPA': 'TXAMP_77GD',
        'ILFD': 'ILFD_77GD',
        'BIAS': 'BIAS_NETWORK',
    }
    block_sizes = {
        'VCO': (250.0, 450.0),
        'LNA': (300.0, 500.0),
        'MIXER': (300.0, 450.0),
        'TXPA': (350.0, 550.0),
        'ILFD': (300.0, 600.0),
        'BIAS': (200.0, 300.0),
    }

    # Load PDK primitives once, then generate all blocks in this layout
    layout.read(PDK_GDS)
    gen_vco.main(layout)
    gen_lna.main(layout)
    gen_mixer.main(layout)
    gen_txpa.main(layout)
    gen_ilfd.main(layout)
    gen_bias.main(layout)

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
        'BIAS':  (550.0, 500.0),
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

    # --- GND PAD → TM1 GROUND MESH CONNECTIONS ---
    # TM1 mesh covers (100,100)-(1900,1900). Pads at edges need TM1 strips.
    gnd_pad_keys = [k for k in pad_positions if 'GND' in k]
    for gk in gnd_pad_keys:
        pcx, pcy = pad_positions[gk]
        # TM1 strip from pad center toward mesh edge (10µm wide)
        sw = 10.0
        if pcy < 100:  # south — extend up to mesh
            top.shapes(ly['TM1']).insert(pya.Box(
                um(pcx - sw/2), um(pcy - 30), um(pcx + sw/2), um(122)))
        elif pcy > 1900:  # north — extend down to mesh
            top.shapes(ly['TM1']).insert(pya.Box(
                um(pcx - sw/2), um(1878), um(pcx + sw/2), um(pcy + 30)))
        elif pcx < 100:  # west — extend right to mesh
            top.shapes(ly['TM1']).insert(pya.Box(
                um(pcx - 30), um(pcy - sw/2), um(122), um(pcy + sw/2)))
        elif pcx > 1900:  # east — extend left to mesh
            top.shapes(ly['TM1']).insert(pya.Box(
                um(1878), um(pcy - sw/2), um(pcx + 30), um(pcy + sw/2)))

    # --- VCC PAD → M4 MESH CONNECTIONS ---
    # M4 mesh is horizontal stripes at y=300,500,700,...,1700. Pads at edges
    # need M4 stubs to reach the nearest stripe.
    vcc_stripe_w = 3.0
    vcc_positions = []
    for pk in ['south_1_VCC', 'south_5_VCC', 'north_4_VCC',
               'east_4_PA_VCC', 'east_6_VCO_VCC', 'west_4_LNA_VCC']:
        if pk in pad_positions:
            vcc_positions.append(pad_positions[pk])
    for pcx, pcy in vcc_positions:
        # Find nearest M4 mesh stripe Y
        nearest_y = min(range(300, 1800, 200), key=lambda ys: abs(ys - pcy))
        # M4 vertical stub from pad to nearest stripe
        y_lo = min(pcy, nearest_y)
        y_hi = max(pcy, nearest_y + vcc_stripe_w)
        top.shapes(ly['M4']).insert(pya.Box(
            um(pcx - 1.5), um(y_lo), um(pcx + 1.5), um(y_hi)))
        # M4 horizontal stub at stripe Y to ensure overlap with mesh
        x_lo = min(pcx, 150.0)
        x_hi = max(pcx, DIE_W - 150.0)
        # Only need short overlap — extend 20µm toward die center
        if pcx < 200:
            top.shapes(ly['M4']).insert(pya.Box(
                um(pcx - 1.5), um(nearest_y), um(pcx + 50), um(nearest_y + vcc_stripe_w)))
        elif pcx > 1800:
            top.shapes(ly['M4']).insert(pya.Box(
                um(pcx - 50), um(nearest_y), um(pcx + 1.5), um(nearest_y + vcc_stripe_w)))
        # South/north pads: vertical reaches mesh, horizontal already exists at mesh Y

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
        (_pl['BIAS'][0], _pl['BIAS'][1], _pl['BIAS'][0] + 200, _pl['BIAS'][1] + 300),
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
    # OUTP signals route on M5; OUTN signals route on M4 in channel regions.
    # This eliminates all same-layer crossings between differential pairs.
    # Single channel X positions work because P and N are on different layers.
    lo_chan_x = 875.0   # LO channel (Mixer-VCO gap x=850-900)
    rf_chan_x = 525.0   # RF channel (LNA-Mixer gap x=500-550)
    tx_chan_x = 1165.0  # TX channel (right of VCO/TXPA, x=1150+)

    # ------------------------------------------------------------------
    # 1. LO_P (VCO OUTP → Mixer LO_P) — M5
    # Path: VCO port(1044,1344) → up to y=1354 → left to channel x=875
    #       → up to y=1389 → left into Mixer at y=1389
    # ------------------------------------------------------------------
    outp_h_y = vco_port_y + 10.0  # 1354 (offset to clear OUTN port at x=1039)
    via_stack_top(vco_outp_x, vco_port_y, 'M3', 'M5')
    # Vertical from port up to routing Y
    top.shapes(ly['M5']).insert(pya.Box(
        um(vco_outp_x - route_w/2), um(vco_port_y - route_w/2),
        um(vco_outp_x + route_w/2), um(outp_h_y + route_w/2)))
    # Horizontal left to channel
    top.shapes(ly['M5']).insert(pya.Box(
        um(lo_chan_x - route_w/2), um(outp_h_y - route_w/2),
        um(vco_outp_x + route_w/2), um(outp_h_y + route_w/2)))
    # Channel vertical up to Mixer LO_P Y
    top.shapes(ly['M5']).insert(pya.Box(
        um(lo_chan_x - route_w/2), um(outp_h_y - route_w/2),
        um(lo_chan_x + route_w/2), um(mix_lop_y + route_w/2)))
    # Horizontal left into Mixer
    top.shapes(ly['M5']).insert(pya.Box(
        um(mix_lo_x - route_w/2), um(mix_lop_y - route_w/2),
        um(lo_chan_x + route_w/2), um(mix_lop_y + route_w/2)))

    # ------------------------------------------------------------------
    # 2. LO_N (VCO OUTN → Mixer LO_N) — M4 in channel, M5 stub into Mixer
    # ------------------------------------------------------------------
    outn_h_y = vco_port_y - 10.0  # 1334
    mix_r_edge = mix_x + 300.0    # 850 (Mixer right edge)
    # M4: VCO port vertical (connects to OUTN M4 bus at cell y=219)
    top.shapes(ly['M4']).insert(pya.Box(
        um(vco_outn_x - route_w/2), um(outn_h_y - route_w/2),
        um(vco_outn_x + route_w/2), um(vco_port_y + route_w/2)))
    # M4: horizontal from channel to VCO OUTN (through VCO at cell y=209)
    top.shapes(ly['M4']).insert(pya.Box(
        um(lo_chan_x - route_w/2), um(outn_h_y - route_w/2),
        um(vco_outn_x + route_w/2), um(outn_h_y + route_w/2)))
    # M4: channel vertical up to Mixer right edge Y
    top.shapes(ly['M4']).insert(pya.Box(
        um(lo_chan_x - route_w/2), um(outn_h_y - route_w/2),
        um(lo_chan_x + route_w/2), um(mix_lon_y + route_w/2)))
    # M4: horizontal from channel to Mixer right edge
    top.shapes(ly['M4']).insert(pya.Box(
        um(mix_r_edge - route_w/2), um(mix_lon_y - route_w/2),
        um(lo_chan_x + route_w/2), um(mix_lon_y + route_w/2)))
    # Via M4→M5 at Mixer right edge
    via_stack_top(mix_r_edge, mix_lon_y, 'M4', 'M5')
    # M5 stub into Mixer to LO_N port pad
    top.shapes(ly['M5']).insert(pya.Box(
        um(mix_lo_x - route_w/2), um(mix_lon_y - route_w/2),
        um(mix_r_edge + route_w/2), um(mix_lon_y + route_w/2)))

    # ------------------------------------------------------------------
    # 3. RF_P (LNA OUTP → Mixer RF_P) — M5
    # ------------------------------------------------------------------
    via_stack_top(lna_outp_x, lna_port_y, 'M4', 'M5')
    via_stack_top(mix_rfp_x, mix_rf_y, 'M4', 'M5')
    lna_p_route_y = lna_port_y + 5.0
    mix_p_rf_y = mix_rf_y + 5.0
    top.shapes(ly['M5']).insert(pya.Box(
        um(lna_outp_x - route_w/2), um(lna_port_y - route_w/2),
        um(lna_outp_x + route_w/2), um(lna_p_route_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(lna_outp_x - route_w/2), um(lna_p_route_y - route_w/2),
        um(rf_chan_x + route_w/2), um(lna_p_route_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(rf_chan_x - route_w/2), um(mix_p_rf_y - route_w/2),
        um(rf_chan_x + route_w/2), um(lna_p_route_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(rf_chan_x - route_w/2), um(mix_p_rf_y - route_w/2),
        um(mix_rfp_x + route_w/2), um(mix_p_rf_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(mix_rfp_x - route_w/2), um(mix_rf_y - route_w/2),
        um(mix_rfp_x + route_w/2), um(mix_p_rf_y + route_w/2)))

    # ------------------------------------------------------------------
    # 4. RF_N (LNA OUTN → Mixer RF_N) — M4 in channel, M5 stubs into blocks
    # ------------------------------------------------------------------
    lna_r_edge = lna_x + 300.0   # 500 (LNA right edge)
    mix_l_edge = mix_x           # 550 (Mixer left edge)
    lna_n_route_y = lna_port_y - 5.0  # 1405
    mix_n_rf_y = mix_rf_y - 5.0       # 1320
    # M5 stub: LNA OUTN port to LNA right edge
    via_stack_top(lna_outn_x, lna_port_y, 'M4', 'M5')
    top.shapes(ly['M5']).insert(pya.Box(
        um(lna_outn_x - route_w/2), um(lna_n_route_y - route_w/2),
        um(lna_outn_x + route_w/2), um(lna_port_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(lna_outn_x - route_w/2), um(lna_n_route_y - route_w/2),
        um(lna_r_edge + route_w/2), um(lna_n_route_y + route_w/2)))
    # Via M5→M4 at LNA right edge
    via_stack_top(lna_r_edge, lna_n_route_y, 'M4', 'M5')
    # M4: channel from LNA edge to Mixer edge
    top.shapes(ly['M4']).insert(pya.Box(
        um(lna_r_edge - route_w/2), um(lna_n_route_y - route_w/2),
        um(rf_chan_x + route_w/2), um(lna_n_route_y + route_w/2)))
    top.shapes(ly['M4']).insert(pya.Box(
        um(rf_chan_x - route_w/2), um(mix_n_rf_y - route_w/2),
        um(rf_chan_x + route_w/2), um(lna_n_route_y + route_w/2)))
    top.shapes(ly['M4']).insert(pya.Box(
        um(rf_chan_x - route_w/2), um(mix_n_rf_y - route_w/2),
        um(mix_l_edge + route_w/2), um(mix_n_rf_y + route_w/2)))
    # Via M4→M5 at Mixer left edge
    via_stack_top(mix_l_edge, mix_n_rf_y, 'M4', 'M5')
    # M5 stub: Mixer left edge to RF_N port
    top.shapes(ly['M5']).insert(pya.Box(
        um(mix_l_edge - route_w/2), um(mix_n_rf_y - route_w/2),
        um(mix_rfn_x + route_w/2), um(mix_n_rf_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(mix_rfn_x - route_w/2), um(mix_rf_y - route_w/2),
        um(mix_rfn_x + route_w/2), um(mix_n_rf_y + route_w/2)))

    # ------------------------------------------------------------------
    # 5. TX_P (VCO OUTP → TXPA INP) — M5
    # ------------------------------------------------------------------
    via_stack_top(txpa_inp_x, txpa_port_y, 'M4', 'M5')
    txpa_p_entry_y = txpa_port_y + 10.0
    top.shapes(ly['M5']).insert(pya.Box(
        um(vco_outp_x - route_w/2), um(vco_port_y - route_w/2),
        um(tx_chan_x + route_w/2), um(vco_port_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(tx_chan_x - route_w/2), um(txpa_p_entry_y - route_w/2),
        um(tx_chan_x + route_w/2), um(vco_port_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(txpa_inp_x - route_w/2), um(txpa_p_entry_y - route_w/2),
        um(tx_chan_x + route_w/2), um(txpa_p_entry_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(txpa_inp_x - route_w/2), um(txpa_port_y - route_w/2),
        um(txpa_inp_x + route_w/2), um(txpa_p_entry_y + route_w/2)))

    # ------------------------------------------------------------------
    # 6. TX_N (VCO OUTN → TXPA INN) — M4 in channel, M5 stub into TXPA
    # ------------------------------------------------------------------
    txpa_r_edge = txpa_x + 350.0  # 1250 (TXPA right edge)
    txpa_n_entry_y = txpa_port_y - 10.0  # 540
    tx_outn_h_y = vco_port_y - 10.0      # 1334
    # M4: extend from LO_N OUTN horizontal (at vco_outn_x) right to TX channel
    top.shapes(ly['M4']).insert(pya.Box(
        um(vco_outn_x - route_w/2), um(tx_outn_h_y - route_w/2),
        um(tx_chan_x + route_w/2), um(tx_outn_h_y + route_w/2)))
    # M4: channel vertical down to TXPA top edge
    top.shapes(ly['M4']).insert(pya.Box(
        um(tx_chan_x - route_w/2), um(txpa_n_entry_y - route_w/2),
        um(tx_chan_x + route_w/2), um(tx_outn_h_y + route_w/2)))
    # M4: horizontal from channel to TXPA right edge (extend past via)
    top.shapes(ly['M4']).insert(pya.Box(
        um(txpa_r_edge + route_w/2), um(txpa_n_entry_y - route_w/2),
        um(tx_chan_x + route_w/2), um(txpa_n_entry_y + route_w/2)))
    # Via M4→M5 at TXPA right edge
    via_stack_top(txpa_r_edge, txpa_n_entry_y, 'M4', 'M5')
    # M5 stub into TXPA to INN port
    top.shapes(ly['M5']).insert(pya.Box(
        um(txpa_inn_x - route_w/2), um(txpa_n_entry_y - route_w/2),
        um(txpa_r_edge + route_w/2), um(txpa_n_entry_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(txpa_inn_x - route_w/2), um(txpa_n_entry_y - route_w/2),
        um(txpa_inn_x + route_w/2), um(txpa_port_y + 3.0)))

    # ------------------------------------------------------------------
    # 7. INJ_P (VCO OUTP → ILFD INJ_P) — M5, branches off LO_P channel
    # ------------------------------------------------------------------
    via_stack_top(ilfd_injp_x, ilfd_port_y, 'M4', 'M5')
    inj_h_y_p = 1010.0
    top.shapes(ly['M5']).insert(pya.Box(
        um(lo_chan_x - route_w/2), um(inj_h_y_p - route_w/2),
        um(lo_chan_x + route_w/2), um(outp_h_y + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(ilfd_injp_x - route_w/2), um(inj_h_y_p - route_w/2),
        um(lo_chan_x + route_w/2), um(inj_h_y_p + route_w/2)))
    top.shapes(ly['M5']).insert(pya.Box(
        um(ilfd_injp_x - route_w/2), um(ilfd_port_y - route_w/2),
        um(ilfd_injp_x + route_w/2), um(inj_h_y_p + route_w/2)))

    # ------------------------------------------------------------------
    # 8. INJ_N (VCO OUTN → ILFD INJ_N) — M4 in channel, M5 stub into ILFD
    # Route: branch off LO_N M4 at lo_chan_x, go down to y=1025, left to
    # ilfd_injn_x, down to ILFD top edge (y=910), via to M5, stub into ILFD.
    # ------------------------------------------------------------------
    inj_h_y_n = 1025.0
    ilfd_top_y = ilfd_y + 600.0 + 10.0  # 910 (just above ILFD top)
    # M4: extend LO_N channel vertical down from outn_h_y to inj_h_y_n
    top.shapes(ly['M4']).insert(pya.Box(
        um(lo_chan_x - route_w/2), um(inj_h_y_n - route_w/2),
        um(lo_chan_x + route_w/2), um(outn_h_y + route_w/2)))
    # M4: horizontal left from lo_chan_x to ilfd_injn_x at inj_h_y_n
    top.shapes(ly['M4']).insert(pya.Box(
        um(ilfd_injn_x - route_w/2), um(inj_h_y_n - route_w/2),
        um(lo_chan_x + route_w/2), um(inj_h_y_n + route_w/2)))
    # M4: vertical down from inj_h_y_n to ilfd_top_y
    top.shapes(ly['M4']).insert(pya.Box(
        um(ilfd_injn_x - route_w/2), um(ilfd_top_y - route_w/2),
        um(ilfd_injn_x + route_w/2), um(inj_h_y_n + route_w/2)))
    # Via M4→M5 at ILFD top edge
    via_stack_top(ilfd_injn_x, ilfd_top_y, 'M4', 'M5')
    # M5: stub down into ILFD to INJ_N port
    top.shapes(ly['M5']).insert(pya.Box(
        um(ilfd_injn_x - route_w/2), um(ilfd_port_y - route_w/2),
        um(ilfd_injn_x + route_w/2), um(ilfd_top_y + route_w/2)))

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

    # ANT_TX_P pad → TXPA OUTP — route on TM2 (M5 has TX_P vertical at x=1165)
    txpa_outp_x = txpa_x + 143.7
    txpa_outp_y = txpa_y + 380.0
    via_stack_top(txpa_outp_x, txpa_outp_y, 'M5', 'TM2')
    top.shapes(ly['TM2']).insert(pya.Box(
        um(txpa_outp_x - route_w/2), um(txpa_outp_y - route_w/2),
        um(ant_txp_pad[0] + route_w/2), um(txpa_outp_y + route_w/2)))
    top.shapes(ly['TM2']).insert(pya.Box(
        um(ant_txp_pad[0] - route_w/2), um(txpa_outp_y - route_w/2),
        um(ant_txp_pad[0] + route_w/2), um(ant_txp_pad[1] + route_w/2)))

    # ANT_TX_N pad → TXPA OUTN — route on TM2
    txpa_outn_x = txpa_x + 206.3
    via_stack_top(txpa_outn_x, txpa_outp_y, 'M5', 'TM2')
    top.shapes(ly['TM2']).insert(pya.Box(
        um(txpa_outn_x - route_w/2), um(txpa_outp_y + 10 - route_w/2),
        um(ant_txn_pad[0] + route_w/2), um(txpa_outp_y + 10 + route_w/2)))
    top.shapes(ly['TM2']).insert(pya.Box(
        um(ant_txn_pad[0] - route_w/2), um(txpa_outp_y + 10 - route_w/2),
        um(ant_txn_pad[0] + route_w/2), um(ant_txn_pad[1] + route_w/2)))

    # ------------------------------------------------------------------
    # VCC pads → M4 VCC mesh via stacks (TM2→TM1→M5→M4)
    # All VCC pads are at die edges, far from M5 signal routes
    # ------------------------------------------------------------------
    vcc_pad_keys = ['south_1_VCC', 'south_5_VCC', 'north_4_VCC',
                    'east_4_PA_VCC', 'east_6_VCO_VCC', 'west_4_LNA_VCC']
    for pk in vcc_pad_keys:
        if pk in pad_positions:
            pcx, pcy = pad_positions[pk]
            via_stack_top(pcx, pcy, 'M4', 'TM2')

    # ------------------------------------------------------------------
    # IF_P/N pads (north_6, north_7) → Mixer IF output ports
    # Route on TM2 from pad down to Mixer area, then via to M5 at port
    # Mixer IF at (mix_x+123.1, mix_y+420) = (673.1, 1545)
    # ------------------------------------------------------------------
    mix_ifp_x = mix_x + 123.1   # 673.1
    mix_ifn_x = mix_x + 173.0   # 723.0
    mix_if_y = mix_y + 420.0    # 1545.0

    # IF_P: TM2 L-route from pad to above Mixer, then via to M5 at port
    ifp_tm2_x = mix_ifp_x + 20.0  # offset to avoid Mixer TM2 CPW
    top.shapes(ly['TM2']).insert(pya.Box(
        um(ifp_tm2_x - route_w/2), um(mix_if_y + 30 - route_w/2),
        um(ifp_pad[0] + route_w/2), um(mix_if_y + 30 + route_w/2)))
    top.shapes(ly['TM2']).insert(pya.Box(
        um(ifp_pad[0] - route_w/2), um(mix_if_y + 30 - route_w/2),
        um(ifp_pad[0] + route_w/2), um(ifp_pad[1] + route_w/2)))
    top.shapes(ly['TM2']).insert(pya.Box(
        um(ifp_tm2_x - route_w/2), um(mix_if_y - route_w/2),
        um(ifp_tm2_x + route_w/2), um(mix_if_y + 30 + route_w/2)))
    via_stack_top(ifp_tm2_x, mix_if_y, 'M5', 'TM2')
    top.shapes(ly['M5']).insert(pya.Box(
        um(mix_ifp_x - route_w/2), um(mix_if_y - route_w/2),
        um(ifp_tm2_x + route_w/2), um(mix_if_y + route_w/2)))

    # IF_N: TM2 L-route from pad to above Mixer, then via to M5 at port
    ifn_tm2_x = mix_ifn_x + 20.0
    top.shapes(ly['TM2']).insert(pya.Box(
        um(ifn_tm2_x - route_w/2), um(mix_if_y + 50 - route_w/2),
        um(ifn_pad[0] + route_w/2), um(mix_if_y + 50 + route_w/2)))
    top.shapes(ly['TM2']).insert(pya.Box(
        um(ifn_pad[0] - route_w/2), um(mix_if_y + 50 - route_w/2),
        um(ifn_pad[0] + route_w/2), um(ifn_pad[1] + route_w/2)))
    top.shapes(ly['TM2']).insert(pya.Box(
        um(ifn_tm2_x - route_w/2), um(mix_if_y - route_w/2),
        um(ifn_tm2_x + route_w/2), um(mix_if_y + 50 + route_w/2)))
    via_stack_top(ifn_tm2_x, mix_if_y, 'M5', 'TM2')
    top.shapes(ly['M5']).insert(pya.Box(
        um(mix_ifn_x - route_w/2), um(mix_if_y - route_w/2),
        um(ifn_tm2_x + route_w/2), um(mix_if_y + route_w/2)))

    # ------------------------------------------------------------------
    # DIV_P/N pads (north_1, north_2) → ILFD output ports
    # ILFD outputs (cross-coupled collectors) not yet routed to external
    # ports. DIV pads get TM2→M5 via stacks only (future connection).
    # ------------------------------------------------------------------
    pad_to_m5(divp_pad[0], divp_pad[1])
    pad_to_m5(divn_pad[0], divn_pad[1])

    # ------------------------------------------------------------------
    # VTUNE pad (east_8) → VCO varactor control
    # Route on TM2 from pad south to y=1100 (below VCO), then west to x=1050
    # Via TM2→M5 at (1050,1100), then M5 north into VCO VTUNE port at (1050,1372)
    # ------------------------------------------------------------------
    # VCO VTUNE M5 port absolute position: vco_x+150=1050, vco_y+247.385≈1372.4
    vtune_m5_x = vco_x + 150.0   # 1050
    vtune_m5_y = vco_y + 247.385  # 1372.385
    vtune_via_y = 1100.0  # below VCO block (VCO starts at y=1125)

    # TM2 from pad south to y=1100
    top.shapes(ly['TM2']).insert(pya.Box(
        um(vtune_pad[0] - route_w/2), um(vtune_via_y - route_w/2),
        um(vtune_pad[0] + route_w/2), um(vtune_pad[1] + route_w/2)))
    # TM2 west from pad_x to vtune_m5_x at y=1100
    top.shapes(ly['TM2']).insert(pya.Box(
        um(vtune_m5_x - route_w/2), um(vtune_via_y - route_w/2),
        um(vtune_pad[0] + route_w/2), um(vtune_via_y + route_w/2)))
    # Via TM2→M5 at (1050, 1100)
    via_stack_top(vtune_m5_x, vtune_via_y, 'M5', 'TM2')
    # M5 vertical from (1050, 1100) north to VCO VTUNE port (1050, 1372)
    top.shapes(ly['M5']).insert(pya.Box(
        um(vtune_m5_x - route_w/2), um(vtune_via_y - route_w/2),
        um(vtune_m5_x + route_w/2), um(vtune_m5_y + route_w/2)))

    # ------------------------------------------------------------------
    # Bias/monitor pads — via stack to M5 landing (future connection)
    # ------------------------------------------------------------------
    bias_pad_keys = ['south_4_LO_TUNE',
                     'south_7_INJ_P', 'south_8_INJ_N',
                     'west_6_RF_MON_P', 'west_7_RF_MON_N']
    for pk in bias_pad_keys:
        if pk in pad_positions:
            pcx, pcy = pad_positions[pk]
            via_stack_top(pcx, pcy, 'M5', 'TM2')

    # === BIAS NETWORK ROUTING ===
    bias_bx, bias_by = 550.0, 500.0
    bias_route_w = 1.5

    # Bias network port positions (absolute)
    tail_in_pos = (bias_bx + 100, bias_by + 10)    # (650, 510)
    vcb_out_pos = (bias_bx + 30, bias_by + 290)    # (580, 790)
    mir_tx_pos = (bias_bx + 60, bias_by + 290)     # (610, 790)
    mir_lna_pos = (bias_bx + 90, bias_by + 290)    # (640, 790)
    mir_mix_pos = (bias_bx + 120, bias_by + 290)   # (670, 790)
    mir_vco_pos = (bias_bx + 150, bias_by + 290)   # (700, 790)
    mir_ilfd_pos = (bias_bx + 170, bias_by + 290)  # (720, 790)

    # Block tail node positions (M5 pads - corrected from block generator code)
    txpa_tail_x, txpa_tail_y = txpa_x + 175.0, txpa_y + 215.6  # (1075, 515.6)
    ilfd_tail_x, ilfd_tail_y = ilfd_x + 150.0, ilfd_y + 260.6  # (350, 560.6)
    lna_tail_x, lna_tail_y = lna_x + 150.0, lna_y + 50.0       # (350, 1150)
    mix_tail_x, mix_tail_y = mix_x + 150.0, mix_y + 50.0        # (700, 1175)
    vco_tail_x, vco_tail_y = vco_x + 125.0, vco_y + 50.0        # (1025, 1175)

    bw = bias_route_w

    # 1. TAIL_BIAS pad → BIAS TAIL_IN
    tail_pad_pos = pad_positions['south_2_TAIL_BIAS']
    via_stack_top(tail_pad_pos[0], tail_pad_pos[1], 'M4', 'TM2')
    via_stack_top(tail_in_pos[0], tail_in_pos[1], 'M4', 'M5')
    # M4 vertical from pad up to tail_in_y
    top.shapes(ly['M4']).insert(pya.Box(
        um(tail_pad_pos[0] - bw/2), um(tail_pad_pos[1]),
        um(tail_pad_pos[0] + bw/2), um(tail_in_pos[1])))
    # M4 horizontal from pad_x to tail_in_x at y=510
    top.shapes(ly['M4']).insert(pya.Box(
        um(min(tail_pad_pos[0], tail_in_pos[0]) - bw/2), um(tail_in_pos[1] - bw/2),
        um(max(tail_pad_pos[0], tail_in_pos[0]) + bw/2), um(tail_in_pos[1] + bw/2)))

    # 2. VCB_BIAS pad → BIAS VCB_OUT
    # Route at y=795 (offset from mirror pads at y=790) to avoid shorting
    vcb_pad_pos = pad_positions['south_3_VCB_BIAS']
    vcb_route_y = 795.0  # offset from y=790 mirror row
    via_stack_top(vcb_pad_pos[0], vcb_pad_pos[1], 'M4', 'TM2')
    via_stack_top(vcb_out_pos[0], vcb_out_pos[1], 'M4', 'M5')
    # M4 vertical from pad up to y=795
    top.shapes(ly['M4']).insert(pya.Box(
        um(vcb_pad_pos[0] - bw/2), um(vcb_pad_pos[1]),
        um(vcb_pad_pos[0] + bw/2), um(vcb_route_y + bw/2)))
    # M4 horizontal from pad_x to vcb_out_x at y=795
    top.shapes(ly['M4']).insert(pya.Box(
        um(min(vcb_pad_pos[0], vcb_out_pos[0]) - bw/2), um(vcb_route_y - bw/2),
        um(max(vcb_pad_pos[0], vcb_out_pos[0]) + bw/2), um(vcb_route_y + bw/2)))
    # Short M4 vertical from y=795 down to vcb_out at y=790
    top.shapes(ly['M4']).insert(pya.Box(
        um(vcb_out_pos[0] - bw/2), um(vcb_out_pos[1] - bw/2),
        um(vcb_out_pos[0] + bw/2), um(vcb_route_y + bw/2)))

    # 3. MIR_TX → TXPA tail (M3 route, avoiding all M3/M4 at y=790)
    # Strategy: from MIR_TX M4 pad (610,790), drop to y=785 on M4 (isolated),
    # then via to M3 at (610,785), then M3 down and right to TXPA tail.
    via_stack_top(mir_tx_pos[0], mir_tx_pos[1], 'M3', 'M4')
    txpa_entry_x = txpa_x + 156.6 - 5.0  # 1051.6
    mir_tx_drop_y = 785.0  # below all mirror pads at y=790
    # M4 short vertical from (610,790) down to (610,785)
    top.shapes(ly['M4']).insert(pya.Box(
        um(mir_tx_pos[0] - bw/2), um(mir_tx_drop_y - bw/2),
        um(mir_tx_pos[0] + bw/2), um(mir_tx_pos[1] + bw/2)))
    # Via M4→M3 at (610, 785)
    top.shapes(ly['M4']).insert(pya.Box(
        um(mir_tx_pos[0] - 0.25), um(mir_tx_drop_y - 0.25),
        um(mir_tx_pos[0] + 0.25), um(mir_tx_drop_y + 0.25)))
    top.shapes(ly['Via3']).insert(pya.Box(
        um(mir_tx_pos[0] - 0.095), um(mir_tx_drop_y - 0.095),
        um(mir_tx_pos[0] + 0.095), um(mir_tx_drop_y + 0.095)))
    top.shapes(ly['M3']).insert(pya.Box(
        um(mir_tx_pos[0] - 0.25), um(mir_tx_drop_y - 0.25),
        um(mir_tx_pos[0] + 0.25), um(mir_tx_drop_y + 0.25)))
    # M3 vertical from (610,785) down to txpa_tail_y=515.6
    top.shapes(ly['M3']).insert(pya.Box(
        um(mir_tx_pos[0] - bw/2), um(txpa_tail_y - bw/2),
        um(mir_tx_pos[0] + bw/2), um(mir_tx_drop_y + bw/2)))
    # M3 horizontal from (610,515.6) right to txpa_entry_x
    top.shapes(ly['M3']).insert(pya.Box(
        um(mir_tx_pos[0] - bw/2), um(txpa_tail_y - bw/2),
        um(txpa_entry_x + bw/2), um(txpa_tail_y + bw/2)))
    # Via M3→M4 at entry point
    via_stack_top(txpa_entry_x, txpa_tail_y, 'M3', 'M4')
    # Short M4 stub from entry to TAIL bus (just 5µm east)
    top.shapes(ly['M4']).insert(pya.Box(
        um(txpa_entry_x - bw/2), um(txpa_tail_y - bw/2),
        um(txpa_entry_x + 6.0), um(txpa_tail_y + bw/2)))

    # 4. MIR_ILFD → ILFD tail (avoid crossing MIR_TX M3 vertical at x=610)
    # ILFD TAIL M4 bus is at abs y=560.6, x=336.6-363.4
    # INJ_N M4 bus is at abs x=374.3, y=561.8-571.8 — must avoid!
    # Strategy: M3 vertical from (720,790) down to (720,560.6), via to M4,
    # then M4 horizontal at y=560.6 (TAIL level, BELOW INJ_N bus at y>561.5)
    via_stack_top(mir_ilfd_pos[0], mir_ilfd_pos[1], 'M3', 'M4')
    # M3 vertical from (720,790) down to (720,560.6)
    top.shapes(ly['M3']).insert(pya.Box(
        um(mir_ilfd_pos[0] - bw/2), um(ilfd_tail_y - bw/2),
        um(mir_ilfd_pos[0] + bw/2), um(mir_ilfd_pos[1] + bw/2)))
    # Via M3→M4 at (720, 560.6)
    via_stack_top(mir_ilfd_pos[0], ilfd_tail_y, 'M3', 'M4')
    # M4 horizontal from (720,560.6) left to ILFD TAIL bus right edge (363.4)
    top.shapes(ly['M4']).insert(pya.Box(
        um(ilfd_x + 163.4 - bw/2), um(ilfd_tail_y - bw/2),
        um(mir_ilfd_pos[0] + bw/2), um(ilfd_tail_y + bw/2)))

    # 5. MIR_LNA → LNA tail (M3, avoids M4 INJ_N crossing)
    via_stack_top(mir_lna_pos[0], mir_lna_pos[1], 'M3', 'M4')
    # M3 horizontal at y=790 from x=640 left to x=170
    top.shapes(ly['M3']).insert(pya.Box(
        um(170 - bw/2), um(mir_lna_pos[1] - bw/2),
        um(mir_lna_pos[0] + bw/2), um(mir_lna_pos[1] + bw/2)))
    # M3 vertical at x=170 from y=790 up to y=1150
    top.shapes(ly['M3']).insert(pya.Box(
        um(170 - bw/2), um(mir_lna_pos[1] - bw/2),
        um(170 + bw/2), um(lna_tail_y + bw/2)))
    # M3 horizontal at y=1150 from x=170 to x=350
    top.shapes(ly['M3']).insert(pya.Box(
        um(170 - bw/2), um(lna_tail_y - bw/2),
        um(lna_tail_x + bw/2), um(lna_tail_y + bw/2)))
    # Via stack at LNA tail from M3→M4 (to connect to block internal M2 via stack)
    via_stack_top(lna_tail_x, lna_tail_y, 'M3', 'M4')

    # 6. MIR_MIX → Mixer tail (M3)
    via_stack_top(mir_mix_pos[0], mir_mix_pos[1], 'M3', 'M4')
    # M3 vertical at x=670 from y=790 up to y=1175
    top.shapes(ly['M3']).insert(pya.Box(
        um(mir_mix_pos[0] - bw/2), um(mir_mix_pos[1] - bw/2),
        um(mir_mix_pos[0] + bw/2), um(mix_tail_y + bw/2)))
    # M3 horizontal at y=1175 from x=670 to x=700
    top.shapes(ly['M3']).insert(pya.Box(
        um(min(mir_mix_pos[0], mix_tail_x) - bw/2), um(mix_tail_y - bw/2),
        um(max(mir_mix_pos[0], mix_tail_x) + bw/2), um(mix_tail_y + bw/2)))
    # Via stack at Mixer tail from M3→M4
    via_stack_top(mix_tail_x, mix_tail_y, 'M3', 'M4')

    # 7. MIR_VCO → VCO tail (M3)
    via_stack_top(mir_vco_pos[0], mir_vco_pos[1], 'M3', 'M4')
    # M3 vertical at x=700 from y=790 up to y=1175
    top.shapes(ly['M3']).insert(pya.Box(
        um(mir_vco_pos[0] - bw/2), um(mir_vco_pos[1] - bw/2),
        um(mir_vco_pos[0] + bw/2), um(vco_tail_y + bw/2)))
    # M3 horizontal at y=1175 from x=700 to x=1025
    top.shapes(ly['M3']).insert(pya.Box(
        um(mir_vco_pos[0] - bw/2), um(vco_tail_y - bw/2),
        um(vco_tail_x + bw/2), um(vco_tail_y + bw/2)))
    # Via stack at VCO tail from M3→M4
    via_stack_top(vco_tail_x, vco_tail_y, 'M3', 'M4')

    print("Bias network routing complete")
    print("Power, ground, and pad connections added")

    # === ESD PROTECTION CELLS ===
    # Simple ESD cell: M1 diode landing (30×30µm) between pad and ground ring
    # In SG13G2, ESD is handled by npn13G2l in diode config (B=C=PAD, E=GND)
    # Place ESD cells adjacent to signal pads (inside pad ring)
    esd_cell = layout.create_cell("ESD_CELL")
    esd_sz = 30.0
    # M1 pad for diode anode (connects to signal via TM1 overlap)
    esd_cell.shapes(ly['M1']).insert(pya.Box(um(2), um(2), um(esd_sz-2), um(esd_sz-2)))
    # M2 ground connection
    esd_cell.shapes(ly['M2']).insert(pya.Box(um(2), um(2), um(esd_sz-2), um(10)))
    # Via1 array for M1→M2
    for vx in range(5, int(esd_sz-5), 3):
        for vy in range(3, 9, 3):
            esd_cell.shapes(ly['Via1']).insert(pya.Box(um(vx), um(vy), um(vx+0.19), um(vy+0.19)))
    # TM1 overlap (connects to ground plane)
    esd_cell.shapes(ly['TM1']).insert(pya.Box(um(0), um(0), um(esd_sz), um(12)))

    esd_idx = layout.cell_by_name("ESD_CELL")
    # Signal pads needing ESD
    esd_pad_names = ['ANT_RX_P', 'ANT_RX_N', 'ANT_TX_P', 'ANT_TX_N',
                     'IF_P', 'IF_N', 'DIV_P', 'DIV_N', 'VTUNE',
                     'TAIL_BIAS', 'VCB_BIAS', 'LO_TUNE',
                     'INJ_P', 'INJ_N', 'RF_MON_P', 'RF_MON_N']
    for pk, (pcx, pcy) in pad_positions.items():
        pad_name = pk.split('_', 2)[-1] if pk.count('_') >= 2 else ''
        if pad_name in esd_pad_names:
            # Place ESD cell inward from pad (toward die center)
            side = pk.split('_')[0]
            if side == 'south':
                ex, ey = pcx - esd_sz/2, pcy + PAD_SIZE/2 + 5
            elif side == 'north':
                ex, ey = pcx - esd_sz/2, pcy - PAD_SIZE/2 - esd_sz - 5
            elif side == 'west':
                ex, ey = pcx + PAD_SIZE/2 + 5, pcy - esd_sz/2
            elif side == 'east':
                ex, ey = pcx - PAD_SIZE/2 - esd_sz - 5, pcy - esd_sz/2
            else:
                continue
            top.insert(pya.CellInstArray(esd_idx, pya.Trans(um(ex), um(ey))))
    print("ESD protection cells placed on signal pads")

    # === METAL FILL FOR DENSITY RULES ===
    # Fill empty areas with small squares to meet minimum density requirements
    fill_specs = [
        ('M1', 2.0, 10.0, 3.0),
        ('M2', 2.0, 10.0, 3.0),
        ('M3', 3.0, 15.0, 3.0),
        ('M4', 3.0, 15.0, 5.0),
        ('M5', 3.0, 15.0, 5.0),
    ]
    for layer_name, fill_sz, fill_pitch, keepout in fill_specs:
        existing = pya.Region(top.begin_shapes_rec(ly[layer_name]))
        die_box = pya.Region(pya.Box(um(50), um(50), um(DIE_W-50), um(DIE_H-50)))
        keepout_reg = existing.sized(um(keepout))
        fill_area = die_box - keepout_reg
        fill_cell_name = f"FILL_{layer_name}"
        fc = layout.create_cell(fill_cell_name)
        fc.shapes(ly[layer_name]).insert(pya.Box(0, 0, um(fill_sz), um(fill_sz)))
        fc_idx = fc.cell_index()
        top.fill_region(fill_area, fc_idx,
                        pya.Box(0, 0, um(fill_pitch), um(fill_pitch)),
                        pya.Point(0, 0))
    print("Metal fill added for density rules")

    # --- DIE SEAL RING (M1 perimeter, single closed ring to avoid corner spacing) ---
    seal_w = 5.0
    # Use a single polygon (ring) to avoid M1.b spacing at corners
    outer = pya.Box(um(0), um(0), um(DIE_W), um(DIE_H))
    inner = pya.Box(um(seal_w), um(seal_w), um(DIE_W-seal_w), um(DIE_H-seal_w))
    ring = pya.Region(outer) - pya.Region(inner)
    top.shapes(ly['M1']).insert(ring)

    # --- OUTPUT ---
    output = OUT_DIR + "PHASED_ARRAY_77G_TOP.gds"
    layout.write(output)
    print(f"Top-level chip: {output}")
    print(f"Die size: {DIE_W} x {DIE_H} µm ({DIE_W/1000:.1f} x {DIE_H/1000:.1f} mm)")
    print(f"Blocks placed: VCO, LNA, MIXER, TXPA, ILFD")
    print(f"Pads: {sum(len(v) for v in pad_defs.values())} total")
    print(f"Inter-block routes: LO (VCO→Mixer), RF (LNA→Mixer), TX (VCO→TXPA), INJ (VCO→ILFD)")


if __name__ == "__main__":
    main()