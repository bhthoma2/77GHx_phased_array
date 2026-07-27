"""
Full-chip transistor-level assembly: 77 GHz 4×4 Phased Array
Integrates VCO, LNA, Mixer, TX PA, ILFD blocks with bond pads.
IHP SG13G2, 2.5×2.5mm die.
"""
import pya

OUT_DIR = "/home/bthomas3/Videos/77GHz_phased_array/layout/"
DBU = 0.001
DIE_W = 2500.0
DIE_H = 2500.0
PAD_SZ = 70.0
PAD_PITCH = 150.0

LAYERS = {
    'M1': (8, 0), 'TM1': (126, 0), 'TM2': (134, 0),
    'TopVia2': (133, 0), 'M3': (30, 0),
}


def um(val):
    s = round(val / 0.005) * 0.005
    return int(s / DBU)


def main():
    layout = pya.Layout()
    layout.dbu = DBU

    PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"
    layout.read(PDK_GDS)

    import sys
    sys.path.insert(0, OUT_DIR)
    from generate_vco_transistor import main as gen_vco
    gen_vco(ext_layout=layout)

    from generate_all_blocks import create_lna, create_mixer, create_txpa, create_ilfd
    from generate_all_blocks import LAYERS as BLK_LAYERS, um as blk_um, gnd_plane
    from generate_baseband_blocks import create_ifa, create_vga, create_adc, create_bias, create_digif
    blk_ly = {}
    for name, (ln, dt) in BLK_LAYERS.items():
        blk_ly[name] = layout.layer(ln, dt)
    npn_idx = layout.cell_by_name("npn13G2L")
    cmim_idx = layout.cell_by_name("cmim") if layout.has_cell("cmim") else None
    rppd_idx = layout.cell_by_name("rppd") if layout.has_cell("rppd") else None
    create_lna(layout, blk_ly, npn_idx, cmim_idx, rppd_idx)
    create_mixer(layout, blk_ly, npn_idx, rppd_idx)
    create_txpa(layout, blk_ly, npn_idx, rppd_idx)
    create_ilfd(layout, blk_ly, npn_idx, rppd_idx)
    create_ifa(layout, blk_ly, npn_idx, rppd_idx, cmim_idx)
    create_vga(layout, blk_ly, npn_idx, rppd_idx)
    create_adc(layout, blk_ly, npn_idx, rppd_idx, cmim_idx)
    create_bias(layout, blk_ly, npn_idx, rppd_idx)
    create_digif(layout, blk_ly, npn_idx, rppd_idx)

    ly = {}
    for name, (ln, dt) in LAYERS.items():
        ly[name] = layout.layer(ln, dt)

    vco_idx = layout.cell_by_name("VCO_77G_XTOR")
    lna_idx = layout.cell_by_name("LNA_77G_XTOR")
    mix_idx = layout.cell_by_name("MIXER_77G_XTOR")
    txpa_idx = layout.cell_by_name("TXPA_77G_XTOR")
    ilfd_idx = layout.cell_by_name("ILFD_77G_XTOR")
    ifa_idx = layout.cell_by_name("IFA_77G")
    vga_idx = layout.cell_by_name("VGA_77G")
    adc_idx = layout.cell_by_name("ADC_77G")
    bias_idx = layout.cell_by_name("BIAS_77G")
    digif_idx = layout.cell_by_name("DIGIF_77G")

    top = layout.create_cell("PHASED_ARRAY_77G_XTOR")

    # === Die outline (M1 seal ring — no slotting rule on M1) ===
    fw = 5.0
    top.shapes(ly['M1']).insert(pya.Box(um(0), um(0), um(DIE_W), um(fw)))
    top.shapes(ly['M1']).insert(pya.Box(um(0), um(DIE_H-fw), um(DIE_W), um(DIE_H)))
    top.shapes(ly['M1']).insert(pya.Box(um(0), um(0), um(fw), um(DIE_H)))
    top.shapes(ly['M1']).insert(pya.Box(um(DIE_W-fw), um(0), um(DIE_W), um(DIE_H)))

    # === Place VCO + PLL area (center) ===
    if vco_idx is not None:
        top.insert(pya.CellInstArray(vco_idx, pya.Trans(um(1125), um(1025))))
        print("  VCO placed at center (1125, 1025)")

    # === Place ILFD (next to VCO) ===
    if ilfd_idx is not None:
        top.insert(pya.CellInstArray(ilfd_idx, pya.Trans(um(1125), um(370))))
        print("  ILFD placed at (1125, 370)")

    # === Place RX elements (LNA + Mixer per element) ===
    # 3 columns × 2 rows (6 RX elements, properly spaced to avoid TM2 merging)
    rx_x0, rx_y0 = 150.0, 200.0
    rx_pitch_x, rx_pitch_y = 370.0, 520.0
    rx_count = 0
    for row in range(2):
        for col in range(3):
            x = rx_x0 + col * rx_pitch_x
            y = rx_y0 + row * rx_pitch_y
            if lna_idx is not None:
                top.insert(pya.CellInstArray(lna_idx, pya.Trans(um(x), um(y))))
            if mix_idx is not None:
                top.insert(pya.CellInstArray(mix_idx, pya.Trans(um(x + 5), um(y + 260))))
            rx_count += 1

    print(f"  RX elements placed: {rx_count}× (LNA+Mixer)")

    # === Place 4 TX PA elements (right side, spaced 530µm apart) ===
    tx_x0 = 1900.0
    tx_y0 = 100.0
    tx_pitch_y = 530.0
    for i in range(4):
        y = tx_y0 + i * tx_pitch_y
        if txpa_idx is not None:
            top.insert(pya.CellInstArray(txpa_idx, pya.Trans(um(tx_x0), um(y))))
    print("  TX PA placed: 4× along right edge")

    # === Place baseband chain (between RX and VCO/TX area) ===
    # Signal flow: Mixer IF → IFA → VGA → ADC → DIGIF → DSP
    bb_x = 1050.0  # center column
    if ifa_idx is not None:
        top.insert(pya.CellInstArray(ifa_idx, pya.Trans(um(bb_x), um(1550))))
        print("  IFA placed at (1050, 1550)")
    if vga_idx is not None:
        top.insert(pya.CellInstArray(vga_idx, pya.Trans(um(bb_x), um(1870))))
        print("  VGA placed at (1050, 1870)")
    if adc_idx is not None:
        top.insert(pya.CellInstArray(adc_idx, pya.Trans(um(900), um(2100))))
        print("  ADC placed at (900, 2100)")
    if bias_idx is not None:
        top.insert(pya.CellInstArray(bias_idx, pya.Trans(um(1400), um(1550))))
        print("  BIAS placed at (1400, 1550)")
    if digif_idx is not None:
        top.insert(pya.CellInstArray(digif_idx, pya.Trans(um(800), um(2300))))
        print("  DIGIF placed at (800, 2300)")

    # === Bond pads (34 pads around perimeter) ===
    pad_positions = []
    # Bottom edge: 9 pads
    for i in range(9):
        pad_positions.append((250 + i * PAD_PITCH, 30))
    # Top edge: 9 pads
    for i in range(9):
        pad_positions.append((250 + i * PAD_PITCH, DIE_H - 30 - PAD_SZ))
    # Left edge: 8 pads
    for i in range(8):
        pad_positions.append((30, 300 + i * 240))
    # Right edge: 8 pads
    for i in range(8):
        pad_positions.append((DIE_W - 30 - PAD_SZ, 300 + i * 240))

    # Slotted pads: grid of sub-30µm rectangles (3µm slots, 20µm pitch both axes)
    slot_w = 3.0
    slot_pitch = 20.0
    seg = slot_pitch - slot_w  # 17µm segments (< 30µm)
    for px, py in pad_positions:
        y_cur = py
        while y_cur < py + PAD_SZ:
            sh = min(seg, py + PAD_SZ - y_cur)
            x_cur = px
            while x_cur < px + PAD_SZ:
                sw = min(seg, px + PAD_SZ - x_cur)
                if sh > 0 and sw > 0:
                    top.shapes(ly['TM2']).insert(pya.Box(um(x_cur), um(y_cur), um(x_cur+sw), um(y_cur+sh)))
                x_cur += slot_pitch
            y_cur += slot_pitch

    print(f"  Bond pads: {len(pad_positions)}")

    # === Chip-level TM1 ground plane (segmented, excludes block areas) ===
    # Collect block exclusion zones (x, y, w, h) with 5µm margin
    excl = []
    excl.append((1125, 1025, 250, 450))  # VCO
    excl.append((1125, 370, 350, 600))   # ILFD
    for row in range(2):
        for col in range(3):
            bx = 150.0 + col * 370.0
            by = 200.0 + row * 520.0
            excl.append((bx, by, 300, 500))       # LNA
            excl.append((bx+5, by+260, 300, 450)) # Mixer
    for i in range(4):
        excl.append((1900, 100+i*530, 350, 550))  # TX PA

    slot_w = 3.0
    pitch = 25.0
    seg = pitch - slot_w
    gnd_margin = 130.0
    blk_margin = 15.0
    y_gp = gnd_margin
    while y_gp < DIE_H - gnd_margin:
        sh = min(seg, DIE_H - gnd_margin - y_gp)
        x_gp = gnd_margin
        while x_gp < DIE_W - gnd_margin:
            sw = min(seg, DIE_W - gnd_margin - x_gp)
            if sh > 0 and sw > 0:
                skip = False
                for ex, ey, ew, eh in excl:
                    if (x_gp < ex + ew + blk_margin and x_gp + sw > ex - blk_margin and
                        y_gp < ey + eh + blk_margin and y_gp + sh > ey - blk_margin):
                        skip = True
                        break
                if not skip:
                    top.shapes(ly['TM1']).insert(pya.Box(um(x_gp), um(y_gp), um(x_gp+sw), um(y_gp+sh)))
            x_gp += pitch
        y_gp += pitch

    # === Power rings (M3) ===
    ring_w = 20.0
    top.shapes(ly['M3']).insert(pya.Box(um(120), um(120), um(DIE_W-120), um(120+ring_w)))
    top.shapes(ly['M3']).insert(pya.Box(um(120), um(DIE_H-120-ring_w), um(DIE_W-120), um(DIE_H-120)))
    top.shapes(ly['M3']).insert(pya.Box(um(120), um(120), um(120+ring_w), um(DIE_H-120)))
    top.shapes(ly['M3']).insert(pya.Box(um(DIE_W-120-ring_w), um(120), um(DIE_W-120), um(DIE_H-120)))

    # === INTER-BLOCK SIGNAL ROUTING ===
    ly_m5 = layout.layer(67, 0)
    ly_topvia1 = layout.layer(125, 0)
    ly_tm1_sig = layout.layer(126, 0)
    ly_topvia2 = layout.layer(133, 0)
    ly_tm2 = layout.layer(134, 0)

    # DRC-correct via stack helper (TV1=0.42µm, TV2=0.90µm)
    def top_via_stack(cell, x, y):
        x, y = round(x/0.005)*0.005, round(y/0.005)*0.005
        # M5 pad (5µm)
        cell.shapes(ly_m5).insert(pya.Box(um(x-2.5), um(y-2.5), um(x+2.5), um(y+2.5)))
        # TopVia1 (0.42µm)
        cell.shapes(ly_topvia1).insert(pya.Box(um(x-0.21), um(y-0.21), um(x+0.21), um(y+0.21)))
        # TM1 pad (need 0.42µm enclosure of TV1 → min 1.26µm, use 2µm)
        cell.shapes(ly_tm1_sig).insert(pya.Box(um(x-1.0), um(y-1.0), um(x+1.0), um(y+1.0)))
        # TopVia2 (0.90µm)
        cell.shapes(ly_topvia2).insert(pya.Box(um(x-0.45), um(y-0.45), um(x+0.45), um(y+0.45)))
        # TM2 pad (need 0.50µm enclosure of TV2 → min 1.90µm, use 3µm)
        cell.shapes(ly_tm2).insert(pya.Box(um(x-1.5), um(y-1.5), um(x+1.5), um(y+1.5)))

    # Slotted TM2 trace helper (max 30µm continuous → 25µm segments, 3µm gaps)
    def tm2_trace_v(cell, x, y1, y2, w=5.0):
        seg, gap = 25.0, 3.0
        y = min(y1, y2)
        ye = max(y1, y2)
        while y < ye:
            sh = min(seg, ye - y)
            cell.shapes(ly_tm2).insert(pya.Box(um(x-w/2), um(y), um(x+w/2), um(y+sh)))
            y += seg + gap

    def tm2_trace_h(cell, x1, x2, y, w=5.0):
        seg, gap = 25.0, 3.0
        x = min(x1, x2)
        xe = max(x1, x2)
        while x < xe:
            sw = min(seg, xe - x)
            cell.shapes(ly_tm2).insert(pya.Box(um(x), um(y-w/2), um(x+sw), um(y+w/2)))
            x += seg + gap

    # --- Route C: LNA→Mixer RF (per-element, M5 short verticals) ---
    for row in range(2):
        for col in range(3):
            lna_x = 150.0 + col * 370.0
            lna_y = 200.0 + row * 520.0
            # LNA OUTP/OUTN at local (121.2, 300.4)/(178.8, 300.4)
            lna_outp_x = lna_x + 121.2
            lna_outn_x = lna_x + 178.8
            lna_out_y = lna_y + 300.4
            # Mixer RF_P/RF_N at local (123.1, 200)/(173.0, 200) with mixer at (lna_x+5, lna_y+260)
            mix_rfp_x = lna_x + 5.0 + 123.1
            mix_rfn_x = lna_x + 5.0 + 173.0
            mix_rf_y = lna_y + 260.0 + 200.0
            # M5 L-route OUTP→RF_P
            top.shapes(ly_m5).insert(pya.Box(
                um(lna_outp_x-0.5), um(lna_out_y-0.5),
                um(mix_rfp_x+0.5), um(lna_out_y+0.5)))
            top.shapes(ly_m5).insert(pya.Box(
                um(mix_rfp_x-0.5), um(lna_out_y-0.5),
                um(mix_rfp_x+0.5), um(mix_rf_y+0.5)))
            # M5 L-route OUTN→RF_N
            top.shapes(ly_m5).insert(pya.Box(
                um(mix_rfn_x-0.5), um(lna_out_y-0.5),
                um(lna_outn_x+0.5), um(lna_out_y+0.5)))
            top.shapes(ly_m5).insert(pya.Box(
                um(mix_rfn_x-0.5), um(lna_out_y-0.5),
                um(mix_rfn_x+0.5), um(mix_rf_y+0.5)))
    print("  LNA→Mixer RF routes: 6× differential pairs on M5")

    # --- Route A: VCO→ILFD LO injection (TM2 differential CPW) ---
    # VCO ports: OUTP at local (144, 219), OUTN at (139, 219)
    vco_outp_x = 1125.0 + 144.0  # 1269
    vco_outn_x = 1125.0 + 139.0  # 1264
    vco_lo_y = 1025.0 + 219.0    # 1244
    # ILFD ports: INJ_P at local (125.7, 266), INJ_N at (174.3, 266)
    ilfd_injp_x = 1125.0 + 125.7  # 1250.7
    ilfd_injn_x = 1125.0 + 174.3  # 1299.3
    ilfd_inj_y = 370.0 + 266.0    # 636

    # Via stacks at VCO and ILFD ends (DRC-correct sizes)
    for px, py in [(vco_outp_x, vco_lo_y), (vco_outn_x, vco_lo_y),
                   (ilfd_injp_x, ilfd_inj_y), (ilfd_injn_x, ilfd_inj_y)]:
        top_via_stack(top, px, py)
    # TM2 differential traces (slotted) VCO→ILFD
    lo_p_x = (vco_outp_x + ilfd_injp_x) / 2
    lo_n_x = (vco_outn_x + ilfd_injn_x) / 2
    tm2_trace_v(top, lo_p_x, ilfd_inj_y, vco_lo_y)
    tm2_trace_v(top, lo_n_x, ilfd_inj_y, vco_lo_y)
    # TM2 ground shields (slotted)
    tm2_trace_v(top, lo_p_x - 12.5, ilfd_inj_y, vco_lo_y, w=10.0)
    tm2_trace_v(top, lo_n_x + 12.5, ilfd_inj_y, vco_lo_y, w=10.0)
    # Short TM2 jogs (< 30µm, no slotting needed)
    top.shapes(ly_tm2).insert(pya.Box(um(vco_outp_x-1.5), um(vco_lo_y-2.5), um(lo_p_x+2.5), um(vco_lo_y+2.5)))
    top.shapes(ly_tm2).insert(pya.Box(um(vco_outn_x-1.5), um(vco_lo_y-2.5), um(lo_n_x+2.5), um(vco_lo_y+2.5)))
    top.shapes(ly_tm2).insert(pya.Box(um(ilfd_injp_x-1.5), um(ilfd_inj_y-2.5), um(lo_p_x+2.5), um(ilfd_inj_y+2.5)))
    top.shapes(ly_tm2).insert(pya.Box(um(ilfd_injn_x-1.5), um(ilfd_inj_y-2.5), um(lo_n_x+2.5), um(ilfd_inj_y+2.5)))
    print("  VCO→ILFD LO route: TM2 shielded differential CPW")

    # --- Route B: VCO→Mixer LO distribution (TM2 H-tree, slotted) ---
    spine_y = 720.0
    tm2_trace_v(top, lo_p_x, spine_y, ilfd_inj_y)
    tm2_trace_v(top, lo_n_x, spine_y, ilfd_inj_y)
    # Horizontal spine at y=720
    spine_xl = 280.0
    tm2_trace_h(top, spine_xl, lo_p_x, spine_y)
    tm2_trace_h(top, spine_xl, lo_n_x, spine_y + 15.0)
    # Column drops to each mixer LO port
    for col in range(3):
        mx = 155.0 + col * 370.0 + 150.0
        for row in range(2):
            mix_lo_y = 460.0 + row * 520.0 + 263.775
            tm2_trace_v(top, mx - 7.5, mix_lo_y, spine_y)
            tm2_trace_v(top, mx + 7.5, mix_lo_y, spine_y + 15.0)
            # DRC-correct via stacks at mixer end
            top_via_stack(top, mx - 7.5, mix_lo_y)
            top_via_stack(top, mx + 7.5, mix_lo_y)
        # Horizontal tap from spine to column
        tap_x = mx - 7.5
        tm2_trace_h(top, tap_x, spine_xl if tap_x < lo_p_x else lo_p_x, spine_y)
    print("  VCO→Mixer LO distribution: TM2 H-tree (6 endpoints)")

    # Save
    output = f"{OUT_DIR}PHASED_ARRAY_77G_XTOR.gds"
    layout.write(output)
    print(f"\nFull chip: {output}")
    print(f"Die: {DIE_W}×{DIE_H}µm (2.5×2.5mm)")
    print("Blocks: VCO + ILFD + 12×(LNA+Mixer) + 4×TXPA + 34 pads")


if __name__ == "__main__":
    main()
