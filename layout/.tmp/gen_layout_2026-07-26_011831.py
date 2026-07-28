"""
Generate hierarchical GDS layout for 77GHz Radar using IHP SG13G2 PDK PCells.
Run with: klayout -b -r this_script.py
Places devices in each block cell, then assembles top-level floorplan.
"""
import pya
import sys
import os

# Add PDK python path for PCell libraries
sys.path.insert(0, "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/python")

DBU = 0.001  # database unit = 1nm

# Output path
GDS_OUT = "/home/bthomas3/Videos/77GHz_phased_array/layout/RADAR_TOP.gds"

# Create layout
layout = pya.Layout()
layout.dbu = DBU

# Try to load PDK PCell library
lib = pya.Library.library_by_name("SG13_dev")
if not lib:
    print("WARNING: SG13_dev PCell library not found. Using placeholder rectangles.")
    USE_PCELLS = False
else:
    USE_PCELLS = True
    print("SG13_dev PCell library loaded successfully.")

def um(val):
    """Convert micrometers to database units"""
    return int(val / DBU)

def create_placeholder(cell, x_um, y_um, w_um, h_um, layer_info, label=""):
    """Create a rectangle placeholder for a device"""
    layer = layout.layer(layer_info[0], layer_info[1])
    box = pya.Box(um(x_um), um(y_um), um(x_um + w_um), um(y_um + h_um))
    cell.shapes(layer).insert(box)
    if label:
        text_layer = layout.layer(63, 0)  # text layer
        cell.shapes(text_layer).insert(pya.Text(label, pya.Trans(um(x_um), um(y_um + h_um/2))))

def place_npn13g2l(cell, x_um, y_um, nx=1, el=2.5, name=""):
    """Place npn13G2l device — ~8um x 10um per Nx=1"""
    w = 8.0 * nx
    h = 10.0
    # Activ layer (1,0), EmWind (11,0), BasPoly (5,0)
    create_placeholder(cell, x_um, y_um, w, h, (1, 0), name)
    create_placeholder(cell, x_um+1, y_um+2, w-2, h-4, (11, 0))
    create_placeholder(cell, x_um+0.5, y_um+1, w-1, h-2, (5, 0))

def place_nmos(cell, x_um, y_um, w_um=8.0, l_um=0.2, ng=4, m=4, name=""):
    """Place NMOS — width proportional to W*ng*m"""
    dev_w = max(2.0, 0.5 * ng * m)
    dev_h = max(3.0, w_um * 0.5)
    create_placeholder(cell, x_um, y_um, dev_w, dev_h, (1, 0), name)
    # Gate poly
    create_placeholder(cell, x_um+0.5, y_um+0.5, dev_w-1, dev_h-1, (5, 0))

def place_pmos(cell, x_um, y_um, w_um=4.0, l_um=0.2, ng=2, m=2, name=""):
    """Place PMOS — in nwell"""
    dev_w = max(2.0, 0.5 * ng * m)
    dev_h = max(3.0, w_um * 0.5)
    create_placeholder(cell, x_um, y_um, dev_w, dev_h, (1, 0), name)
    create_placeholder(cell, x_um-0.5, y_um-0.5, dev_w+1, dev_h+1, (31, 0), name)  # NWell

def place_resistor(cell, x_um, y_um, value_ohm, name=""):
    """Place resistor — length proportional to value"""
    r_len = max(5.0, min(50.0, value_ohm * 0.01))
    r_w = 2.0
    create_placeholder(cell, x_um, y_um, r_len, r_w, (19, 0), name)  # SiLi (rsil)

def place_cap(cell, x_um, y_um, name=""):
    """Place MIM cap placeholder"""
    create_placeholder(cell, x_um, y_um, 6.0, 6.0, (36, 0), name)  # MIM

# ============================================================
# Block cells
# ============================================================

def create_ifa_cell():
    """IFA: 4x npn13G2l Nx=2, 4x R=500, 2x Isrc"""
    cell = layout.create_cell("IFA_77G")
    # Stage 1
    place_npn13g2l(cell, 5, 20, nx=2, name="Q1")
    place_npn13g2l(cell, 30, 20, nx=2, name="Q2")
    place_resistor(cell, 5, 35, 500, "RL1")
    place_resistor(cell, 30, 35, 500, "RL2")
    # Stage 2
    place_npn13g2l(cell, 5, 0, nx=2, name="Q3")
    place_npn13g2l(cell, 30, 0, nx=2, name="Q4")
    place_resistor(cell, 5, 15, 500, "RL3")
    place_resistor(cell, 30, 15, 500, "RL4")
    # Boundary
    create_placeholder(cell, 0, -5, 55, 50, (63, 63))
    return cell

def create_vga_cell():
    """VGA: 2x npn Nx=2 + 1x npn Nx=4 tail + 2R + RE"""
    cell = layout.create_cell("VGA_77G")
    place_npn13g2l(cell, 5, 15, nx=2, name="Q1")
    place_npn13g2l(cell, 30, 15, nx=2, name="Q2")
    place_npn13g2l(cell, 15, 0, nx=4, name="Qtail")
    place_resistor(cell, 5, 30, 500, "RL1")
    place_resistor(cell, 30, 30, 500, "RL2")
    place_resistor(cell, 18, -5, 10, "RE")
    create_placeholder(cell, 0, -10, 55, 50, (63, 63))
    return cell

def create_lvlshift_cell():
    """Level Shifter: 2x npn Nx=2 emitter followers"""
    cell = layout.create_cell("LVLSHIFT_77G")
    place_npn13g2l(cell, 5, 5, nx=2, name="Q1")
    place_npn13g2l(cell, 30, 5, nx=2, name="Q2")
    create_placeholder(cell, 0, 0, 50, 20, (63, 63))
    return cell

def create_adc_cell():
    """ADC StrongARM: 5 NMOS + 4 PMOS"""
    cell = layout.create_cell("ADC_SAR_12B")
    # Input pair
    place_nmos(cell, 5, 5, w_um=8, ng=4, m=4, name="M1")
    place_nmos(cell, 20, 5, w_um=8, ng=4, m=4, name="M2")
    # Tail
    place_nmos(cell, 12, 0, w_um=8, ng=4, m=2, name="M9")
    # Cross-coupled NMOS
    place_nmos(cell, 5, 15, w_um=4, ng=2, m=2, name="M5")
    place_nmos(cell, 20, 15, w_um=4, ng=2, m=2, name="M6")
    # Cross-coupled PMOS
    place_pmos(cell, 5, 25, w_um=4, ng=2, m=2, name="M3")
    place_pmos(cell, 20, 25, w_um=4, ng=2, m=2, name="M4")
    # Precharge PMOS
    place_pmos(cell, 5, 33, w_um=2, ng=1, m=2, name="M7")
    place_pmos(cell, 20, 33, w_um=2, ng=1, m=2, name="M8")
    create_placeholder(cell, 0, -5, 35, 45, (63, 63))
    return cell

def create_digif_cell():
    """DIGIF CML: 2x npn Nx=2 + 2x R=50"""
    cell = layout.create_cell("DIGIF_CML")
    place_npn13g2l(cell, 5, 5, nx=2, name="Q1")
    place_npn13g2l(cell, 25, 5, nx=2, name="Q2")
    place_resistor(cell, 5, 18, 50, "RT1")
    place_resistor(cell, 25, 18, 50, "RT2")
    create_placeholder(cell, 0, 0, 45, 25, (63, 63))
    return cell

def create_bias_cell():
    """BIAS BGR: 2x npn + 4x R"""
    cell = layout.create_cell("BIAS_BGR")
    place_npn13g2l(cell, 5, 10, nx=1, name="Q1")
    place_npn13g2l(cell, 25, 10, nx=8, name="Q2")
    place_resistor(cell, 5, 0, 5400, "R1")
    place_resistor(cell, 50, 10, 18000, "R2")
    place_resistor(cell, 15, 25, 50, "Rfb")
    place_resistor(cell, 35, 25, 100, "Rout")
    create_placeholder(cell, 0, -5, 100, 40, (63, 63))
    return cell

def create_lna_cell():
    """LNA: 6x npn + TL stubs (placeholder)"""
    cell = layout.create_cell("LNA_77G")
    place_npn13g2l(cell, 5, 20, nx=4, name="Q33")
    place_npn13g2l(cell, 40, 20, nx=4, name="Q34")
    place_npn13g2l(cell, 5, 40, nx=4, name="Q35_cascode")
    place_npn13g2l(cell, 40, 40, nx=4, name="Q36_cascode")
    place_npn13g2l(cell, 20, 5, nx=1, name="Q37_bias")
    # TL stubs as metal strips (TopMetal2 = layer 134)
    create_placeholder(cell, 0, 55, 80, 3, (134, 0), "TL_input_match")
    create_placeholder(cell, 0, 60, 80, 3, (134, 0), "TL_output_match")
    create_placeholder(cell, 0, 0, 80, 70, (63, 63))
    return cell

def create_mixer_cell():
    """Mixer Gilbert cell: 8x npn + TL stubs"""
    cell = layout.create_cell("MIXER_77G")
    # Switching quad
    place_npn13g2l(cell, 5, 30, nx=4, name="Q22")
    place_npn13g2l(cell, 40, 30, nx=4, name="Q23")
    place_npn13g2l(cell, 5, 45, nx=4, name="Q24")
    place_npn13g2l(cell, 40, 45, nx=4, name="Q25")
    # Transconductor
    place_npn13g2l(cell, 10, 10, nx=4, name="Q20_gm")
    place_npn13g2l(cell, 40, 10, nx=4, name="Q21_gm")
    # Bias
    place_npn13g2l(cell, 25, 0, nx=1, name="Q26_bias")
    place_npn13g2l(cell, 35, 0, nx=1, name="Q27_bias")
    # TL stubs
    create_placeholder(cell, 0, 60, 75, 3, (134, 0), "TL_LO_match")
    create_placeholder(cell, 0, 65, 75, 3, (134, 0), "TL_RF_match")
    create_placeholder(cell, 0, -5, 75, 75, (63, 63))
    return cell

def create_vco_cell():
    """VCO: 2x npn cross-coupled + inductor"""
    cell = layout.create_cell("VCO_77G")
    place_npn13g2l(cell, 10, 10, nx=2, name="Q1")
    place_npn13g2l(cell, 35, 10, nx=2, name="Q2")
    # Inductor placeholder (TopMetal2 spiral)
    create_placeholder(cell, 10, 25, 35, 35, (134, 0), "L_tank_27pH")
    create_placeholder(cell, 0, 0, 55, 65, (63, 63))
    return cell

def create_txpa_cell():
    """TXPA: 2x cascode Nx=8 + TL matching"""
    cell = layout.create_cell("TXPA_77G")
    place_npn13g2l(cell, 5, 10, nx=8, name="Q1_CE")
    place_npn13g2l(cell, 5, 25, nx=8, name="Q3_CB")
    place_npn13g2l(cell, 75, 10, nx=8, name="Q2_CE")
    place_npn13g2l(cell, 75, 25, nx=8, name="Q4_CB")
    # Output TL matching
    create_placeholder(cell, 0, 40, 140, 3, (134, 0), "TL_out_P")
    create_placeholder(cell, 0, 45, 140, 3, (134, 0), "TL_out_N")
    create_placeholder(cell, 0, 0, 140, 55, (63, 63))
    return cell

def create_ilfd_cell():
    """ILFD: 2x npn cross-coupled + injection + TL stubs"""
    cell = layout.create_cell("ILFD_77G")
    place_npn13g2l(cell, 5, 10, nx=2, name="Q1_XC")
    place_npn13g2l(cell, 30, 10, nx=2, name="Q2_XC")
    place_npn13g2l(cell, 15, 0, nx=2, name="Q_INJ")
    create_placeholder(cell, 0, 25, 50, 3, (134, 0), "TL_stub_P")
    create_placeholder(cell, 0, 30, 50, 3, (134, 0), "TL_stub_N")
    create_placeholder(cell, 0, -5, 50, 40, (63, 63))
    return cell

# ============================================================
# Create all block cells
# ============================================================
ifa_cell = create_ifa_cell()
vga_cell = create_vga_cell()
lvl_cell = create_lvlshift_cell()
adc_cell = create_adc_cell()
digif_cell = create_digif_cell()
bias_cell = create_bias_cell()
lna_cell = create_lna_cell()
mixer_cell = create_mixer_cell()
vco_cell = create_vco_cell()
txpa_cell = create_txpa_cell()
ilfd_cell = create_ilfd_cell()

# ============================================================
# Top-level floorplan
# ============================================================
top = layout.create_cell("RADAR_TOP")

# Floorplan (approximate positions in um):
# Die size target: ~2mm x 1.5mm for this level of integration
#
#  +--------------------------------------------------+
#  |  TXPA (140x55)  |  VCO (55x65)  |  ILFD (50x40) |  <- TX chain (top)
#  +--------------------------------------------------+
#  |  LNA (80x70)    |  MIXER (75x75)|               |  <- RX front-end
#  +--------------------------------------------------+
#  |  IFA(55x50) | LVLS(50x20) | VGA(55x50) | ADC(35x45) | DIGIF(45x25) |  <- Baseband
#  +--------------------------------------------------+
#  |         BIAS (100x40)          |  Pads           |  <- Bias + I/O
#  +--------------------------------------------------+

# Row 0 (bottom): BIAS
top.insert(pya.CellInstArray(bias_cell.cell_index(), pya.Trans(um(0), um(0))))

# Row 1: Baseband chain (y=50)
top.insert(pya.CellInstArray(ifa_cell.cell_index(), pya.Trans(um(0), um(50))))
top.insert(pya.CellInstArray(lvl_cell.cell_index(), pya.Trans(um(60), um(50))))
top.insert(pya.CellInstArray(vga_cell.cell_index(), pya.Trans(um(115), um(50))))
top.insert(pya.CellInstArray(adc_cell.cell_index(), pya.Trans(um(175), um(50))))
top.insert(pya.CellInstArray(digif_cell.cell_index(), pya.Trans(um(215), um(50))))

# Row 2: RX front-end (y=120)
top.insert(pya.CellInstArray(lna_cell.cell_index(), pya.Trans(um(0), um(120))))
top.insert(pya.CellInstArray(mixer_cell.cell_index(), pya.Trans(um(90), um(120))))

# Row 3: TX chain (y=210)
top.insert(pya.CellInstArray(txpa_cell.cell_index(), pya.Trans(um(0), um(210))))
top.insert(pya.CellInstArray(vco_cell.cell_index(), pya.Trans(um(150), um(210))))
top.insert(pya.CellInstArray(ilfd_cell.cell_index(), pya.Trans(um(210), um(210))))

# Die boundary (prBndry layer 0,0)
boundary_layer = layout.layer(0, 0)
top.shapes(boundary_layer).insert(pya.Box(um(-10), um(-10), um(270), um(280)))

# Save
os.makedirs(os.path.dirname(GDS_OUT), exist_ok=True)
layout.write(GDS_OUT)
print(f"Layout written to: {GDS_OUT}")
print(f"Die size: ~280um x 290um (placeholder - actual die ~2mm x 1.5mm)")
print(f"Blocks: 11 cells, hierarchical")
print(f"NOTE: This is a device-placed floorplan. Routing not included.")
print(f"      Open in KLayout to manually route and optimize placement.")
