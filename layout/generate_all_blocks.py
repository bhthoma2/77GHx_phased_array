"""
Generate transistor-level layouts for all 77 GHz phased array blocks.
Uses IHP SG13G2 PDK cells. DRC-clean pattern from VCO.
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
TL_W = 5.0
TL_GAP = 5.0
TL_GND = 15.0


def um(val):
    s = round(val / 0.005) * 0.005
    return int(s / DBU)


def gnd_plane(cell, ly, w, h, clearances=None):
    """No-op: ground plane moved to chip level to avoid PDK cell interactions"""
    pass


def cpw(cell, ly, x0, y0, length, d='up'):
    """CPW with segmented ground strips (≤25µm segments to meet Slt.c.TM2)"""
    w = um(TL_W)
    g = um(TL_GAP)
    gw = um(TL_GND)
    l = um(length)
    seg_max = 25.0
    slot_gap = 3.0
    # Signal trace (5µm wide, always fine for Slt.c since width<30)
    if d == 'up':
        cell.shapes(ly['TM2']).insert(pya.Box(um(x0)-w//2, um(y0), um(x0)+w//2, um(y0)+l))
        # Segmented ground strips
        pos = 0.0
        while pos < length:
            seg_l = min(seg_max, length - pos)
            y_s = um(y0 + pos)
            y_e = um(y0 + pos + seg_l)
            cell.shapes(ly['TM2']).insert(pya.Box(um(x0)-w//2-g-gw, y_s, um(x0)-w//2-g, y_e))
            cell.shapes(ly['TM2']).insert(pya.Box(um(x0)+w//2+g, y_s, um(x0)+w//2+g+gw, y_e))
            pos += seg_max + slot_gap
    elif d == 'down':
        cell.shapes(ly['TM2']).insert(pya.Box(um(x0)-w//2, um(y0)-l, um(x0)+w//2, um(y0)))
        pos = 0.0
        while pos < length:
            seg_l = min(seg_max, length - pos)
            y_s = um(y0 - pos - seg_l)
            y_e = um(y0 - pos)
            cell.shapes(ly['TM2']).insert(pya.Box(um(x0)-w//2-g-gw, y_s, um(x0)-w//2-g, y_e))
            cell.shapes(ly['TM2']).insert(pya.Box(um(x0)+w//2+g, y_s, um(x0)+w//2+g+gw, y_e))
            pos += seg_max + slot_gap
    elif d == 'right':
        cell.shapes(ly['TM2']).insert(pya.Box(um(x0), um(y0)-w//2, um(x0)+l, um(y0)+w//2))
        pos = 0.0
        while pos < length:
            seg_l = min(seg_max, length - pos)
            x_s = um(x0 + pos)
            x_e = um(x0 + pos + seg_l)
            cell.shapes(ly['TM2']).insert(pya.Box(x_s, um(y0)+w//2+g, x_e, um(y0)+w//2+g+gw))
            cell.shapes(ly['TM2']).insert(pya.Box(x_s, um(y0)-w//2-g-gw, x_e, um(y0)-w//2-g))
            pos += seg_max + slot_gap


def via_stack(cell, ly, x, y):
    x = round(x/0.005)*0.005
    y = round(y/0.005)*0.005
    specs = [('M1','Via1','M2',0.19,0.5),('M2','Via2','M3',0.19,0.5),
             ('M3','Via3','M4',0.19,0.5),('M4','Via4','M5',0.19,0.5),
             ('M5','TopVia1','TM1',0.42,5.0),('TM1','TopVia2','TM2',0.9,5.0)]
    for bot,via,top,vs,ps in specs:
        cx,cy = um(x),um(y)
        v,p = um(round(vs/0.005)*0.005), um(round(ps/0.005)*0.005)
        cell.shapes(ly[bot]).insert(pya.Box(cx-p//2,cy-p//2,cx+p//2,cy+p//2))
        cell.shapes(ly[via]).insert(pya.Box(cx-v//2,cy-v//2,cx+v//2,cy+v//2))
        cell.shapes(ly[top]).insert(pya.Box(cx-p//2,cy-p//2,cx+p//2,cy+p//2))


def via_n(cell, ly, x, y, bot, via, top):
    x = round(x/0.005)*0.005
    y = round(y/0.005)*0.005
    ps = um(0.5)
    vs = um(0.19)
    cx, cy = um(x), um(y)
    cell.shapes(ly[bot]).insert(pya.Box(cx-ps//2, cy-ps//2, cx+ps//2, cy+ps//2))
    cell.shapes(ly[via]).insert(pya.Box(cx-vs//2, cy-vs//2, cx+vs//2, cy+vs//2))
    cell.shapes(ly[top]).insert(pya.Box(cx-ps//2, cy-ps//2, cx+ps//2, cy+ps//2))


COL_DY = 5.425
BAS_DY = 1.775
EMI_DY = 3.6
PCX = 3.9


def hbt_col(x, y):
    return (x + PCX, y + COL_DY)

def hbt_bas(x, y):
    return (x + PCX, y + BAS_DY)

def hbt_emi(x, y):
    return (x + PCX, y + EMI_DY)


def place_hbts(cell, npn_idx, x, y, nx, spacing=10.0):
    for i in range(nx):
        cell.insert(pya.CellInstArray(npn_idx, pya.Trans(um(x), um(y + i*spacing))))


def connect_collectors_m3(cell, ly, positions, bus_x, bus_y):
    for px, py in positions:
        via_n(cell, ly, px, py, 'M1', 'Via1', 'M2')
        via_n(cell, ly, px, py, 'M2', 'Via2', 'M3')
        cell.shapes(ly['M3']).insert(pya.Box(
            um(min(px, bus_x)-0.25), um(py-0.25),
            um(max(px, bus_x)+0.25), um(py+0.25)))
    ys = [p[1] for p in positions]
    cell.shapes(ly['M3']).insert(pya.Box(
        um(bus_x-0.25), um(min(ys)-0.25),
        um(bus_x+0.25), um(max(ys)+0.25)))


def connect_bases_m4(cell, ly, positions, bus_x, bus_y):
    for px, py in positions:
        via_n(cell, ly, px, py, 'M1', 'Via1', 'M2')
        via_n(cell, ly, px, py, 'M2', 'Via2', 'M3')
        via_n(cell, ly, px, py, 'M3', 'Via3', 'M4')
        cell.shapes(ly['M4']).insert(pya.Box(
            um(min(px, bus_x)-0.25), um(py-0.25),
            um(max(px, bus_x)+0.25), um(py+0.25)))
    ys = [p[1] for p in positions]
    cell.shapes(ly['M4']).insert(pya.Box(
        um(bus_x-0.25), um(min(ys)-0.25),
        um(bus_x+0.25), um(max(ys)+0.25)))


def connect_emitters_m2(cell, ly, positions, bus_x):
    for px, py in positions:
        cell.shapes(ly['M2']).insert(pya.Box(
            um(min(px, bus_x)-0.25), um(py-0.25),
            um(max(px, bus_x)+0.25), um(py+0.25)))
    ys = [p[1] for p in positions]
    cell.shapes(ly['M2']).insert(pya.Box(
        um(bus_x-0.25), um(min(ys)-0.25),
        um(bus_x+0.25), um(max(ys)+0.25)))


def create_lna(layout, ly, npn_idx, cmim_idx, rppd_idx):
    """LNA: Differential cascode, 4× Nx=4 HBTs
    Q1(left input) → Q3(left cascode) → OUTP
    Q2(right input) → Q4(right cascode) → OUTN
    """
    W, H = 300.0, 500.0
    cell = layout.create_cell("LNA_77G_XTOR")
    cx, cy = W/2, H/2
    gnd_plane(cell, ly, W, H)

    # Device placement
    q1_x, q1_y0, sp = cx-35, cy-20, 9.0
    q2_x, q2_y0 = cx+25, cy-20
    q3_x, q3_y0 = cx-35, cy+25
    q4_x, q4_y0 = cx+25, cy+25
    place_hbts(cell, npn_idx, q1_x, q1_y0, 4, sp)
    place_hbts(cell, npn_idx, q2_x, q2_y0, 4, sp)
    place_hbts(cell, npn_idx, q3_x, q3_y0, 4, sp)
    place_hbts(cell, npn_idx, q4_x, q4_y0, 4, sp)

    # === ROUTING ===
    # Q1 collectors → M3 bus (left, x=112)
    q1_cols = [hbt_col(q1_x, q1_y0+i*sp) for i in range(4)]
    connect_collectors_m3(cell, ly, q1_cols, q1_x+1.0, 0)
    # Q2 collectors → M3 bus (right, x=182)
    q2_cols = [hbt_col(q2_x, q2_y0+i*sp) for i in range(4)]
    connect_collectors_m3(cell, ly, q2_cols, q2_x+6.8, 0)

    # Q3 emitters → M2 bus (left)
    q3_emis = [hbt_emi(q3_x, q3_y0+i*sp) for i in range(4)]
    connect_emitters_m2(cell, ly, q3_emis, q3_x+1.0)
    # Q4 emitters → M2 bus (right)
    q4_emis = [hbt_emi(q4_x, q4_y0+i*sp) for i in range(4)]
    connect_emitters_m2(cell, ly, q4_emis, q4_x+6.8)

    # Cascode connection: Q1.C bus (M3) → via down to M2 → Q3.E bus (M2)
    # Left cascode node
    casc_l_x = q1_x + 1.0
    casc_l_y = (q1_cols[-1][1] + q3_emis[0][1]) / 2
    via_n(cell, ly, casc_l_x, casc_l_y, 'M2', 'Via2', 'M3')
    cell.shapes(ly['M3']).insert(pya.Box(
        um(casc_l_x-0.25), um(q1_cols[-1][1]-0.25),
        um(casc_l_x+0.25), um(casc_l_y+0.25)))
    cell.shapes(ly['M2']).insert(pya.Box(
        um(casc_l_x-0.25), um(casc_l_y-0.25),
        um(casc_l_x+0.25), um(q3_emis[0][1]+0.25)))
    # Right cascode node
    casc_r_x = q2_x + 6.8
    casc_r_y = (q2_cols[-1][1] + q4_emis[0][1]) / 2
    via_n(cell, ly, casc_r_x, casc_r_y, 'M2', 'Via2', 'M3')
    cell.shapes(ly['M3']).insert(pya.Box(
        um(casc_r_x-0.25), um(q2_cols[-1][1]-0.25),
        um(casc_r_x+0.25), um(casc_r_y+0.25)))
    cell.shapes(ly['M2']).insert(pya.Box(
        um(casc_r_x-0.25), um(casc_r_y-0.25),
        um(casc_r_x+0.25), um(q4_emis[0][1]+0.25)))

    # Q3 collectors → OUTP (M3 bus at x=113)
    q3_cols = [hbt_col(q3_x, q3_y0+i*sp) for i in range(4)]
    outp_x = q3_x + 0.0
    connect_collectors_m3(cell, ly, q3_cols, outp_x, 0)
    # Q4 collectors → OUTN (M3 bus at x=183)
    q4_cols = [hbt_col(q4_x, q4_y0+i*sp) for i in range(4)]
    outn_x = q4_x + 7.8
    connect_collectors_m3(cell, ly, q4_cols, outn_x, 0)

    # Q1 bases → INP (M4 bus at x=113)
    q1_bases = [hbt_bas(q1_x, q1_y0+i*sp) for i in range(4)]
    connect_bases_m4(cell, ly, q1_bases, q1_x+0.0, 0)
    # Q2 bases → INN (M4 bus at x=183)
    q2_bases = [hbt_bas(q2_x, q2_y0+i*sp) for i in range(4)]
    connect_bases_m4(cell, ly, q2_bases, q2_x+7.8, 0)

    # Q3+Q4 bases → VCASC (M4 bus, shared)
    q3_bases = [hbt_bas(q3_x, q3_y0+i*sp) for i in range(4)]
    q4_bases = [hbt_bas(q4_x, q4_y0+i*sp) for i in range(4)]
    vcasc_y = (q3_bases[0][1] + q3_bases[-1][1]) / 2
    connect_bases_m4(cell, ly, q3_bases, q3_x-2.0, 0)
    connect_bases_m4(cell, ly, q4_bases, q4_x+9.8, 0)
    # Horizontal M4 connecting both cascode bias buses
    cell.shapes(ly['M4']).insert(pya.Box(
        um(q3_x-2.25), um(vcasc_y-0.25),
        um(q4_x+10.05), um(vcasc_y+0.25)))

    # Q1 emitters → TAIL_L (M2 bus)
    q1_emis = [hbt_emi(q1_x, q1_y0+i*sp) for i in range(4)]
    connect_emitters_m2(cell, ly, q1_emis, q1_x+6.8)
    # Q2 emitters → TAIL_R (M2 bus)
    q2_emis = [hbt_emi(q2_x, q2_y0+i*sp) for i in range(4)]
    connect_emitters_m2(cell, ly, q2_emis, q2_x+1.0)

    # CPW and via stacks
    cpw(cell, ly, cx-45, cy+80, 97.0, 'up')
    cpw(cell, ly, cx+45, cy+80, 97.0, 'up')
    cpw(cell, ly, cx-35, cy+80, 210.0, 'up')
    cpw(cell, ly, cx+35, cy+80, 210.0, 'up')
    cpw(cell, ly, cx-35, cy-50, 58.0, 'down')
    cpw(cell, ly, cx+35, cy-50, 58.0, 'down')
    via_stack(cell, ly, cx-35, cy+80)
    via_stack(cell, ly, cx+35, cy+80)

    if cmim_idx: cell.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx-60), um(cy+90))))
    if cmim_idx: cell.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(cx+50), um(cy+90))))
    if rppd_idx: cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx), um(cy+70))))

    cell.shapes(ly['M3']).insert(pya.Box(um(10), um(H-30), um(W-10), um(H-24)))
    cell.shapes(ly['TM2']).insert(pya.Text("INP", pya.Trans(um(cx-45), um(cy+180))))
    cell.shapes(ly['TM2']).insert(pya.Text("INN", pya.Trans(um(cx+45), um(cy+180))))
    cell.shapes(ly['TM2']).insert(pya.Text("OUTP", pya.Trans(um(cx-35), um(cy+295))))
    cell.shapes(ly['TM2']).insert(pya.Text("OUTN", pya.Trans(um(cx+35), um(cy+295))))

    return cell, W, H


def create_mixer(layout, ly, npn_idx, rppd_idx):
    """Mixer: Gilbert cell
    Q5(RF left).C → Q1.E + Q2.E (LO left pair)
    Q6(RF right).C → Q3.E + Q4.E (LO right pair)
    Q1.C + Q3.C → IF_P, Q2.C + Q4.C → IF_N
    Q1.B + Q4.B → LO_P, Q2.B + Q3.B → LO_N
    """
    W, H = 300.0, 450.0
    cell = layout.create_cell("MIXER_77G_XTOR")
    cx, cy = W/2, H/2
    gnd_plane(cell, ly, W, H)

    # Device placement
    q5_x, q5_y0, sp = cx-30, cy-40, 9.0
    q6_x, q6_y0 = cx+20, cy-40
    q1_x, q1_y0 = cx-40, cy+20
    q2_x, q2_y0 = cx-15, cy+20
    q3_x, q3_y0 = cx+10, cy+20
    q4_x, q4_y0 = cx+35, cy+20
    place_hbts(cell, npn_idx, q5_x, q5_y0, 4, sp)
    place_hbts(cell, npn_idx, q6_x, q6_y0, 4, sp)
    place_hbts(cell, npn_idx, q1_x, q1_y0, 2, sp)
    place_hbts(cell, npn_idx, q2_x, q2_y0, 2, sp)
    place_hbts(cell, npn_idx, q3_x, q3_y0, 2, sp)
    place_hbts(cell, npn_idx, q4_x, q4_y0, 2, sp)

    # === ROUTING ===
    # Q5 collectors → M3 bus (left RF node)
    q5_cols = [hbt_col(q5_x, q5_y0+i*sp) for i in range(4)]
    connect_collectors_m3(cell, ly, q5_cols, q5_x+1.0, 0)
    # Q6 collectors → M3 bus (right RF node)
    q6_cols = [hbt_col(q6_x, q6_y0+i*sp) for i in range(4)]
    connect_collectors_m3(cell, ly, q6_cols, q6_x+6.8, 0)

    # Q1+Q2 emitters → M2 bus (connect to Q5.C via M3→M2)
    q1_emis = [hbt_emi(q1_x, q1_y0+i*sp) for i in range(2)]
    q2_emis = [hbt_emi(q2_x, q2_y0+i*sp) for i in range(2)]
    all_left_emis = q1_emis + q2_emis
    connect_emitters_m2(cell, ly, all_left_emis, q5_x+1.0)
    # Bridge Q5.C (M3) down to left LO emitters (M2)
    bridge_l_y = (q5_cols[-1][1] + min(e[1] for e in all_left_emis)) / 2
    via_n(cell, ly, q5_x+1.0, bridge_l_y, 'M2', 'Via2', 'M3')
    cell.shapes(ly['M3']).insert(pya.Box(
        um(q5_x+0.75), um(q5_cols[-1][1]-0.25),
        um(q5_x+1.25), um(bridge_l_y+0.25)))
    cell.shapes(ly['M2']).insert(pya.Box(
        um(q5_x+0.75), um(bridge_l_y-0.25),
        um(q5_x+1.25), um(min(e[1] for e in all_left_emis)+0.25)))

    # Q3+Q4 emitters → M2 bus (connect to Q6.C via M3→M2)
    q3_emis = [hbt_emi(q3_x, q3_y0+i*sp) for i in range(2)]
    q4_emis = [hbt_emi(q4_x, q4_y0+i*sp) for i in range(2)]
    all_right_emis = q3_emis + q4_emis
    connect_emitters_m2(cell, ly, all_right_emis, q6_x+6.8)
    bridge_r_y = (q6_cols[-1][1] + min(e[1] for e in all_right_emis)) / 2
    via_n(cell, ly, q6_x+6.8, bridge_r_y, 'M2', 'Via2', 'M3')
    cell.shapes(ly['M3']).insert(pya.Box(
        um(q6_x+6.55), um(q6_cols[-1][1]-0.25),
        um(q6_x+7.05), um(bridge_r_y+0.25)))
    cell.shapes(ly['M2']).insert(pya.Box(
        um(q6_x+6.55), um(bridge_r_y-0.25),
        um(q6_x+7.05), um(min(e[1] for e in all_right_emis)+0.25)))

    # IF_P: Q1.C + Q3.C → M3 bus
    q1_cols = [hbt_col(q1_x, q1_y0+i*sp) for i in range(2)]
    q3_cols = [hbt_col(q3_x, q3_y0+i*sp) for i in range(2)]
    ifp_x = cx - 45.0
    connect_collectors_m3(cell, ly, q1_cols + q3_cols, ifp_x, 0)
    # IF_N: Q2.C + Q4.C → M3 bus
    q2_cols = [hbt_col(q2_x, q2_y0+i*sp) for i in range(2)]
    q4_cols = [hbt_col(q4_x, q4_y0+i*sp) for i in range(2)]
    ifn_x = cx + 45.0
    connect_collectors_m3(cell, ly, q2_cols + q4_cols, ifn_x, 0)

    # LO_P: Q1.B + Q4.B → M4 bus
    q1_bases = [hbt_bas(q1_x, q1_y0+i*sp) for i in range(2)]
    q4_bases = [hbt_bas(q4_x, q4_y0+i*sp) for i in range(2)]
    lop_x = cx - 50.0
    connect_bases_m4(cell, ly, q1_bases + q4_bases, lop_x, 0)
    # LO_N: Q2.B + Q3.B → M4 bus
    q2_bases = [hbt_bas(q2_x, q2_y0+i*sp) for i in range(2)]
    q3_bases = [hbt_bas(q3_x, q3_y0+i*sp) for i in range(2)]
    lon_x = cx + 50.0
    connect_bases_m4(cell, ly, q2_bases + q3_bases, lon_x, 0)

    # RF inputs: Q5.B → RFP, Q6.B → RFN (M4 bus)
    q5_bases = [hbt_bas(q5_x, q5_y0+i*sp) for i in range(4)]
    q6_bases = [hbt_bas(q6_x, q6_y0+i*sp) for i in range(4)]
    connect_bases_m4(cell, ly, q5_bases, q5_x-2.0, 0)
    connect_bases_m4(cell, ly, q6_bases, q6_x+9.8, 0)

    # Q5+Q6 emitters → TAIL (M2)
    q5_emis = [hbt_emi(q5_x, q5_y0+i*sp) for i in range(4)]
    q6_emis = [hbt_emi(q6_x, q6_y0+i*sp) for i in range(4)]
    connect_emitters_m2(cell, ly, q5_emis + q6_emis, cx)

    # CPW, via stacks, passives
    cpw(cell, ly, cx-30, cy+50, 49.0, 'up')
    cpw(cell, ly, cx+30, cy+50, 49.0, 'up')
    cpw(cell, ly, cx-30, cy-70, 125.0, 'down')
    cpw(cell, ly, cx+30, cy-70, 125.0, 'down')
    if rppd_idx:
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx-20), um(cy+55))))
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx+20), um(cy+55))))
        cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx), um(cy-55))))
    via_stack(cell, ly, cx-30, cy+50)
    via_stack(cell, ly, cx+30, cy+50)

    cell.shapes(ly['M3']).insert(pya.Box(um(10), um(H-25), um(W-10), um(H-19)))
    cell.shapes(ly['TM2']).insert(pya.Text("RFP", pya.Trans(um(cx-30), um(cy-200))))
    cell.shapes(ly['TM2']).insert(pya.Text("RFN", pya.Trans(um(cx+30), um(cy-200))))
    cell.shapes(ly['TM2']).insert(pya.Text("LOP", pya.Trans(um(cx-30), um(cy+105))))
    cell.shapes(ly['TM2']).insert(pya.Text("LON", pya.Trans(um(cx+30), um(cy+105))))

    return cell, W, H


def create_txpa(layout, ly, npn_idx, rppd_idx):
    """TX PA: Differential cascode, Nx=8
    Same topology as LNA but with 8 parallel devices per transistor.
    """
    W, H = 350.0, 550.0
    cell = layout.create_cell("TXPA_77G_XTOR")
    cx, cy = W/2, H/2
    gnd_plane(cell, ly, W, H)

    q1_x, q1_y0, sp = cx-40, cy-40, 9.0
    q2_x, q2_y0 = cx+30, cy-40
    q3_x, q3_y0 = cx-40, cy+50
    q4_x, q4_y0 = cx+30, cy+50
    place_hbts(cell, npn_idx, q1_x, q1_y0, 8, sp)
    place_hbts(cell, npn_idx, q2_x, q2_y0, 8, sp)
    place_hbts(cell, npn_idx, q3_x, q3_y0, 8, sp)
    place_hbts(cell, npn_idx, q4_x, q4_y0, 8, sp)

    # === ROUTING (same pattern as LNA) ===
    q1_cols = [hbt_col(q1_x, q1_y0+i*sp) for i in range(8)]
    connect_collectors_m3(cell, ly, q1_cols, q1_x+1.0, 0)
    q2_cols = [hbt_col(q2_x, q2_y0+i*sp) for i in range(8)]
    connect_collectors_m3(cell, ly, q2_cols, q2_x+6.8, 0)

    q3_emis = [hbt_emi(q3_x, q3_y0+i*sp) for i in range(8)]
    connect_emitters_m2(cell, ly, q3_emis, q3_x+1.0)
    q4_emis = [hbt_emi(q4_x, q4_y0+i*sp) for i in range(8)]
    connect_emitters_m2(cell, ly, q4_emis, q4_x+6.8)

    # Cascode bridges
    casc_l_x = q1_x + 1.0
    casc_l_y = (q1_cols[-1][1] + q3_emis[0][1]) / 2
    via_n(cell, ly, casc_l_x, casc_l_y, 'M2', 'Via2', 'M3')
    cell.shapes(ly['M3']).insert(pya.Box(
        um(casc_l_x-0.25), um(q1_cols[-1][1]-0.25),
        um(casc_l_x+0.25), um(casc_l_y+0.25)))
    cell.shapes(ly['M2']).insert(pya.Box(
        um(casc_l_x-0.25), um(casc_l_y-0.25),
        um(casc_l_x+0.25), um(q3_emis[0][1]+0.25)))
    casc_r_x = q2_x + 6.8
    casc_r_y = (q2_cols[-1][1] + q4_emis[0][1]) / 2
    via_n(cell, ly, casc_r_x, casc_r_y, 'M2', 'Via2', 'M3')
    cell.shapes(ly['M3']).insert(pya.Box(
        um(casc_r_x-0.25), um(q2_cols[-1][1]-0.25),
        um(casc_r_x+0.25), um(casc_r_y+0.25)))
    cell.shapes(ly['M2']).insert(pya.Box(
        um(casc_r_x-0.25), um(casc_r_y-0.25),
        um(casc_r_x+0.25), um(q4_emis[0][1]+0.25)))

    q3_cols = [hbt_col(q3_x, q3_y0+i*sp) for i in range(8)]
    connect_collectors_m3(cell, ly, q3_cols, q3_x+0.0, 0)
    q4_cols = [hbt_col(q4_x, q4_y0+i*sp) for i in range(8)]
    connect_collectors_m3(cell, ly, q4_cols, q4_x+7.8, 0)

    q1_bases = [hbt_bas(q1_x, q1_y0+i*sp) for i in range(8)]
    connect_bases_m4(cell, ly, q1_bases, q1_x+0.0, 0)
    q2_bases = [hbt_bas(q2_x, q2_y0+i*sp) for i in range(8)]
    connect_bases_m4(cell, ly, q2_bases, q2_x+7.8, 0)

    q3_bases = [hbt_bas(q3_x, q3_y0+i*sp) for i in range(8)]
    q4_bases = [hbt_bas(q4_x, q4_y0+i*sp) for i in range(8)]
    connect_bases_m4(cell, ly, q3_bases, q3_x-2.0, 0)
    connect_bases_m4(cell, ly, q4_bases, q4_x+9.8, 0)
    vcasc_y = (q3_bases[0][1] + q3_bases[-1][1]) / 2
    cell.shapes(ly['M4']).insert(pya.Box(
        um(q3_x-2.25), um(vcasc_y-0.25),
        um(q4_x+10.05), um(vcasc_y+0.25)))

    q1_emis = [hbt_emi(q1_x, q1_y0+i*sp) for i in range(8)]
    connect_emitters_m2(cell, ly, q1_emis, q1_x+6.8)
    q2_emis = [hbt_emi(q2_x, q2_y0+i*sp) for i in range(8)]
    connect_emitters_m2(cell, ly, q2_emis, q2_x+1.0)

    cpw(cell, ly, cx-50, cy+140, 97.0, 'up')
    cpw(cell, ly, cx+50, cy+140, 97.0, 'up')
    cpw(cell, ly, cx-40, cy+140, 210.0, 'up')
    cpw(cell, ly, cx+40, cy+140, 210.0, 'up')
    cpw(cell, ly, cx-40, cy-50, 58.0, 'down')
    cpw(cell, ly, cx+40, cy-50, 58.0, 'down')
    via_stack(cell, ly, cx-40, cy+140)
    via_stack(cell, ly, cx+40, cy+140)
    if rppd_idx: cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx), um(cy+130))))

    cell.shapes(ly['M3']).insert(pya.Box(um(10), um(H-25), um(W-10), um(H-19)))
    cell.shapes(ly['TM2']).insert(pya.Text("INP", pya.Trans(um(cx-50), um(cy+240))))
    cell.shapes(ly['TM2']).insert(pya.Text("INN", pya.Trans(um(cx+50), um(cy+240))))
    cell.shapes(ly['TM2']).insert(pya.Text("OUTP", pya.Trans(um(cx-40), um(cy+355))))
    cell.shapes(ly['TM2']).insert(pya.Text("OUTN", pya.Trans(um(cx+40), um(cy+355))))

    return cell, W, H


def create_ilfd(layout, ly, npn_idx, rppd_idx):
    """ILFD: Injection-locked frequency divider
    Cross-coupled: Q1.C→Q2.B, Q2.C→Q1.B (OUTP/OUTN)
    Injection: Q3.C→Q1.E, Q4.C→Q2.E
    Q3.B→INP, Q4.B→INN, Q1.E+Q2.E=TAIL
    """
    W, H = 350.0, 600.0
    cell = layout.create_cell("ILFD_77G_XTOR")
    cx, cy = W/2, H/2
    gnd_plane(cell, ly, W, H)

    q1_x, q1_y0, sp = cx-20, cy-10, 9.0
    q2_x, q2_y0 = cx+10, cy-10
    q3_x, q3_y0 = cx-20, cy-40
    q4_x, q4_y0 = cx+10, cy-40
    place_hbts(cell, npn_idx, q1_x, q1_y0, 2, sp)
    place_hbts(cell, npn_idx, q2_x, q2_y0, 2, sp)
    place_hbts(cell, npn_idx, q3_x, q3_y0, 2, sp)
    place_hbts(cell, npn_idx, q4_x, q4_y0, 2, sp)

    # === ROUTING ===
    # Cross-coupling: Q1.C→OUTP (M3), Q2.C→OUTN (M3)
    # Q1.C also connects to Q2.B, Q2.C also connects to Q1.B
    # Use M3 for OUTP, M4 for OUTN (avoid crossing)
    q1_cols = [hbt_col(q1_x, q1_y0+i*sp) for i in range(2)]
    q2_cols = [hbt_col(q2_x, q2_y0+i*sp) for i in range(2)]
    q1_bases = [hbt_bas(q1_x, q1_y0+i*sp) for i in range(2)]
    q2_bases = [hbt_bas(q2_x, q2_y0+i*sp) for i in range(2)]

    # OUTP = Q1.C + Q2.B on M3
    outp_pins = q1_cols + q2_bases
    outp_bus_x = q1_x - 2.0
    connect_collectors_m3(cell, ly, outp_pins, outp_bus_x, 0)

    # OUTN = Q2.C + Q1.B on M4
    outn_pins = q2_cols + q1_bases
    outn_bus_x = q2_x + 9.8
    connect_bases_m4(cell, ly, outn_pins, outn_bus_x, 0)

    # Injection: Q3.C → Q1.E (M2), Q4.C → Q2.E (M2)
    q3_cols = [hbt_col(q3_x, q3_y0+i*sp) for i in range(2)]
    q4_cols = [hbt_col(q4_x, q4_y0+i*sp) for i in range(2)]
    q1_emis = [hbt_emi(q1_x, q1_y0+i*sp) for i in range(2)]
    q2_emis = [hbt_emi(q2_x, q2_y0+i*sp) for i in range(2)]

    # Q3.C bus (M3) → bridge to Q1.E bus (M2)
    connect_collectors_m3(cell, ly, q3_cols, q3_x+1.0, 0)
    connect_emitters_m2(cell, ly, q1_emis, q1_x+1.0)
    inj_l_y = (q3_cols[-1][1] + q1_emis[0][1]) / 2
    via_n(cell, ly, q3_x+1.0, inj_l_y, 'M2', 'Via2', 'M3')
    cell.shapes(ly['M3']).insert(pya.Box(
        um(q3_x+0.75), um(q3_cols[-1][1]-0.25),
        um(q3_x+1.25), um(inj_l_y+0.25)))
    cell.shapes(ly['M2']).insert(pya.Box(
        um(q3_x+0.75), um(inj_l_y-0.25),
        um(q3_x+1.25), um(q1_emis[0][1]+0.25)))

    # Q4.C bus (M3) → bridge to Q2.E bus (M2)
    connect_collectors_m3(cell, ly, q4_cols, q4_x+6.8, 0)
    connect_emitters_m2(cell, ly, q2_emis, q4_x+6.8)
    inj_r_y = (q4_cols[-1][1] + q2_emis[0][1]) / 2
    via_n(cell, ly, q4_x+6.8, inj_r_y, 'M2', 'Via2', 'M3')
    cell.shapes(ly['M3']).insert(pya.Box(
        um(q4_x+6.55), um(q4_cols[-1][1]-0.25),
        um(q4_x+7.05), um(inj_r_y+0.25)))
    cell.shapes(ly['M2']).insert(pya.Box(
        um(q4_x+6.55), um(inj_r_y-0.25),
        um(q4_x+7.05), um(q2_emis[0][1]+0.25)))

    # Q3.B → INP, Q4.B → INN (M4)
    q3_bases = [hbt_bas(q3_x, q3_y0+i*sp) for i in range(2)]
    q4_bases = [hbt_bas(q4_x, q4_y0+i*sp) for i in range(2)]
    connect_bases_m4(cell, ly, q3_bases, q3_x-2.0, 0)
    connect_bases_m4(cell, ly, q4_bases, q4_x+9.8, 0)

    # Q3+Q4 emitters → TAIL (M2)
    q3_emis = [hbt_emi(q3_x, q3_y0+i*sp) for i in range(2)]
    q4_emis = [hbt_emi(q4_x, q4_y0+i*sp) for i in range(2)]
    connect_emitters_m2(cell, ly, q3_emis + q4_emis, cx)

    # CPW resonators and chokes
    cpw(cell, ly, cx-50, cy+20, 270.0, 'up')
    cpw(cell, ly, cx+50, cy+20, 270.0, 'up')
    cpw(cell, ly, cx-50, cy-60, 250.0, 'down')
    cpw(cell, ly, cx+50, cy-60, 250.0, 'down')
    via_stack(cell, ly, cx-50, cy+20)
    via_stack(cell, ly, cx+50, cy+20)
    if rppd_idx: cell.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(cx), um(cy-55))))

    cell.shapes(ly['M3']).insert(pya.Box(um(10), um(10), um(W-10), um(16)))
    cell.shapes(ly['TM2']).insert(pya.Text("INP", pya.Trans(um(cx-20), um(cy-60))))
    cell.shapes(ly['TM2']).insert(pya.Text("INN", pya.Trans(um(cx+20), um(cy-60))))
    cell.shapes(ly['TM2']).insert(pya.Text("OUTP", pya.Trans(um(cx-50), um(cy+325))))
    cell.shapes(ly['TM2']).insert(pya.Text("OUTN", pya.Trans(um(cx+50), um(cy+325))))

    return cell, W, H


def main():
    layout = pya.Layout()
    layout.dbu = DBU
    layout.read(PDK_GDS)

    ly = {}
    for name, (ln, dt) in LAYERS.items():
        ly[name] = layout.layer(ln, dt)

    npn_idx = layout.cell_by_name("npn13G2L") if layout.has_cell("npn13G2L") else None
    cmim_idx = layout.cell_by_name("cmim") if layout.has_cell("cmim") else None
    rppd_idx = layout.cell_by_name("rppd") if layout.has_cell("rppd") else None

    if npn_idx is None:
        print("ERROR: npn13G2L not found in PDK GDS")
        return

    results = []

    lna, lw, lh = create_lna(layout, ly, npn_idx, cmim_idx, rppd_idx)
    results.append(("LNA_77G_XTOR", lw, lh, "16×npn + 2×cmim + 1×rppd"))

    mix, mw, mh = create_mixer(layout, ly, npn_idx, rppd_idx)
    results.append(("MIXER_77G_XTOR", mw, mh, "16×npn + 3×rppd"))

    txpa, tw, th = create_txpa(layout, ly, npn_idx, rppd_idx)
    results.append(("TXPA_77G_XTOR", tw, th, "32×npn + 1×rppd"))

    ilfd, iw, ih = create_ilfd(layout, ly, npn_idx, rppd_idx)
    results.append(("ILFD_77G_XTOR", iw, ih, "8×npn + 1×rppd"))

    # Save individual GDS files
    for cell_name, w, h, devs in results:
        ci = layout.cell_by_name(cell_name)
        out = f"{OUT_DIR}{cell_name}.gds"
        layout.write(out, pya.SaveLayoutOptions())
        print(f"  {cell_name}: {w}×{h}µm, {devs}")

    # Save combined GDS with all blocks
    combined = f"{OUT_DIR}ALL_BLOCKS_77G.gds"
    layout.write(combined)
    print(f"\nCombined GDS: {combined}")
    print(f"Cells: {', '.join(r[0] for r in results)}")


if __name__ == "__main__":
    main()
