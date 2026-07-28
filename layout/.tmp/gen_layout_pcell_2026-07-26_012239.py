"""
Generate layout with PDK PCells loaded via technology bootstrap.
Then run DRC and LVS preparation.
"""
import sys
import os

# Bootstrap PDK python modules
pdk_python = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/python"
sys.path.insert(0, pdk_python)
sys.path.insert(0, os.path.join(pdk_python, "pycell4klayout-api/source/python"))

import pya

# Load PDK PCell libraries
try:
    import sg13g2_pycell_lib
    import sg13g2_native_pcell_lib
    PCELLS_LOADED = True
    print("PDK PCell libraries loaded successfully.")
except Exception as e:
    PCELLS_LOADED = False
    print(f"WARNING: Could not load PDK PCells: {e}")
    print("Falling back to placeholder layout.")

# Constants
DBU = 0.001
GDS_OUT = "/home/bthomas3/Videos/77GHz_phased_array/layout/RADAR_TOP.gds"

layout = pya.Layout()
layout.dbu = DBU

def um(val):
    return int(val / DBU)

def create_pcell_in_cell(parent_cell, pcell_name, lib_name, params, x_um, y_um):
    """Try to create a PCell instance; fall back to placeholder."""
    lib = pya.Library.library_by_name(lib_name)
    if lib:
        pcell_decl = lib.layout().pcell_declaration(pcell_name)
        if pcell_decl:
            pcell_var = layout.add_pcell_variant(lib, pcell_decl.id(), params)
            bbox = layout.cell(pcell_var).bbox()
            trans = pya.Trans(um(x_um) - bbox.left, um(y_um) - bbox.bottom)
            parent_cell.insert(pya.CellInstArray(pcell_var, trans))
            return (bbox.width() * DBU, bbox.height() * DBU)
    # Fallback placeholder
    layer = layout.layer(1, 0)
    w, h = 8.0, 10.0
    parent_cell.shapes(layer).insert(pya.Box(um(x_um), um(y_um), um(x_um+w), um(y_um+h)))
    tl = layout.layer(63, 0)
    parent_cell.shapes(tl).insert(pya.Text(f"{pcell_name}", pya.Trans(um(x_um), um(y_um+h/2))))
    return (w, h)

def place_npn(cell, x, y, nx=1, el=2.5, name=""):
    params = {"Nx": nx, "le": f"{el}u", "we": "0.07u"}
    create_pcell_in_cell(cell, "npn13G2L", "SG13_dev", params, x, y)
    tl = layout.layer(63, 0)
    cell.shapes(tl).insert(pya.Text(name, pya.Trans(um(x), um(y-1))))

def place_nmos(cell, x, y, w="8u", l="200n", ng=4, m=1, name=""):
    params = {"w": w, "l": l, "ng": ng, "m": m}
    create_pcell_in_cell(cell, "nmos", "SG13_dev", params, x, y)
    tl = layout.layer(63, 0)
    cell.shapes(tl).insert(pya.Text(name, pya.Trans(um(x), um(y-1))))

def place_pmos(cell, x, y, w="4u", l="200n", ng=2, m=1, name=""):
    params = {"w": w, "l": l, "ng": ng, "m": m}
    create_pcell_in_cell(cell, "pmos", "SG13_dev", params, x, y)
    tl = layout.layer(63, 0)
    cell.shapes(tl).insert(pya.Text(name, pya.Trans(um(x), um(y-1))))

def place_res(cell, x, y, value, name=""):
    # Placeholder for resistor - PDK has various res types
    layer = layout.layer(19, 0)
    r_len = max(5.0, min(50.0, value * 0.01))
    cell.shapes(layer).insert(pya.Box(um(x), um(y), um(x+r_len), um(y+2)))
    tl = layout.layer(63, 0)
    cell.shapes(tl).insert(pya.Text(f"{name}={value}", pya.Trans(um(x), um(y+1))))

def place_tl(cell, x, y, length_um, name=""):
    """Transmission line on TopMetal2 (layer 134,0)"""
    layer = layout.layer(134, 0)
    w_um = 4.0  # ~50ohm microstrip width at 77GHz on SG13G2
    cell.shapes(layer).insert(pya.Box(um(x), um(y), um(x+length_um), um(y+w_um)))
    tl = layout.layer(63, 0)
    cell.shapes(tl).insert(pya.Text(name, pya.Trans(um(x), um(y+w_um+1))))

def add_supply_rings(cell, w_um, h_um):
    """Add VCC/GND supply rings on Metal1/Metal2"""
    m1 = layout.layer(8, 0)   # Metal1
    m2 = layout.layer(10, 0)  # Metal2
    ring_w = 3.0
    # Bottom GND
    cell.shapes(m1).insert(pya.Box(um(-ring_w), um(-ring_w), um(w_um+ring_w), um(0)))
    # Top VCC
    cell.shapes(m2).insert(pya.Box(um(-ring_w), um(h_um), um(w_um+ring_w), um(h_um+ring_w)))
    # Left GND
    cell.shapes(m1).insert(pya.Box(um(-ring_w), um(-ring_w), um(0), um(h_um+ring_w)))
    # Right VCC
    cell.shapes(m2).insert(pya.Box(um(w_um), um(-ring_w), um(w_um+ring_w), um(h_um+ring_w)))

# ============================================================
# Block cells with proper device placement
# ============================================================

def create_ifa():
    cell = layout.create_cell("IFA_77G")
    # Stage 1 diff pair
    place_npn(cell, 10, 30, nx=2, name="Q1")
    place_npn(cell, 40, 30, nx=2, name="Q2")
    place_res(cell, 10, 45, 500, "RL1")
    place_res(cell, 40, 45, 500, "RL2")
    # Stage 2 diff pair
    place_npn(cell, 10, 10, nx=2, name="Q3")
    place_npn(cell, 40, 10, nx=2, name="Q4")
    place_res(cell, 10, 25, 500, "RL3")
    place_res(cell, 40, 25, 500, "RL4")
    add_supply_rings(cell, 60, 55)
    return cell

def create_lvlshift():
    cell = layout.create_cell("LVLSHIFT_77G")
    place_npn(cell, 10, 5, nx=2, name="Q1")
    place_npn(cell, 40, 5, nx=2, name="Q2")
    add_supply_rings(cell, 60, 20)
    return cell

def create_vga():
    cell = layout.create_cell("VGA_77G")
    place_npn(cell, 10, 20, nx=2, name="Q1")
    place_npn(cell, 40, 20, nx=2, name="Q2")
    place_npn(cell, 25, 5, nx=4, name="Qtail")
    place_res(cell, 10, 35, 500, "RL1")
    place_res(cell, 40, 35, 500, "RL2")
    place_res(cell, 25, 0, 10, "RE")
    add_supply_rings(cell, 60, 45)
    return cell

def create_adc():
    cell = layout.create_cell("ADC_SAR_12B")
    # NMOS input pair
    place_nmos(cell, 5, 10, w="8u", ng=4, m=4, name="M1")
    place_nmos(cell, 25, 10, w="8u", ng=4, m=4, name="M2")
    # Tail
    place_nmos(cell, 15, 0, w="8u", ng=4, m=2, name="M9")
    # Cross-coupled NMOS latch
    place_nmos(cell, 5, 22, w="4u", ng=2, m=2, name="M5")
    place_nmos(cell, 25, 22, w="4u", ng=2, m=2, name="M6")
    # Cross-coupled PMOS latch
    place_pmos(cell, 5, 34, w="4u", ng=2, m=2, name="M3")
    place_pmos(cell, 25, 34, w="4u", ng=2, m=2, name="M4")
    # Precharge
    place_pmos(cell, 5, 44, w="2u", ng=1, m=2, name="M7")
    place_pmos(cell, 25, 44, w="2u", ng=1, m=2, name="M8")
    add_supply_rings(cell, 40, 55)
    return cell

def create_digif():
    cell = layout.create_cell("DIGIF_CML")
    place_npn(cell, 10, 5, nx=2, name="Q1")
    place_npn(cell, 35, 5, nx=2, name="Q2")
    place_res(cell, 10, 18, 50, "RT1")
    place_res(cell, 35, 18, 50, "RT2")
    add_supply_rings(cell, 50, 25)
    return cell

def create_bias():
    cell = layout.create_cell("BIAS_BGR")
    place_npn(cell, 5, 15, nx=1, name="Q1_1x")
    place_npn(cell, 30, 15, nx=8, name="Q2_8x")
    place_res(cell, 5, 0, 5400, "R1_5k4")
    place_res(cell, 5, 30, 50, "Rfb")
    place_res(cell, 30, 30, 100, "Rout")
    place_res(cell, 70, 10, 18000, "R2_18k")
    add_supply_rings(cell, 120, 40)
    return cell

def create_lna():
    cell = layout.create_cell("LNA_77G")
    # Input stage
    place_npn(cell, 10, 20, nx=4, name="Q33")
    place_npn(cell, 55, 20, nx=4, name="Q34")
    # Cascode
    place_npn(cell, 10, 40, nx=4, name="Q35")
    place_npn(cell, 55, 40, nx=4, name="Q36")
    # Bias
    place_npn(cell, 35, 5, nx=1, name="Q37_bias")
    # TL input matching
    place_tl(cell, 0, 55, 97, "TL_in_P")
    place_tl(cell, 0, 62, 97, "TL_in_N")
    # TL output matching
    place_tl(cell, 0, 70, 151, "TL_out_P")
    place_tl(cell, 0, 77, 151, "TL_out_N")
    # TL bias
    place_tl(cell, 0, 84, 58, "TL_bias")
    add_supply_rings(cell, 155, 92)
    return cell

def create_mixer():
    cell = layout.create_cell("MIXER_77G")
    # Switching quad
    place_npn(cell, 10, 40, nx=4, name="Q22")
    place_npn(cell, 55, 40, nx=4, name="Q23")
    place_npn(cell, 10, 55, nx=4, name="Q24")
    place_npn(cell, 55, 55, nx=4, name="Q25")
    # Transconductor pair
    place_npn(cell, 10, 15, nx=4, name="Q20")
    place_npn(cell, 55, 15, nx=4, name="Q21")
    # Bias
    place_npn(cell, 30, 0, nx=1, name="Q26")
    place_npn(cell, 45, 0, nx=1, name="Q27")
    # TL matching
    place_tl(cell, 0, 70, 66, "TL_LO")
    place_tl(cell, 0, 77, 125, "TL_RF")
    add_supply_rings(cell, 130, 85)
    return cell

def create_vco():
    cell = layout.create_cell("VCO_77G")
    place_npn(cell, 10, 10, nx=2, name="Q1")
    place_npn(cell, 40, 10, nx=2, name="Q2")
    # Inductor as octagonal spiral on TopMetal2
    tm2 = layout.layer(134, 0)
    # Outer ring
    pts = [pya.Point(um(15), um(30)), pya.Point(um(50), um(30)),
           pya.Point(um(55), um(35)), pya.Point(um(55), um(60)),
           pya.Point(um(50), um(65)), pya.Point(um(15), um(65)),
           pya.Point(um(10), um(60)), pya.Point(um(10), um(35))]
    cell.shapes(tm2).insert(pya.Path(pts, um(3)))
    tl = layout.layer(63, 0)
    cell.shapes(tl).insert(pya.Text("L_27pH", pya.Trans(um(25), um(45))))
    add_supply_rings(cell, 65, 70)
    return cell

def create_txpa():
    cell = layout.create_cell("TXPA_77G")
    # Left cascode
    place_npn(cell, 5, 10, nx=8, name="Q1_CE")
    place_npn(cell, 5, 30, nx=8, name="Q3_CB")
    # Right cascode
    place_npn(cell, 80, 10, nx=8, name="Q2_CE")
    place_npn(cell, 80, 30, nx=8, name="Q4_CB")
    # Output TL matching network
    place_tl(cell, 5, 48, 210, "TL_out_P")
    place_tl(cell, 5, 55, 210, "TL_out_N")
    # Degeneration stubs
    place_tl(cell, 5, 0, 58, "TL_deg_P")
    place_tl(cell, 80, 0, 58, "TL_deg_N")
    add_supply_rings(cell, 220, 65)
    return cell

def create_ilfd():
    cell = layout.create_cell("ILFD_77G")
    place_npn(cell, 10, 10, nx=2, name="Q1_XC")
    place_npn(cell, 40, 10, nx=2, name="Q2_XC")
    place_npn(cell, 25, 0, nx=2, name="Q_INJ")
    # TL stubs (280um each)
    place_tl(cell, 0, 25, 280, "TL_stub_P")
    place_tl(cell, 0, 32, 280, "TL_stub_N")
    add_supply_rings(cell, 285, 40)
    return cell

# ============================================================
# Create block cells
# ============================================================
print("Creating block cells...")
ifa = create_ifa()
lvl = create_lvlshift()
vga = create_vga()
adc = create_adc()
digif = create_digif()
bias = create_bias()
lna = create_lna()
mixer = create_mixer()
vco = create_vco()
txpa = create_txpa()
ilfd = create_ilfd()

# ============================================================
# Top-level floorplan — realistic die size
# ============================================================
print("Assembling top-level floorplan...")
top = layout.create_cell("RADAR_TOP")

# Die ~1.2mm x 0.8mm (reasonable for this circuit in 130nm)
# Floorplan rows:
# Row 0 (y=0):    BIAS (120x40)
# Row 1 (y=60):   IFA(60x55) LVLS(60x20) VGA(60x45) ADC(40x55) DIGIF(50x25)
# Row 2 (y=170):  LNA(155x92) MIXER(130x85)
# Row 3 (y=310):  TXPA(220x65) VCO(65x70) ILFD(285x40)

# Row 0: Bias
top.insert(pya.CellInstArray(bias.cell_index(), pya.Trans(um(50), um(10))))

# Row 1: Baseband chain
top.insert(pya.CellInstArray(ifa.cell_index(), pya.Trans(um(10), um(70))))
top.insert(pya.CellInstArray(lvl.cell_index(), pya.Trans(um(80), um(70))))
top.insert(pya.CellInstArray(vga.cell_index(), pya.Trans(um(150), um(70))))
top.insert(pya.CellInstArray(adc.cell_index(), pya.Trans(um(220), um(70))))
top.insert(pya.CellInstArray(digif.cell_index(), pya.Trans(um(270), um(70))))

# Row 2: RX front-end
top.insert(pya.CellInstArray(lna.cell_index(), pya.Trans(um(10), um(180))))
top.insert(pya.CellInstArray(mixer.cell_index(), pya.Trans(um(180), um(180))))

# Row 3: TX chain
top.insert(pya.CellInstArray(txpa.cell_index(), pya.Trans(um(10), um(320))))
top.insert(pya.CellInstArray(vco.cell_index(), pya.Trans(um(250), um(320))))
top.insert(pya.CellInstArray(ilfd.cell_index(), pya.Trans(um(330), um(320))))

# Die boundary
boundary = layout.layer(0, 0)
die_w, die_h = 650, 420
top.shapes(boundary).insert(pya.Box(um(0), um(0), um(die_w), um(die_h)))

# Pad ring (bondpad placeholders on TopMetal2)
tm2 = layout.layer(134, 0)
pad_size = 70  # 70x70um pads
pad_pitch = 100
# Bottom pads
for i in range(6):
    x = 50 + i * pad_pitch
    top.shapes(tm2).insert(pya.Box(um(x), um(-pad_size-10), um(x+pad_size), um(-10)))
    tl = layout.layer(63, 0)
    labels = ["GND", "VCC_33", "VDD_12", "VTUNE", "VCTRL", "CLK"]
    top.shapes(tl).insert(pya.Text(labels[i], pya.Trans(um(x+10), um(-pad_size))))
# Top pads
for i in range(4):
    x = 100 + i * pad_pitch
    top.shapes(tm2).insert(pya.Box(um(x), um(die_h+10), um(x+pad_size), um(die_h+pad_size+10)))
    tl = layout.layer(63, 0)
    labels = ["ANT_TXP", "ANT_TXN", "ANT_RXP", "ANT_RXN"]
    top.shapes(tl).insert(pya.Text(labels[i], pya.Trans(um(x+10), um(die_h+pad_size))))
# Right pads
for i in range(2):
    y = 100 + i * pad_pitch
    top.shapes(tm2).insert(pya.Box(um(die_w+10), um(y), um(die_w+pad_size+10), um(y+pad_size)))
    tl = layout.layer(63, 0)
    labels = ["DOUT_P", "DOUT_N"]
    top.shapes(tl).insert(pya.Text(labels[i], pya.Trans(um(die_w+20), um(y+30))))

# Save GDS
layout.write(GDS_OUT)
print(f"\n{'='*60}")
print(f"Layout written: {GDS_OUT}")
print(f"Die size: {die_w}um x {die_h}um ({die_w/1000:.2f}mm x {die_h/1000:.2f}mm)")
print(f"Cells: {layout.cells()} total ({11} block cells + top + PCells)")
print(f"{'='*60}")
print(f"\nNext steps:")
print(f"1. Open in KLayout with PDK: klayout -e -t sg13g2 {GDS_OUT}")
print(f"2. Replace placeholders with real PCells via Import Netlist macro")
print(f"3. Route metal interconnects")
print(f"4. Run DRC: Macros → sg13g2_drc")
print(f"5. Run LVS: Macros → sg13g2_lvs (compare vs xschem netlist)")
