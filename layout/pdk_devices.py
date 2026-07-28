"""
Parameterized PDK device generators for IHP SG13G2.
Creates LVS-correct geometry for rppd, cap_cmim, and npn13G2l.
"""

import pya

DBU = 0.001  # 1nm database unit


def um(val):
    snapped = round(val / 0.005) * 0.005
    return int(snapped / DBU)


def snap(val):
    return round(val / 0.005) * 0.005


def create_rppd(cell, layout, x, y, w_um, l_um, m=1):
    """
    Create a parameterized rppd resistor at (x, y) in um.
    w_um: resistor width in um
    l_um: resistor length in um
    m: number of parallel instances (placed side by side)

    Returns dict with pin positions: {'P': (px,py), 'M': (mx,my)}
    The resistor body runs vertically (length in Y direction).

    Layer mapping (from PDK rppd cell analysis):
      gatpoly (5,0): poly body + port extensions
      cont (6,0): contact between poly and M1
      M1 (8,0): metal contacts (pins)
      M1_pin (8,2): pin markers
      psd_drw (14,0): p-implant
      salblock (28,0): salicide block
      psd2 (52,0): secondary p-implant marker
      polyres_drw (128,0): resistor body marker
    """
    ly_gatpoly = layout.layer(5, 0)
    ly_cont = layout.layer(6, 0)
    ly_m1 = layout.layer(8, 0)
    ly_m1_pin = layout.layer(8, 2)
    ly_psd = layout.layer(14, 0)
    ly_salblock = layout.layer(28, 0)
    ly_psd2 = layout.layer(52, 0)
    ly_extblock = layout.layer(111, 0)
    ly_polyres = layout.layer(128, 0)

    w = w_um * 1000  # convert to nm (database units)
    l = l_um * 1000

    # Margins (from PDK cell analysis, scaled)
    port_ext = 200  # poly extension beyond body for contacts
    cont_margin = 70  # contact inset from poly edge
    cont_h = 160  # contact height
    m1_margin = 20  # M1 inset from poly edge
    m1_h = 300  # M1 pad height
    sal_margin = 200  # salblock overhang
    psd_margin = 180  # psd overhang

    pins = []

    for i in range(m):
        ox = int(x * 1000 + i * (w + 500))  # 500nm spacing between instances
        oy = int(y * 1000)

        # Resistor body center at (ox + w/2, oy + l/2)
        bx = ox
        by = oy

        # polyres_drw (128,0): resistor body marker
        cell.shapes(ly_polyres).insert(pya.Box(bx, by, int(bx + w), int(by + l)))

        # extblock_drw (111,0): required for polyres_mk derivation
        cell.shapes(ly_extblock).insert(pya.Box(
            int(bx - psd_margin), int(by - port_ext - 180),
            int(bx + w + psd_margin), int(by + l + port_ext + 180)))

        # psd2 (52,0): same as polyres
        cell.shapes(ly_psd2).insert(pya.Box(bx, by, int(bx + w), int(by + l)))

        # salblock (28,0): covers body with margin
        cell.shapes(ly_salblock).insert(pya.Box(
            int(bx - sal_margin), by,
            int(bx + w + sal_margin), int(by + l)))

        # gatpoly (5,0): full poly strip from bottom contact to top contact
        # Bottom port extension
        cell.shapes(ly_gatpoly).insert(pya.Box(
            bx, int(by - port_ext), int(bx + w), by))
        # Resistor body
        cell.shapes(ly_gatpoly).insert(pya.Box(
            bx, by, int(bx + w), int(by + l)))
        # Top port extension
        cell.shapes(ly_gatpoly).insert(pya.Box(
            bx, int(by + l), int(bx + w), int(by + l + port_ext)))

        # psd_drw (14,0): covers full area including contacts
        cell.shapes(ly_psd).insert(pya.Box(
            int(bx - psd_margin), int(by - port_ext - 180),
            int(bx + w + psd_margin), int(by + l + port_ext + 180)))

        # Contacts (6,0): at top and bottom port extensions
        # Bottom contact
        cell.shapes(ly_cont).insert(pya.Box(
            int(bx + cont_margin), int(by - port_ext + 40),
            int(bx + w - cont_margin), int(by - port_ext + 40 + cont_h)))
        # Top contact
        cell.shapes(ly_cont).insert(pya.Box(
            int(bx + cont_margin), int(by + l + port_ext - 40 - cont_h),
            int(bx + w - cont_margin), int(by + l + port_ext - 40)))

        # M1 (8,0): metal pads at top and bottom
        # Bottom M1 (Pin M = minus)
        m1_bot_y1 = int(by - port_ext - 100)
        m1_bot_y2 = int(by - port_ext + m1_h - 100)
        cell.shapes(ly_m1).insert(pya.Box(
            int(bx + m1_margin), m1_bot_y1,
            int(bx + w - m1_margin), m1_bot_y2))
        cell.shapes(ly_m1_pin).insert(pya.Box(
            int(bx + m1_margin), m1_bot_y1,
            int(bx + w - m1_margin), m1_bot_y2))

        # Top M1 (Pin P = plus)
        m1_top_y1 = int(by + l + port_ext - m1_h + 100)
        m1_top_y2 = int(by + l + port_ext + 100)
        cell.shapes(ly_m1).insert(pya.Box(
            int(bx + m1_margin), m1_top_y1,
            int(bx + w - m1_margin), m1_top_y2))
        cell.shapes(ly_m1_pin).insert(pya.Box(
            int(bx + m1_margin), m1_top_y1,
            int(bx + w - m1_margin), m1_top_y2))

        if i == 0:
            # Return pin centers of first instance (in um)
            pin_p = (x + w_um / 2, (m1_top_y1 + m1_top_y2) / 2 / 1000)
            pin_m = (x + w_um / 2, (m1_bot_y1 + m1_bot_y2) / 2 / 1000)

    total_w = m * w + (m - 1) * 500
    pins = {
        'P': pin_p,
        'M': pin_m,
        'bbox_w': total_w / 1000,
        'bbox_h': (l + 2 * port_ext + 2 * 200) / 1000,
    }
    return pins
