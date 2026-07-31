# 77 GHz Phased Array Vibrometer

## Overview

A 77 GHz FMCW phased array vibrometer for autonomous drone-based landmine detection, implemented on **IHP SG13G2 130nm SiGe BiCMOS**. The system detects buried landmines by measuring acoustic-seismic surface vibrations induced by an airborne speaker, using Doppler processing across multiple radar beams.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FULL CHIP (2.5×2.5 mm)                    │
├──────────────────┬──────────────────┬───────────────────────┤
│   RF Front-End   │   IMU Analog     │    Digital DSP        │
│                  │                  │                       │
│  • VCO (77 GHz)  │  • Input Amp     │  • 64-pt Range FFT   │
│  • LNA           │  • Gm-C BPF      │  • 128-pt Doppler FFT│
│  • Mixer         │  • Peak Detector  │  • 4-beam Beamformer │
│  • TX PA         │  • S&H            │  • Motion Comp       │
│  • ILFD (/2)     │  • 8-bit SAR ADC  │  • SPI Output        │
│  • Phase Shifter │                  │  • SRAM (1024×32)    │
└──────────────────┴──────────────────┴───────────────────────┘
```

## Status

| Subsystem | Design | Layout | LVS | P&R |
|-----------|--------|--------|-----|-----|
| VCO 77 GHz | ✅ | ✅ GDS | ✅ | — |
| LNA 77 GHz | ✅ | ✅ GDS | ✅ | — |
| Mixer 77 GHz | ✅ | ✅ GDS | ✅ | — |
| TX PA 77 GHz | ✅ | ✅ GDS | ✅ | — |
| ILFD 77 GHz | ✅ | ✅ GDS | ✅ | — |
| IFA (IF Amp) | ✅ | ✅ GDS | ✅ | — |
| IMU Analog Chain | ✅ | ✅ GDS | — | — |
| Digital DSP (slow-time FFT) | ✅ | — | — | ✅ Routed |
| Digital DSP (full vibrometer) | ✅ | — | — | Placed |
| Full Chip Assembly | ✅ | ✅ GDS | — | — |

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Frequency | 77 GHz |
| Modulation | FMCW |
| Process | IHP SG13G2 130nm SiGe BiCMOS |
| Die size | 2.5 × 2.5 mm |
| Digital clock | 200 MHz |
| Digital area | 1.87 mm² (placed), 0.079 mm² (FFT routed) |
| SRAM | IHP RM_IHPSG13_1P_1024x32_c2_bm_bist |
| Beams | 4 (expandable to 16) |
| FFT size | 64-pt range, 128-pt Doppler |
| ADC channels | 6 |

## Directory Structure

```
77GHz_phased_array/
├── rtl/                        # Digital RTL (SystemVerilog)
│   ├── vibrometer_top.v        # Top-level (FFT + slow-time + SPI)
│   ├── vibrometer_mocomp_top.v # Full system with motion compensation
│   ├── radar_mac_accel.v       # 4-MAC engine (range FFT + beamformer)
│   ├── slowtime_fft.v          # 128-pt Doppler FFT
│   ├── sram_if.v               # IHP SRAM macro wrapper
│   ├── spi_serializer.v        # 38-bit SPI output
│   ├── deconv_kernel_estimator_top_level.v  # Motion comp (nhpoole)
│   ├── iir_notch_filter.v      # IIR H(f) evaluator
│   ├── cordic_*.v              # CORDIC converters
│   ├── fixed_pt_div.v          # 32-bit divider
│   └── serializer.v / deserializer.v
├── layout/                     # Analog layout generators + GDS
│   ├── generate_vco_transistor.py
│   ├── generate_full_chip_mocomp.py
│   ├── VCO_77G_XTOR.gds
│   ├── LNA_77G_XTOR.gds
│   ├── MIXER_77G_XTOR.gds
│   ├── TXPA_77G_XTOR.gds
│   ├── ILFD_77G_XTOR.gds
│   ├── IFA_77G_XTOR.gds
│   ├── IMU_ANALOG_CHAIN.gds
│   ├── PHASED_ARRAY_77G_XTOR.gds  # Full RF front-end
│   └── VIBROMETER_FULL_CHIP.gds   # Full chip assembly
├── analog_mocomp/              # IMU analog signal chain
│   └── imu_signal_chain.py     # KLayout generator (IHP BJT-based)
├── digital_pnr/                # Digital place & route
│   ├── synth_core.ys           # Yosys synthesis (full vibrometer)
│   ├── synth_small.ys          # Yosys synthesis (slow-time FFT)
│   ├── pnr.tcl                 # OpenROAD P&R (full)
│   ├── pnr_small.tcl           # OpenROAD P&R (FFT, fully routed)
│   ├── route_only.tcl          # Routing-only script
│   ├── constraints.sdc         # 200 MHz clock
│   ├── power.tcl               # Power grid (Metal3/Metal4)
│   └── build/
│       ├── slowtime_fft_routed.def   # ✅ Fully routed DEF
│       ├── slowtime_fft_synth.v      # Synthesized netlist (FFT)
│       ├── vibrometer_top.def        # Placed DEF (full design)
│       └── vibrometer_top_synth.v    # Synthesized netlist (full)
├── sim/                        # SPICE simulations
├── xschem/                     # Schematics (xschem)
├── tapeout/                    # Tapeout files
└── docs/                       # Documentation
```

## RF Front-End

Modified from mWATTBAT (150 GHz radar) with transmission lines scaled by 150/77 ≈ 1.95×.

| Block | Topology | Key Feature |
|-------|----------|-------------|
| VCO | Cross-coupled npn13G2L | TL resonator, VTUNE varactor |
| LNA | Cascode CE | 12-18 dB gain, NF < 6 dB |
| Mixer | Gilbert cell | 5-10 dB conversion gain |
| TX PA | CE push-pull | 3-8 dBm Psat |
| ILFD | Injection-locked /2 | Low-power frequency divider |
| IFA | Cascode | IF amplification stage |

## Digital DSP

The radar signal processor implements:
1. **Range FFT** — 64-pt radix-2 DIT across 6 ADC channels (4-MAC engine)
2. **Beamforming** — 4-beam steering via complex weight multiply-accumulate
3. **Peak detection** — Per-beam range bin extraction
4. **Slow-time FFT** — 128-pt Doppler FFT across chirps (vibration spectrum)
5. **Motion compensation** — IIR notch filter deconvolution (nhpoole)
6. **SPI output** — 38-bit serialized frame (amplitude + beam index)

## Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| Yosys | 0.35 | RTL synthesis to IHP sg13g2_stdcell |
| OpenROAD | 26Q3 | Place & route |
| KLayout | 0.30.9 | Layout generation, DRC, GDS viewing |
| slang | — | SystemVerilog linting |
| ngspice/Xyce | — | SPICE simulation |
| xschem | — | Schematic capture |

## Building

### Synthesis
```bash
cd digital_pnr
yosys -s synth_small.ys    # Slow-time FFT only
yosys -s synth_core.ys     # Full vibrometer
```

### Place & Route
```bash
openroad -exit pnr_small.tcl   # FFT (fully routes in ~30 min)
openroad -exit pnr.tcl         # Full vibrometer (placement only on small machines)
```

### Layout Generation
```bash
klayout -b -r analog_mocomp/imu_signal_chain.py
klayout -b -r layout/generate_full_chip_mocomp.py
```

## References

- mWATTBAT: https://github.com/EngGhaith/mWATTBAT_RADAR_150GHz_TO_July2025
- nhpoole motion comp: https://github.com/nhpoole/mixed_signal_mmwave_edge_accelerator
- IHP SG13G2 PDK: https://github.com/IHP-GmbH/IHP-Open-PDK
- IIC-OSIC-TOOLS: https://github.com/iic-jku/IIC-OSIC-TOOLS
- npn13G2L: fT ~350 GHz, fmax ~450 GHz

## License

Apache 2.0
