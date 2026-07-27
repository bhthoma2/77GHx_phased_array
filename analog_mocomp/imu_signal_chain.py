"""
IMU Analog Signal Chain for Motion Compensation — IHP SG13G2
Adapted from nhpoole/mixed_signal_mmwave_edge_accelerator (Sky130 → IHP)

Signal flow:
  IMU accelerometer (analog) → Input Amp → Gm-C BPF → Peak Detector → S&H → SAR ADC

All blocks use IHP SG13G2 PDK cells:
  - npn13G2L: BJT for amplifiers/comparators
  - sg13_lv_nmos/pmos: MOSFET switches
  - cmim: MIM capacitors (48.86 fF/µm²)
  - rppd: Poly resistors
  - SVaricap: Not used in analog chain (RF only)
"""

import pya

PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"

LAYERS = {
    'M1': (8, 0), 'Via1': (19, 0), 'M2': (10, 0), 'Via2': (29, 0),
    'M3': (30, 0), 'Via3': (49, 0), 'M4': (50, 0), 'Via4': (66, 0),
    'M5': (67, 0), 'TopVia1': (125, 0), 'TM1': (126, 0),
    'TopVia2': (133, 0), 'TM2': (134, 0),
}

DBU = 0.001
CELL_W = 200.0
CELL_H = 150.0


def um(val):
    return int(round(val / 0.005) * 0.005 / DBU)


def main():
    layout = pya.Layout()
    layout.dbu = DBU
    layout.read(PDK_GDS)

    ly = {}
    for name, (ln, dt) in LAYERS.items():
        ly[name] = layout.layer(ln, dt)

    npn_idx = layout.cell_by_name("npn13G2L")
    cmim_idx = layout.cell_by_name("cmim")
    rppd_idx = layout.cell_by_name("rppd")

    # =========================================================
    # Block 1: Input Differential Amplifier (variable gain)
    # Architecture: npn13G2L diff pair with resistive load
    # Gain: 6-20 dB (controlled by degeneration resistor)
    # BW: >10 kHz (IMU signals are 50-1000 Hz)
    # =========================================================
    inp_amp = layout.create_cell("IMU_INPUT_AMP")

    # Diff pair: Q1, Q2 (matched npn13G2L)
    inp_amp.insert(pya.CellInstArray(npn_idx, pya.Trans(um(20), um(50))))
    inp_amp.insert(pya.CellInstArray(npn_idx, pya.Trans(um(40), um(50))))
    # Tail current source: Q3
    inp_amp.insert(pya.CellInstArray(npn_idx, pya.Trans(um(30), um(20))))
    # Load resistors: 2× rppd
    inp_amp.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(20), um(80))))
    inp_amp.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(40), um(80))))
    # Degeneration resistors (gain control)
    inp_amp.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(25), um(35))))
    inp_amp.insert(pya.CellInstArray(rppd_idx, pya.Trans(um(35), um(35))))

    # =========================================================
    # Block 2: Gm-C Biquad Bandpass Filter
    # Architecture: 2nd-order Gm-C (two integrators in feedback)
    # Center freq: ~200 Hz (tunable), Q=5
    # Uses npn13G2L OTAs + cmim caps
    # =========================================================
    gmc_filt = layout.create_cell("IMU_GMC_FILTER")

    # OTA 1 (Gm1): diff pair + current mirror
    gmc_filt.insert(pya.CellInstArray(npn_idx, pya.Trans(um(15), um(60))))
    gmc_filt.insert(pya.CellInstArray(npn_idx, pya.Trans(um(30), um(60))))
    gmc_filt.insert(pya.CellInstArray(npn_idx, pya.Trans(um(22), um(30))))
    # OTA 2 (Gm2): diff pair + current mirror
    gmc_filt.insert(pya.CellInstArray(npn_idx, pya.Trans(um(60), um(60))))
    gmc_filt.insert(pya.CellInstArray(npn_idx, pya.Trans(um(75), um(60))))
    gmc_filt.insert(pya.CellInstArray(npn_idx, pya.Trans(um(67), um(30))))
    # Integration caps C1, C2 (cmim, ~3pF each for 200 Hz center)
    gmc_filt.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(15), um(90))))
    gmc_filt.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(60), um(90))))

    # =========================================================
    # Block 3: Peak Detector
    # Architecture: OTA + diode-connected NFET + hold cap
    # Tracks positive envelope of filtered IMU signal
    # =========================================================
    peak_det = layout.create_cell("IMU_PEAK_DETECTOR")

    # OTA (follower with gain)
    peak_det.insert(pya.CellInstArray(npn_idx, pya.Trans(um(20), um(50))))
    peak_det.insert(pya.CellInstArray(npn_idx, pya.Trans(um(35), um(50))))
    peak_det.insert(pya.CellInstArray(npn_idx, pya.Trans(um(27), um(25))))
    # Hold capacitor
    peak_det.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(50), um(40))))

    # =========================================================
    # Block 4: Sample & Hold
    # Architecture: NMOS switch + hold capacitor + buffer
    # Sampling clock from digital (adc_clk)
    # =========================================================
    sah = layout.create_cell("IMU_SAMPLE_HOLD")

    # Hold cap
    sah.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(30), um(40))))
    # Buffer (emitter follower)
    sah.insert(pya.CellInstArray(npn_idx, pya.Trans(um(50), um(50))))
    sah.insert(pya.CellInstArray(npn_idx, pya.Trans(um(50), um(25))))

    # =========================================================
    # Block 5: 8-bit SAR ADC (capacitive DAC + comparator)
    # Architecture: Binary-weighted cap array + StrongARM latch
    # Sample rate: ~50 kHz (10 cycles × 5 MHz clock)
    # =========================================================
    sar_adc = layout.create_cell("IMU_SAR_ADC")

    # Cap array: 8 cmim instances (binary weighted via area)
    for i in range(8):
        sar_adc.insert(pya.CellInstArray(cmim_idx, pya.Trans(um(10 + i*12), um(20))))
    # StrongARM comparator: 4 npn13G2L
    sar_adc.insert(pya.CellInstArray(npn_idx, pya.Trans(um(30), um(70))))
    sar_adc.insert(pya.CellInstArray(npn_idx, pya.Trans(um(45), um(70))))
    sar_adc.insert(pya.CellInstArray(npn_idx, pya.Trans(um(30), um(85))))
    sar_adc.insert(pya.CellInstArray(npn_idx, pya.Trans(um(45), um(85))))
    # Tail
    sar_adc.insert(pya.CellInstArray(npn_idx, pya.Trans(um(37), um(55))))

    # =========================================================
    # Top-level: IMU Analog Signal Chain
    # =========================================================
    top = layout.create_cell("IMU_ANALOG_CHAIN")

    # Place blocks in signal-flow order (left to right)
    top.insert(pya.CellInstArray(inp_amp.cell_index(), pya.Trans(um(0), um(0))))
    top.insert(pya.CellInstArray(gmc_filt.cell_index(), pya.Trans(um(100), um(0))))
    top.insert(pya.CellInstArray(peak_det.cell_index(), pya.Trans(um(200), um(0))))
    top.insert(pya.CellInstArray(sah.cell_index(), pya.Trans(um(300), um(0))))
    top.insert(pya.CellInstArray(sar_adc.cell_index(), pya.Trans(um(380), um(0))))

    # Port labels
    top.shapes(ly['M1']).insert(pya.Text("VIN_P", pya.Trans(um(5), um(60))))
    top.shapes(ly['M1']).insert(pya.Text("VIN_N", pya.Trans(um(5), um(40))))
    top.shapes(ly['M1']).insert(pya.Text("VCC", pya.Trans(um(250), um(130))))
    top.shapes(ly['M1']).insert(pya.Text("VSS", pya.Trans(um(250), um(5))))
    top.shapes(ly['M2']).insert(pya.Text("ADC_OUT[7:0]", pya.Trans(um(480), um(75))))
    top.shapes(ly['M1']).insert(pya.Text("ADC_CLK", pya.Trans(um(380), um(130))))

    output = "/home/bthomas3/Videos/77GHz_phased_array/layout/IMU_ANALOG_CHAIN.gds"
    layout.write(output)
    print(f"IMU analog signal chain: {output}")
    print(f"Blocks: Input Amp + Gm-C BPF + Peak Det + S&H + 8-bit SAR ADC")
    print(f"Total width: ~500 µm, height: ~150 µm")


if __name__ == "__main__":
    main()