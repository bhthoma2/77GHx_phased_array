"""
77 GHz Phased Array — Bias Network Layout
Current mirrors and cascode bias for all blocks on IHP SG13G2
"""

import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"

LAYERS = {
    'Activ': (1, 0), 'GatPoly': (5, 0), 'Cont': (6, 0), 'nSD': (7, 0),
    'M1': (8, 0), 'M2': (10, 0), 'EmWind': (11, 0), 'pSD': (14, 0),
    'Via1': (19, 0), 'SalBlock': (28, 0), 'Via2': (29, 0), 'M3': (30, 0),
    'NWell': (31, 0), 'Via3': (49, 0), 'M4': (50, 0), 'Via4': (66, 0),
    'M5': (67, 0), 'TopVia1': (125, 0), 'TM1': (126, 0),
    'TopVia2': (133, 0), 'TM2': (134, 0), 'trans_mk': (220, 0),
}

DBU = 0.001
CELL_W = 200.0
CELL_H = 300.0


def um(val):
    snapped = round(val / 0.005) * 0.005
    return int(snapped / DBU)


def snap(val):
    return round(val / 0.005) * 0.005


def place_npn_unit(cell, ly, x, y):
    """Place one npn13G2l unit at (x,y) center"""
    ew, el = 0.07, 1.0
    cell.shapes(ly['Activ']).insert(pya.Box(um(x-ew/2), um(y-el/2), um(x+ew/2), um(y+el/2)))
    cell.shapes(ly['EmWind']).insert(pya.Box(um(x-ew/2), um(y-el/2), um(x+ew/2), um(y+el/2)))
    bw, bl = 1.0, 2.0
    cell.shapes(ly['GatPoly']).insert(pya.Box(um(x-bw/2), um(y-bl/2), um(x+bw/2), um(y+bl/2)))
    nw, nl = 3.0, 4.0
    cell.shapes(ly['NWell']).insert(pya.Box(um(x-nw/2), um(y-nl/2), um(x+nw/2), um(y+nl/2)))
    cell.shapes(ly['nSD']).insert(pya.Box(um(x-nw/2), um(y-nl/2), um(x+nw/2), um(y+nl/2)))
    cell.shapes(ly['Activ']).insert(pya.Box(um(x-nw/2+0.2), um(y-nl/2+0.2), um(x+nw/2-0.2), um(y+nl/2-0.2)))
    cell.shapes(ly['trans_mk']).insert(pya.Box(um(x-3.66), um(y-3.66), um(x+3.66), um(y+3.66)))
    # M1 collector pad (upper)
    col_dy = 5.425
    cell.shapes(ly['M1']).insert(pya.Box(um(x-0.5), um(y+col_dy-0.5), um(x+0.5), um(y+col_dy+0.5)))
    cell.shapes(ly['Cont']).insert(pya.Box(um(x-0.09), um(y+col_dy-0.09), um(x+0.09), um(y+col_dy+0.09)))
    # M1 base pad (lower)
    bas_dy = 1.775
    cell.shapes(ly['M1']).insert(pya.Box(um(x-0.5), um(y+bas_dy-0.5), um(x+0.5), um(y+bas_dy+0.5)))
    cell.shapes(ly['Cont']).insert(pya.Box(um(x-0.09), um(y+bas_dy-0.09), um(x+0.09), um(y+bas_dy+0.09)))


def place_npn_array(cell, ly, x, y, m):
    """Place m-unit npn13G2l array at starting x,y with 10µm pitch"""
    for i in range(m):
        place_npn_unit(cell, ly, x + i * 10.0, y)


def place_rppd(cell, ly, x, y, w=0.5, l=5.0):
    """Place rppd resistor at (x,y) center, horizontal orientation"""
    cell.shapes(ly['GatPoly']).insert(pya.Box(um(x-l/2), um(y-w/2), um(x+l/2), um(y+w/2)))
    cell.shapes(ly['SalBlock']).insert(pya.Box(um(x-l/2-0.2), um(y-w/2-0.2), um(x+l/2+0.2), um(y+w/2+0.2)))
    cell.shapes(ly['M1']).insert(pya.Box(um(x-l/2-1), um(y-0.5), um(x-l/2), um(y+0.5)))
    cell.shapes(ly['Cont']).insert(pya.Box(um(x-l/2-0.5-0.09), um(y-0.09), um(x-l/2-0.5+0.09), um(y+0.09)))
    cell.shapes(ly['M1']).insert(pya.Box(um(x+l/2), um(y-0.5), um(x+l/2+1), um(y+0.5)))
    cell.shapes(ly['Cont']).insert(pya.Box(um(x+l/2+0.5-0.09), um(y-0.09), um(x+l/2+0.5+0.09), um(y+0.09)))


def via_n(cell, ly, x, y, bot_layer, via_layer, top_layer):
    x, y = snap(x), snap(y)
    ps = um(0.5)
    vs = um(0.19)
    cx, cy = um(x), um(y)
    cell.shapes(ly[bot_layer]).insert(pya.Box(cx-ps//2, cy-ps//2, cx+ps//2, cy+ps//2))
    cell.shapes(ly[via_layer]).insert(pya.Box(cx-vs//2, cy-vs//2, cx+vs//2, cy+vs//2))
    cell.shapes(ly[top_layer]).insert(pya.Box(cx-ps//2, cy-ps//2, cx+ps//2, cy+ps//2))


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

    cell = layout.create_cell("BIAS_NETWORK")

    col_dy = 5.425
    bas_dy = 1.775

    # === DEVICE PLACEMENT ===
    # Row 1: Q_REF (m=1) at x=20, y=50
    place_npn_array(cell, ly, 20.0, 50.0, 1)
    # Row 2: Q_VCB1 (m=1) at x=20, y=80; Q_VCB2 (m=1) at x=40, y=80
    place_npn_array(cell, ly, 20.0, 80.0, 1)
    place_npn_array(cell, ly, 40.0, 80.0, 1)
    # Row 3: Q_MIR_ILFD (m=2) at x=20, y=120; Q_MIR_VCO (m=2) at x=50, y=120
    place_npn_array(cell, ly, 20.0, 120.0, 2)
    place_npn_array(cell, ly, 50.0, 120.0, 2)
    # Row 4: Q_MIR_MIX (m=4) at x=20, y=160
    place_npn_array(cell, ly, 20.0, 160.0, 4)
    # Row 5: Q_MIR_LNA (m=4) at x=20, y=200
    place_npn_array(cell, ly, 20.0, 200.0, 4)
    # Row 6: Q_MIR_TX (m=8) at x=20, y=240
    place_npn_array(cell, ly, 20.0, 240.0, 8)
    # Resistors at y=270
    res_xs = [20.0, 40.0, 60.0, 80.0, 100.0, 120.0]
    for rx in res_xs:
        place_rppd(cell, ly, rx, 270.0)

    # === ROUTING ===
    # MIRROR_BASE bus on M2: connects Q_REF base/collector to all mirror bases
    # Q_REF is diode-connected: short C to B on M1
    ref_x = 20.0
    # Diode connection: M1 short between collector and base of Q_REF
    cell.shapes(ly['M1']).insert(pya.Box(
        um(ref_x - 0.5), um(50.0 + bas_dy + 0.5),
        um(ref_x + 0.5), um(50.0 + col_dy - 0.5)))

    # Via from Q_REF base to M2 for mirror bus
    via_n(cell, ly, ref_x, 50.0 + bas_dy, 'M1', 'Via1', 'M2')

    # M2 MIRROR_BASE vertical bus at x=10
    mir_bus_x = 10.0
    cell.shapes(ly['M2']).insert(pya.Box(
        um(mir_bus_x - 0.25), um(50.0 + bas_dy - 0.25),
        um(mir_bus_x + 0.25), um(240.0 + bas_dy + 0.25)))
    # Horizontal from Q_REF base to bus
    cell.shapes(ly['M2']).insert(pya.Box(
        um(mir_bus_x - 0.25), um(50.0 + bas_dy - 0.25),
        um(ref_x + 0.25), um(50.0 + bas_dy + 0.25)))

    # Connect each mirror's first unit base to M2 bus
    mirror_rows = [
        (20.0, 120.0),   # Q_MIR_ILFD
        (50.0, 120.0),   # Q_MIR_VCO
        (20.0, 160.0),   # Q_MIR_MIX
        (20.0, 200.0),   # Q_MIR_LNA
        (20.0, 240.0),   # Q_MIR_TX
    ]
    for mx, my in mirror_rows:
        via_n(cell, ly, mx, my + bas_dy, 'M1', 'Via1', 'M2')
        cell.shapes(ly['M2']).insert(pya.Box(
            um(mir_bus_x - 0.25), um(my + bas_dy - 0.25),
            um(mx + 0.25), um(my + bas_dy + 0.25)))

    # For multi-unit mirrors, connect all bases on M1 horizontal
    # Q_MIR_ILFD (m=2): units at x=20,30
    for m_count, start_x, row_y in [(2, 20.0, 120.0), (2, 50.0, 120.0),
                                     (4, 20.0, 160.0), (4, 20.0, 200.0),
                                     (8, 20.0, 240.0)]:
        if m_count > 1:
            cell.shapes(ly['M1']).insert(pya.Box(
                um(start_x - 0.5), um(row_y + bas_dy - 0.25),
                um(start_x + (m_count - 1) * 10.0 + 0.5), um(row_y + bas_dy + 0.25)))

    # VCC rail on M3 at y=295 (near top)
    vcc_y = 295.0
    cell.shapes(ly['M3']).insert(pya.Box(um(5), um(vcc_y - 2.5), um(CELL_W - 5), um(vcc_y + 2.5)))

    # Connect mirror collectors to VCC via M1→M2→M3
    # For each mirror row, connect all collector pads to VCC
    for m_count, start_x, row_y in [(2, 20.0, 120.0), (2, 50.0, 120.0),
                                     (4, 20.0, 160.0), (4, 20.0, 200.0),
                                     (8, 20.0, 240.0)]:
        for i in range(m_count):
            ux = start_x + i * 10.0
            via_n(cell, ly, ux, row_y + col_dy, 'M1', 'Via1', 'M2')
            via_n(cell, ly, ux, row_y + col_dy, 'M2', 'Via2', 'M3')
        # M3 horizontal connecting to VCC rail
        cell.shapes(ly['M3']).insert(pya.Box(
            um(start_x - 0.25), um(row_y + col_dy - 0.25),
            um(start_x + (m_count - 1) * 10.0 + 0.25), um(row_y + col_dy + 0.25)))
        # M3 vertical from collector row to VCC rail
        cell.shapes(ly['M3']).insert(pya.Box(
            um(start_x - 0.25), um(row_y + col_dy - 0.25),
            um(start_x + 0.25), um(vcc_y + 0.25)))

    # VCB diode stack: Q_VCB1 and Q_VCB2 diode-connected, stacked
    for vx, vy in [(20.0, 80.0), (40.0, 80.0)]:
        cell.shapes(ly['M1']).insert(pya.Box(
            um(vx - 0.5), um(vy + bas_dy + 0.5),
            um(vx + 0.5), um(vy + col_dy - 0.5)))

    # VCB output on M4 from Q_VCB2 collector
    via_n(cell, ly, 40.0, 80.0 + col_dy, 'M1', 'Via1', 'M2')
    via_n(cell, ly, 40.0, 80.0 + col_dy, 'M2', 'Via2', 'M3')
    via_n(cell, ly, 40.0, 80.0 + col_dy, 'M3', 'Via3', 'M4')

    # === M5 PORT PADS ===
    port_pad = 5.0

    # TAIL_IN: x=100, y=10
    tail_x, tail_y = 100.0, 10.0
    via_n(cell, ly, ref_x, 50.0 + col_dy, 'M1', 'Via1', 'M2')
    via_n(cell, ly, ref_x, 50.0 + col_dy, 'M2', 'Via2', 'M3')
    via_n(cell, ly, ref_x, 50.0 + col_dy, 'M3', 'Via3', 'M4')
    via_n(cell, ly, ref_x, 50.0 + col_dy, 'M4', 'Via4', 'M5')
    # M5 trace from Q_REF collector to TAIL_IN port
    cell.shapes(ly['M5']).insert(pya.Box(
        um(ref_x - 0.25), um(tail_y - 0.25),
        um(tail_x + 0.25), um(tail_y + 0.25)))
    cell.shapes(ly['M5']).insert(pya.Box(
        um(ref_x - 0.25), um(tail_y - 0.25),
        um(ref_x + 0.25), um(50.0 + col_dy + 0.25)))
    cell.shapes(ly['M5']).insert(pya.Box(
        um(tail_x - port_pad/2), um(tail_y - port_pad/2),
        um(tail_x + port_pad/2), um(tail_y + port_pad/2)))

    # VCB_OUT: x=30, y=290
    vcb_port_x, vcb_port_y = 30.0, 290.0
    via_n(cell, ly, 40.0, 80.0 + col_dy, 'M4', 'Via4', 'M5')
    cell.shapes(ly['M5']).insert(pya.Box(
        um(vcb_port_x - 0.25), um(80.0 + col_dy - 0.25),
        um(40.0 + 0.25), um(80.0 + col_dy + 0.25)))
    cell.shapes(ly['M5']).insert(pya.Box(
        um(vcb_port_x - 0.25), um(80.0 + col_dy - 0.25),
        um(vcb_port_x + 0.25), um(vcb_port_y + 0.25)))
    cell.shapes(ly['M5']).insert(pya.Box(
        um(vcb_port_x - port_pad/2), um(vcb_port_y - port_pad/2),
        um(vcb_port_x + port_pad/2), um(vcb_port_y + port_pad/2)))

    # Mirror output ports on M5 at y=290
    # Each mirror emitter connects through degeneration resistor then to M4 port
    # For simplicity, tap from first unit emitter position (center of unit)
    mir_ports = [
        ('MIR_TX', 60.0, 290.0, 20.0, 240.0),
        ('MIR_LNA', 90.0, 290.0, 20.0, 200.0),
        ('MIR_MIX', 120.0, 290.0, 20.0, 160.0),
        ('MIR_VCO', 150.0, 290.0, 50.0, 120.0),
        ('MIR_ILFD', 170.0, 290.0, 20.0, 120.0),
    ]
    for name, px, py, dev_x, dev_y in mir_ports:
        # Via from M1 emitter area up to M2
        via_n(cell, ly, dev_x, dev_y, 'M1', 'Via1', 'M2')
        if name == 'MIR_ILFD':
            # Route MIR_ILFD on M2 at y=115 to avoid MIR_VCO M2 pad at (50,120)
            ilfd_route_y = 115.0
            # M2 vertical from (20,120) down to (20,115)
            cell.shapes(ly['M2']).insert(pya.Box(
                um(dev_x - 0.25), um(ilfd_route_y - 0.25),
                um(dev_x + 0.25), um(dev_y + 0.25)))
            # M2 horizontal from (20,115) to (170,115)
            cell.shapes(ly['M2']).insert(pya.Box(
                um(dev_x - 0.25), um(ilfd_route_y - 0.25),
                um(px + 0.25), um(ilfd_route_y + 0.25)))
            # M2 vertical from (170,115) up to (170,120)
            cell.shapes(ly['M2']).insert(pya.Box(
                um(px - 0.25), um(ilfd_route_y - 0.25),
                um(px + 0.25), um(dev_y + 0.25)))
            # Via M2→M3 at (170, 120)
            via_n(cell, ly, px, dev_y, 'M2', 'Via2', 'M3')
            # M3 vertical from (170, 120) to port (170, 290)
            cell.shapes(ly['M3']).insert(pya.Box(
                um(px - 0.25), um(dev_y - 0.25),
                um(px + 0.25), um(py + 0.25)))
        else:
            # Standard M3 L-route for all other mirrors
            via_n(cell, ly, dev_x, dev_y, 'M2', 'Via2', 'M3')
            # M3 vertical from port to dev_y level
            cell.shapes(ly['M3']).insert(pya.Box(
                um(px - 0.25), um(dev_y - 0.25),
                um(px + 0.25), um(py + 0.25)))
            # M3 horizontal from dev_x to px at dev_y
            cell.shapes(ly['M3']).insert(pya.Box(
                um(min(dev_x, px) - 0.25), um(dev_y - 0.25),
                um(max(dev_x, px) + 0.25), um(dev_y + 0.25)))
        # Via M3→M4 at port position (for external M4 connection)
        via_n(cell, ly, px, py, 'M3', 'Via3', 'M4')
        # Port pad on M4
        cell.shapes(ly['M4']).insert(pya.Box(
            um(px - port_pad/2), um(py - port_pad/2),
            um(px + port_pad/2), um(py + port_pad/2)))

    # VCC port: x=100, y=295
    vcc_port_x = 100.0
    via_n(cell, ly, vcc_port_x, vcc_y, 'M3', 'Via3', 'M4')
    via_n(cell, ly, vcc_port_x, vcc_y, 'M4', 'Via4', 'M5')
    cell.shapes(ly['M5']).insert(pya.Box(
        um(vcc_port_x - port_pad/2), um(vcc_y - port_pad/2),
        um(vcc_port_x + port_pad/2), um(vcc_y + port_pad/2)))

    # Port labels
    labels = [('TAIL_IN', tail_x, tail_y), ('VCB_OUT', vcb_port_x, vcb_port_y),
              ('MIR_TX', 60.0, 290.0), ('MIR_LNA', 90.0, 290.0),
              ('MIR_MIX', 120.0, 290.0), ('MIR_VCO', 150.0, 290.0),
              ('MIR_ILFD', 170.0, 290.0), ('VCC', vcc_port_x, vcc_y)]
    for lbl, lx, ly_pos in labels:
        cell.shapes(ly['M5']).insert(pya.Text(lbl, pya.Trans(um(lx), um(ly_pos))))

    # === TM1 GROUND PLANE (slotted) ===
    tm1_gnd = pya.Region()
    y = 5.0
    slot_pitch = 25.0
    slot_w = 2.0
    while y < CELL_H - 5:
        sh = min(slot_pitch - slot_w, CELL_H - 5 - y)
        if sh > 0:
            tm1_gnd.insert(pya.Box(um(5), um(y), um(CELL_W - 5), um(y + sh)))
        y += slot_pitch
    # Cut holes at via stack positions
    hole_sz = 9.0
    via_positions = [(tail_x, tail_y), (vcb_port_x, vcb_port_y),
                     (vcc_port_x, vcc_y), (60.0, 290.0), (90.0, 290.0),
                     (120.0, 290.0), (150.0, 290.0), (170.0, 290.0)]
    for hx, hy in via_positions:
        tm1_gnd -= pya.Region(pya.Box(
            um(snap(hx) - hole_sz/2), um(snap(hy) - hole_sz/2),
            um(snap(hx) + hole_sz/2), um(snap(hy) + hole_sz/2)))
    for p in tm1_gnd.each():
        cell.shapes(ly['TM1']).insert(p)

    if ext_layout is None:
        output = "/home/bthomas3/Videos/77GHz_phased_array/layout/BIAS_NETWORK.gds"
        layout.write(output)
        print(f"Wrote {output}")
        print(f"Cell: BIAS_NETWORK, {CELL_W} x {CELL_H} um")
        print("Devices: 21x npn13G2l + 6x rppd")

    return cell


if __name__ == "__main__":
    main()
