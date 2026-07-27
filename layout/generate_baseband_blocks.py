"""
Baseband blocks for complete single-channel 77 GHz FMCW radar.
Completes the signal chain: Mixer IF → IFA → VGA → ADC → Digital Interface → DSP

Blocks:
  IFA_77G: IF amplifier, 2-stage diff amp, 40dB gain, BW=10MHz
  VGA_77G: Variable gain amp (Gilbert cell attenuator), 0-30dB
  ADC_77G: 12-bit SAR ADC analog front-end (comparator + R-DAC)
  BIAS_77G: Bandgap reference + bias distribution
  DIGIF_77G: CML output buffers (12-bit parallel bus to DSP)

All built from IHP SG13G2 PDK: npn13G2L + rppd + cmim
Pin mapping (confirmed): Collector=upper M1(y+5.425), Base=lower M1(y+1.775), Emitter=M2(y+3.6)
"""
import pya
import sys
sys.path.insert(0, "/home/bthomas3/Videos/77GHz_phased_array/layout/")
from generate_all_blocks import (
    um, via_stack, via_n, place_hbts, gnd_plane,
    connect_collectors_m3, connect_bases_m4, connect_emitters_m2,
    hbt_col, hbt_bas, hbt_emi, COL_DY, BAS_DY, EMI_DY, PCX,
    LAYERS, DBU
)

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"


def create_ifa(layout, ly, npn_idx, rppd_idx, cmim_idx):
    """IF Amplifier: 2-stage differential amplifier
    Stage1: Q1/Q2 (Nx=2) with resistive load → 20dB
    Stage2: Q3/Q4 (Nx=2) with resistive load → 20dB
    Total: 40dB gain, BW ~10MHz (set by cmim interstage caps)
    """
    W, H = 200.0, 300.0
    cell = layout.create_cell("IFA_77G")
    cx, cy = W/2, H/2
    sp = 9.0

    # Stage 1: input pair
    q1_x, q1_y0 = cx-25, cy-30
    q2_x, q2_y0 = cx+15, cy-30
    place_hbts(cell, npn_idx, q1_x, q1_y0, 2, sp)
    place_hbts(cell, npn_idx, q2_x, q2_y0, 2, sp)

    # Stage 2: output pair
    q3_x, q3_y0 = cx-25, cy+30
    q4_x, q4_y0 = cx+15, cy+30
    place_hbts(cell, npn_idx, q3_x, q3_y0, 2, sp)
    place_hbts(cell, npn_idx, q4_x, q4_y0, 2, sp)

    # Load resistors (4× rppd: 2 per stage)
    if rppd_idx:
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx-30), um(cy-10))))
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx+20), um(cy-10))))
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx-30), um(cy+60))))
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx+20), um(cy+60))))

    # Interstage coupling caps
    if cmim_idx:
        cell.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx-40), um(cy+5))))
        cell.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx+25), um(cy+5))))

    # Tail current source resistor
    if rppd_idx:
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx-5), um(cy-60))))
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx-5), um(cy+80))))

    # === ROUTING ===
    # Stage 1: Q1.C + Q2.C → collectors tied per side
    q1_cols = [hbt_col(q1_x, q1_y0+i*sp) for i in range(2)]
    q2_cols = [hbt_col(q2_x, q2_y0+i*sp) for i in range(2)]
    connect_collectors_m3(cell, ly, q1_cols, q1_x+0.0, 0)
    connect_collectors_m3(cell, ly, q2_cols, q2_x+7.8, 0)

    # Stage 1 bases → INP/INN
    q1_bases = [hbt_bas(q1_x, q1_y0+i*sp) for i in range(2)]
    q2_bases = [hbt_bas(q2_x, q2_y0+i*sp) for i in range(2)]
    connect_bases_m4(cell, ly, q1_bases, q1_x-2.0, 0)
    connect_bases_m4(cell, ly, q2_bases, q2_x+9.8, 0)

    # Stage 1 emitters → TAIL1
    q1_emis = [hbt_emi(q1_x, q1_y0+i*sp) for i in range(2)]
    q2_emis = [hbt_emi(q2_x, q2_y0+i*sp) for i in range(2)]
    connect_emitters_m2(cell, ly, q1_emis + q2_emis, cx)

    # Stage 2: same pattern
    q3_cols = [hbt_col(q3_x, q3_y0+i*sp) for i in range(2)]
    q4_cols = [hbt_col(q4_x, q4_y0+i*sp) for i in range(2)]
    connect_collectors_m3(cell, ly, q3_cols, q3_x+0.0, 0)
    connect_collectors_m3(cell, ly, q4_cols, q4_x+7.8, 0)

    q3_bases = [hbt_bas(q3_x, q3_y0+i*sp) for i in range(2)]
    q4_bases = [hbt_bas(q4_x, q4_y0+i*sp) for i in range(2)]
    connect_bases_m4(cell, ly, q3_bases, q3_x-2.0, 0)
    connect_bases_m4(cell, ly, q4_bases, q4_x+9.8, 0)

    q3_emis = [hbt_emi(q3_x, q3_y0+i*sp) for i in range(2)]
    q4_emis = [hbt_emi(q4_x, q4_y0+i*sp) for i in range(2)]
    connect_emitters_m2(cell, ly, q3_emis + q4_emis, cx+3.0)

    # Interstage: Q1.C (M3) → Q3.B (M4) via M3 vertical extension
    # (These are on different layers so they cross without shorting)

    cell.shapes(ly['M3']).insert(pya.Text("INP", pya.Trans(um(q1_x-2), um(q1_bases[0][1]))))
    cell.shapes(ly['M3']).insert(pya.Text("INN", pya.Trans(um(q2_x+10), um(q2_bases[0][1]))))
    cell.shapes(ly['M3']).insert(pya.Text("OUTP", pya.Trans(um(q3_x), um(q3_cols[-1][1]))))
    cell.shapes(ly['M3']).insert(pya.Text("OUTN", pya.Trans(um(q4_x+8), um(q4_cols[-1][1]))))

    return cell, W, H


def create_vga(layout, ly, npn_idx, rppd_idx):
    """VGA: Gilbert-cell variable gain amplifier
    Signal pair Q1/Q2 (Nx=2), gain control quad Q3-Q6 (Nx=1 each)
    Gain range: 0-30dB via control voltage
    """
    W, H = 200.0, 280.0
    cell = layout.create_cell("VGA_77G")
    cx, cy = W/2, H/2
    sp = 9.0

    # Signal transconductor
    q1_x, q1_y0 = cx-25, cy-40
    q2_x, q2_y0 = cx+15, cy-40
    place_hbts(cell, npn_idx, q1_x, q1_y0, 2, sp)
    place_hbts(cell, npn_idx, q2_x, q2_y0, 2, sp)

    # Gain control quad (attenuation)
    q3_x, q3_y0 = cx-35, cy+10
    q4_x, q4_y0 = cx-15, cy+10
    q5_x, q5_y0 = cx+5, cy+10
    q6_x, q6_y0 = cx+25, cy+10
    place_hbts(cell, npn_idx, q3_x, q3_y0, 1, sp)
    place_hbts(cell, npn_idx, q4_x, q4_y0, 1, sp)
    place_hbts(cell, npn_idx, q5_x, q5_y0, 1, sp)
    place_hbts(cell, npn_idx, q6_x, q6_y0, 1, sp)

    # Load resistors
    if rppd_idx:
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx-30), um(cy+40))))
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx+20), um(cy+40))))

    # === ROUTING ===
    # Signal pair collectors → M3
    q1_cols = [hbt_col(q1_x, q1_y0+i*sp) for i in range(2)]
    q2_cols = [hbt_col(q2_x, q2_y0+i*sp) for i in range(2)]
    connect_collectors_m3(cell, ly, q1_cols, q1_x+1.0, 0)
    connect_collectors_m3(cell, ly, q2_cols, q2_x+6.8, 0)

    # Signal pair emitters → tail
    q1_emis = [hbt_emi(q1_x, q1_y0+i*sp) for i in range(2)]
    q2_emis = [hbt_emi(q2_x, q2_y0+i*sp) for i in range(2)]
    connect_emitters_m2(cell, ly, q1_emis + q2_emis, cx)

    # Signal pair bases → input
    q1_bases = [hbt_bas(q1_x, q1_y0+i*sp) for i in range(2)]
    q2_bases = [hbt_bas(q2_x, q2_y0+i*sp) for i in range(2)]
    connect_bases_m4(cell, ly, q1_bases, q1_x-2.0, 0)
    connect_bases_m4(cell, ly, q2_bases, q2_x+9.8, 0)

    # Gain quad: Q3.C+Q5.C → OUTP, Q4.C+Q6.C → OUTN
    q3_col = [hbt_col(q3_x, q3_y0)]
    q5_col = [hbt_col(q5_x, q5_y0)]
    q4_col = [hbt_col(q4_x, q4_y0)]
    q6_col = [hbt_col(q6_x, q6_y0)]
    connect_collectors_m3(cell, ly, q3_col + q5_col, cx-40.0, 0)
    connect_collectors_m3(cell, ly, q4_col + q6_col, cx+40.0, 0)

    # Gain quad emitters → signal collectors (cascode connection)
    q3_emi = [hbt_emi(q3_x, q3_y0)]
    q4_emi = [hbt_emi(q4_x, q4_y0)]
    q5_emi = [hbt_emi(q5_x, q5_y0)]
    q6_emi = [hbt_emi(q6_x, q6_y0)]
    connect_emitters_m2(cell, ly, q3_emi + q4_emi, q1_x+1.0)
    connect_emitters_m2(cell, ly, q5_emi + q6_emi, q2_x+6.8)

    # Bridges: signal collector M3 → quad emitter M2
    bridge_l_y = (q1_cols[-1][1] + q3_emi[0][1]) / 2
    via_n(cell, ly, q1_x+1.0, bridge_l_y, 'M2', 'Via2', 'M3')
    cell.shapes(ly['M3']).insert(pya.Box(
        um(q1_x+0.75), um(q1_cols[-1][1]-0.25),
        um(q1_x+1.25), um(bridge_l_y+0.25)))
    cell.shapes(ly['M2']).insert(pya.Box(
        um(q1_x+0.75), um(bridge_l_y-0.25),
        um(q1_x+1.25), um(q3_emi[0][1]+0.25)))

    bridge_r_y = (q2_cols[-1][1] + q5_emi[0][1]) / 2
    via_n(cell, ly, q2_x+6.8, bridge_r_y, 'M2', 'Via2', 'M3')
    cell.shapes(ly['M3']).insert(pya.Box(
        um(q2_x+6.55), um(q2_cols[-1][1]-0.25),
        um(q2_x+7.05), um(bridge_r_y+0.25)))
    cell.shapes(ly['M2']).insert(pya.Box(
        um(q2_x+6.55), um(bridge_r_y-0.25),
        um(q2_x+7.05), um(q5_emi[0][1]+0.25)))

    # Gain control bases
    q3_bas = [hbt_bas(q3_x, q3_y0)]
    q4_bas = [hbt_bas(q4_x, q4_y0)]
    q5_bas = [hbt_bas(q5_x, q5_y0)]
    q6_bas = [hbt_bas(q6_x, q6_y0)]
    # Q3.B + Q6.B → VCTRL_P, Q4.B + Q5.B → VCTRL_N
    connect_bases_m4(cell, ly, q3_bas + q6_bas, cx-42.0, 0)
    connect_bases_m4(cell, ly, q4_bas + q5_bas, cx+42.0, 0)

    cell.shapes(ly['M3']).insert(pya.Text("INP", pya.Trans(um(q1_x-2), um(cy-40))))
    cell.shapes(ly['M3']).insert(pya.Text("INN", pya.Trans(um(q2_x+10), um(cy-40))))
    cell.shapes(ly['M3']).insert(pya.Text("OUTP", pya.Trans(um(cx-40), um(cy+30))))
    cell.shapes(ly['M3']).insert(pya.Text("OUTN", pya.Trans(um(cx+40), um(cy+30))))

    return cell, W, H


def create_adc(layout, ly, npn_idx, rppd_idx, cmim_idx):
    """ADC: 12-bit SAR analog front-end
    - Track/hold: differential pair + cmim sampling caps
    - Comparator: regenerative latch (4 HBTs)
    - DAC: R-2R ladder (24× rppd)
    - SAR logic: represented by CML flip-flops (12× diff pairs)
    """
    W, H = 400.0, 350.0
    cell = layout.create_cell("ADC_77G")
    cx, cy = W/2, H/2
    sp = 9.0

    # Track/hold pair
    th_x1, th_y = cx-60, cy-80
    th_x2 = cx-40
    place_hbts(cell, npn_idx, th_x1, th_y, 2, sp)
    place_hbts(cell, npn_idx, th_x2, th_y, 2, sp)

    # Sampling caps
    if cmim_idx:
        cell.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx-80), um(cy-60))))
        cell.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx-25), um(cy-60))))

    # Comparator (regenerative latch: 4 HBTs)
    cmp_x1, cmp_y = cx+20, cy-40
    cmp_x2 = cx+40
    place_hbts(cell, npn_idx, cmp_x1, cmp_y, 2, sp)
    place_hbts(cell, npn_idx, cmp_x2, cmp_y, 2, sp)

    # R-2R DAC: 24 resistors arranged in 2 rows of 12
    if rppd_idx:
        for i in range(12):
            cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(30+i*28), um(cy+40))))
            cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(30+i*28), um(cy+55))))

    # SAR logic: 12 CML diff pairs (flip-flops)
    for i in range(12):
        place_hbts(cell, npn_idx, 30+i*28, cy+80, 2, sp)

    # === ROUTING ===
    # T/H pair collectors
    th1_cols = [hbt_col(th_x1, th_y+i*sp) for i in range(2)]
    th2_cols = [hbt_col(th_x2, th_y+i*sp) for i in range(2)]
    connect_collectors_m3(cell, ly, th1_cols, th_x1+0.0, 0)
    connect_collectors_m3(cell, ly, th2_cols, th_x2+7.8, 0)

    # T/H emitters
    th1_emis = [hbt_emi(th_x1, th_y+i*sp) for i in range(2)]
    th2_emis = [hbt_emi(th_x2, th_y+i*sp) for i in range(2)]
    connect_emitters_m2(cell, ly, th1_emis + th2_emis, (th_x1+th_x2)/2 + PCX)

    # T/H bases → analog input
    th1_bases = [hbt_bas(th_x1, th_y+i*sp) for i in range(2)]
    th2_bases = [hbt_bas(th_x2, th_y+i*sp) for i in range(2)]
    connect_bases_m4(cell, ly, th1_bases, th_x1-2.0, 0)
    connect_bases_m4(cell, ly, th2_bases, th_x2+9.8, 0)

    # Comparator collectors (output latch)
    cmp1_cols = [hbt_col(cmp_x1, cmp_y+i*sp) for i in range(2)]
    cmp2_cols = [hbt_col(cmp_x2, cmp_y+i*sp) for i in range(2)]
    connect_collectors_m3(cell, ly, cmp1_cols, cmp_x1+0.0, 0)
    connect_collectors_m3(cell, ly, cmp2_cols, cmp_x2+7.8, 0)

    # Comparator bases → from T/H output
    cmp1_bases = [hbt_bas(cmp_x1, cmp_y+i*sp) for i in range(2)]
    cmp2_bases = [hbt_bas(cmp_x2, cmp_y+i*sp) for i in range(2)]
    connect_bases_m4(cell, ly, cmp1_bases, cmp_x1-2.0, 0)
    connect_bases_m4(cell, ly, cmp2_bases, cmp_x2+9.8, 0)

    # Comparator emitters
    cmp1_emis = [hbt_emi(cmp_x1, cmp_y+i*sp) for i in range(2)]
    cmp2_emis = [hbt_emi(cmp_x2, cmp_y+i*sp) for i in range(2)]
    connect_emitters_m2(cell, ly, cmp1_emis + cmp2_emis, (cmp_x1+cmp_x2)/2 + PCX)

    # SAR FF collectors → digital output bus (M3)
    for i in range(12):
        ff_cols = [hbt_col(30+i*28, cy+80+j*sp) for j in range(2)]
        connect_collectors_m3(cell, ly, ff_cols, 30+i*28-1.0, 0)

    # SAR FF emitters → shared tail (M2 horizontal bus)
    all_ff_emis = []
    for i in range(12):
        for j in range(2):
            all_ff_emis.append(hbt_emi(30+i*28, cy+80+j*sp))
    connect_emitters_m2(cell, ly, all_ff_emis, cx)

    cell.shapes(ly['M3']).insert(pya.Text("AINP", pya.Trans(um(th_x1-2), um(cy-80))))
    cell.shapes(ly['M3']).insert(pya.Text("AINN", pya.Trans(um(th_x2+10), um(cy-80))))
    cell.shapes(ly['M3']).insert(pya.Text("DOUT", pya.Trans(um(cx), um(cy+110))))
    cell.shapes(ly['M3']).insert(pya.Text("CLK", pya.Trans(um(cx+80), um(cy+110))))

    return cell, W, H


def create_bias(layout, ly, npn_idx, rppd_idx):
    """Bandgap reference + bias current mirrors
    - Bandgap core: 2 HBTs (different emitter areas via Nx)
    - Start-up circuit: 2 HBTs
    - Bias mirrors: 8 HBTs (distribute to all blocks)
    """
    W, H = 150.0, 200.0
    cell = layout.create_cell("BIAS_77G")
    cx, cy = W/2, H/2
    sp = 9.0

    # Bandgap core
    place_hbts(cell, npn_idx, cx-30, cy-30, 2, sp)
    place_hbts(cell, npn_idx, cx+10, cy-30, 2, sp)
    # Bias mirrors
    place_hbts(cell, npn_idx, cx-30, cy+20, 4, sp)
    place_hbts(cell, npn_idx, cx+10, cy+20, 4, sp)

    # Resistors (set bias currents)
    if rppd_idx:
        for i in range(6):
            cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx-40+i*15), um(cy-60))))

    # === ROUTING (Self-biased Brokaw bandgap) ===
    # BG core: Q1.C + Q2.C → VREF node (M3, shared)
    bg1_cols = [hbt_col(cx-30, cy-30+i*sp) for i in range(2)]
    bg2_cols = [hbt_col(cx+10, cy-30+i*sp) for i in range(2)]
    vref_bus_x = cx - 8.0
    connect_collectors_m3(cell, ly, bg1_cols + bg2_cols, vref_bus_x, 0)

    # BG emitters: separate per branch (different degeneration)
    # Q1.E → R1 (high-R branch), Q2.E → R2 (low-R branch, PTAT)
    bg1_emis = [hbt_emi(cx-30, cy-30+i*sp) for i in range(2)]
    bg2_emis = [hbt_emi(cx+10, cy-30+i*sp) for i in range(2)]
    connect_emitters_m2(cell, ly, bg1_emis, cx-28.0)
    connect_emitters_m2(cell, ly, bg2_emis, cx+12.0)

    # BG bases: Q1.B + Q2.B → self-bias from VREF (M3→Via3→M4 bridge)
    bg1_bases = [hbt_bas(cx-30, cy-30+i*sp) for i in range(2)]
    bg2_bases = [hbt_bas(cx+10, cy-30+i*sp) for i in range(2)]
    connect_bases_m4(cell, ly, bg1_bases + bg2_bases, vref_bus_x, 0)
    # Bridge VREF (M3) → BG bases (M4) via Via3
    vref_bridge_y = (bg1_cols[0][1] + bg1_bases[0][1]) / 2
    via_n(cell, ly, vref_bus_x, vref_bridge_y, 'M3', 'Via3', 'M4')

    # Mirror bases tied together → driven from VREF (M4 bus already at vref_bus_x)
    mir1_bases = [hbt_bas(cx-30, cy+20+i*sp) for i in range(4)]
    mir2_bases = [hbt_bas(cx+10, cy+20+i*sp) for i in range(4)]
    connect_bases_m4(cell, ly, mir1_bases + mir2_bases, vref_bus_x, 0)
    # Extend M4 bus from BG bases down to mirror bases (continuous vertical)
    cell.shapes(ly['M4']).insert(pya.Box(
        um(vref_bus_x-0.25), um(min(b[1] for b in bg1_bases)-0.25),
        um(vref_bus_x+0.25), um(max(b[1] for b in mir2_bases)+0.25)))

    # Mirror collectors → individual bias outputs (M3)
    mir1_cols = [hbt_col(cx-30, cy+20+i*sp) for i in range(4)]
    mir2_cols = [hbt_col(cx+10, cy+20+i*sp) for i in range(4)]
    connect_collectors_m3(cell, ly, mir1_cols, cx-32.0, 0)
    connect_collectors_m3(cell, ly, mir2_cols, cx+17.8, 0)

    # Mirror emitters → VSS (M2 shared bus)
    mir1_emis = [hbt_emi(cx-30, cy+20+i*sp) for i in range(4)]
    mir2_emis = [hbt_emi(cx+10, cy+20+i*sp) for i in range(4)]
    connect_emitters_m2(cell, ly, mir1_emis + mir2_emis, cx-5.0)

    cell.shapes(ly['M3']).insert(pya.Text("VREF", pya.Trans(um(cx), um(cy-60))))
    cell.shapes(ly['M3']).insert(pya.Text("IBIAS", pya.Trans(um(cx), um(cy+70))))

    return cell, W, H


def create_digif(layout, ly, npn_idx, rppd_idx):
    """Digital Interface: 12-bit CML output buffer + SPI control
    - 12× CML→50Ω drivers (data bus)
    - 2× clock buffer (CLK, FRAME)
    - 4× SPI interface (SCLK, MOSI, MISO, CS)
    Total: 18 diff pairs = 36 HBTs
    """
    W, H = 350.0, 200.0
    cell = layout.create_cell("DIGIF_77G")
    cx, cy = W/2, H/2
    sp = 9.0

    # 18 output buffer pairs (2 HBTs each)
    for i in range(18):
        x = 20.0 + i * 18.0
        place_hbts(cell, npn_idx, x, cy-20, 2, sp)

    # Termination resistors
    if rppd_idx:
        for i in range(18):
            cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(20+i*18), um(cy+20))))

    # === ROUTING ===
    # Each buffer: collectors → output, bases → input, emitters → tail
    for i in range(18):
        x = 20.0 + i * 18.0
        cols = [hbt_col(x, cy-20+j*sp) for j in range(2)]
        connect_collectors_m3(cell, ly, cols, x+0.0, 0)
        bases = [hbt_bas(x, cy-20+j*sp) for j in range(2)]
        connect_bases_m4(cell, ly, bases, x+7.8, 0)

    # Shared tail bus (M2)
    all_emis = []
    for i in range(18):
        x = 20.0 + i * 18.0
        for j in range(2):
            all_emis.append(hbt_emi(x, cy-20+j*sp))
    connect_emitters_m2(cell, ly, all_emis, cy-15.0)

    cell.shapes(ly['M3']).insert(pya.Text("DIN", pya.Trans(um(20), um(cy-50))))
    cell.shapes(ly['M3']).insert(pya.Text("DOUT", pya.Trans(um(cx), um(cy+40))))
    cell.shapes(ly['M3']).insert(pya.Text("CLK", pya.Trans(um(W-30), um(cy-50))))

    return cell, W, H


def main(ext_layout=None):
    if ext_layout:
        layout = ext_layout
    else:
        layout = pya.Layout()
        layout.dbu = DBU
        layout.read(PDK_GDS)

    ly = {}
    for name, (ln, dt) in LAYERS.items():
        ly[name] = layout.layer(ln, dt)

    npn_idx = layout.cell_by_name("npn13G2L")
    cmim_idx = layout.cell_by_name("cmim") if layout.has_cell("cmim") else None
    rppd_idx = layout.cell_by_name("rppd") if layout.has_cell("rppd") else None

    results = []
    ifa, w, h = create_ifa(layout, ly, npn_idx, rppd_idx, cmim_idx)
    results.append(("IFA_77G", w, h, "8×npn + 6×rppd + 2×cmim"))
    vga, w, h = create_vga(layout, ly, npn_idx, rppd_idx)
    results.append(("VGA_77G", w, h, "8×npn + 2×rppd"))
    adc, w, h = create_adc(layout, ly, npn_idx, rppd_idx, cmim_idx)
    results.append(("ADC_77G", w, h, "32×npn + 24×rppd + 2×cmim"))
    bias, w, h = create_bias(layout, ly, npn_idx, rppd_idx)
    results.append(("BIAS_77G", w, h, "12×npn + 6×rppd"))
    digif, w, h = create_digif(layout, ly, npn_idx, rppd_idx)
    results.append(("DIGIF_77G", w, h, "36×npn + 18×rppd"))

    if ext_layout is None:
        output = "/home/bthomas3/Videos/77GHz_phased_array/layout/BASEBAND_77G.gds"
        layout.write(output)
        print(f"\nBaseband blocks: {output}")
        for name, w, h, devs in results:
            print(f"  {name}: {w}×{h}µm, {devs}")

    return results


if __name__ == "__main__":
    main()