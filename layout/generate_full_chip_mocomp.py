"""
Full-Chip GDS Assembly — 77 GHz Vibrometer with Motion Compensation
Merges: RF front-end + IMU analog chain + Digital DSP (post-P&R)

Die size: 2500 × 2500 µm (IHP SG13G2 MPW slot)

Floorplan:
  ┌──────────────────────────────────────────┐
  │           Bond Pads (top)                 │
  ├────────────┬─────────────┬───────────────┤
  │  RX Array  │  Digital    │  TX Array     │
  │  6× LNA+  │  DSP Core   │  4× TX PA     │
  │  Mixer    │  (P&R)      │               │
  │  800×1500 │  1000×1000  │  700×1500     │
  ├────────────┴─────────────┴───────────────┤
  │  VCO + ILFD + Phase Shifters (500×400)   │
  ├──────────────────────────────────────────┤
  │  IMU Analog Chain (500×150)              │
  │  Motion Comp SRAM + Bias (500×200)       │
  └──────────────────────────────────────────┘
"""

import pya
import os

LAYOUT_DIR = "/home/bthomas3/Videos/77GHz_phased_array/layout"
DIE_W = 2500.0
DIE_H = 2500.0
DBU = 0.001


def um(val):
    return int(round(val / 0.005) * 0.005 / DBU)


def main():
    layout = pya.Layout()
    layout.dbu = DBU

    # Load all sub-block GDS files
    gds_files = {
        'vco': os.path.join(LAYOUT_DIR, "VCO_77G_XTOR.gds"),
        'fullchip_rf': os.path.join(LAYOUT_DIR, "PHASED_ARRAY_77G_XTOR.gds"),
        'imu_analog': os.path.join(LAYOUT_DIR, "IMU_ANALOG_CHAIN.gds"),
    }

    # Check which files exist
    available = {}
    for name, path in gds_files.items():
        if os.path.exists(path):
            available[name] = path
            print(f"  Found: {name} → {path}")
        else:
            print(f"  Missing: {name} → {path}")

    # Load RF front-end (has VCO, LNA, Mixer, PA, ILFD)
    if 'fullchip_rf' in available:
        layout.read(available['fullchip_rf'])

    # Load IMU analog chain
    if 'imu_analog' in available:
        layout.read(available['imu_analog'])

    # Create top-level assembly cell
    top = layout.create_cell("VIBROMETER_FULL_CHIP")

    # Place RF front-end (already assembled as PHASED_ARRAY_77G)
    rf_idx = layout.cell_by_name("PHASED_ARRAY_77G") if layout.has_cell("PHASED_ARRAY_77G") else None
    if rf_idx is not None:
        top.insert(pya.CellInstArray(rf_idx, pya.Trans(um(0), um(0))))
        print("  Placed: RF front-end (PHASED_ARRAY_77G)")

    # Place IMU analog chain at bottom of die
    imu_idx = layout.cell_by_name("IMU_ANALOG_CHAIN") if layout.has_cell("IMU_ANALOG_CHAIN") else None
    if imu_idx is not None:
        top.insert(pya.CellInstArray(imu_idx, pya.Trans(um(1000), um(50))))
        print("  Placed: IMU analog chain at (1000, 50)")

    # Digital P&R block would be merged here after OpenROAD produces GDS
    # Placeholder: reserve area for digital core
    dig_layer = layout.layer(134, 0)  # TM2 as boundary marker
    top.shapes(dig_layer).insert(pya.Box(um(800), um(600), um(1800), um(1600)))
    top.shapes(dig_layer).insert(pya.Text("DIGITAL_DSP_CORE", pya.Trans(um(1300), um(1100))))

    # Die boundary
    boundary_layer = layout.layer(63, 0)  # Outline layer
    top.shapes(boundary_layer).insert(pya.Box(um(0), um(0), um(DIE_W), um(DIE_H)))

    output = os.path.join(LAYOUT_DIR, "VIBROMETER_FULL_CHIP.gds")
    layout.write(output)
    print(f"\nFull chip assembled: {output}")
    print(f"Die: {DIE_W} × {DIE_H} µm")
    print(f"Blocks: RF front-end + IMU analog + Digital DSP (placeholder)")


if __name__ == "__main__":
    main()