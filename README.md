# 77 GHz Phased Array Vibrometer - RF Front-End

## Overview

Modified RF building blocks from mWATTBAT (150 GHz radar, IHP SG13G2) retuned
for 77 GHz operation in a 4×4 phased array laser-Doppler vibrometer for
autonomous drone-based landmine detection.

## Design Methodology

All transmission line lengths scaled by factor 150/77 ≈ 1.95× from original.
Coupling capacitors enlarged for lower reactance at 77 GHz.
Transistor sizing and bias networks kept identical (DC operating point unchanged).

## Modified Blocks

| Block | File | Key Changes |
|-------|------|-------------|
| LNA (RX amp) | `RXAMP_77GD.sch` | Input TL: 50→97µm, Load TL: 77.5→151µm, Coupling caps: 4→6µm, 2.7→4µm |
| Mixer | `MIXER_77GD.sch` | LO TL: 25→49µm, 34→66µm, RF TL: 64→125µm, Coupling caps: 3→5µm, 2.3→4µm |
| Wilkinson | `WILKINSON_77GD.sch` | λ/4 TL: 302.5→590µm |
| LNA Testbench | `RXAMP_77GD_TB.sch` | AC sweep 50-110 GHz, TRAN at 77 GHz, Noise 50-110 GHz |

## Transmission Line Scaling Summary

| TL Function | Original len (150G) | Scaled len (77G) | Z0 |
|-------------|--------------------:|------------------:|---:|
| RX input match | 50 µm | 97 µm | 85Ω |
| RX load/resonator | 77.5 µm | 151 µm | 85Ω |
| RX emitter degen | 30 µm | 58 µm | 85Ω |
| Mixer LO short | 25 µm | 49 µm | 85Ω |
| Mixer LO long | 34 µm | 66 µm | 85Ω |
| Mixer RF | 64 µm | 125 µm | 85Ω |
| Wilkinson λ/4 | 302.5 µm | 590 µm | 60Ω |

## Simulation Setup

Simulator: Xyce (primary) or ngspice
PDK: IHP SG13G2 (set $PDK_ROOT and $PDK environment variables)
Models: cornerHBT, cornerCAP, cornerRES (typical corners)

### Running Simulations

1. Install IIC-OSIC-TOOLS Docker image (includes xschem + ngspice + Xyce + SG13G2 PDK)
2. Open testbench in xschem: `xschem RXAMP_77GD_TB.sch`
3. Netlist and simulate (Xyce launcher button in schematic)
4. Load waveforms and verify:
   - S21 gain peak at 77 GHz (target: >12 dB)
   - S11 < -10 dB at 77 GHz
   - NF < 6 dB at 77 GHz
   - Supply current (ICC) within expected range

### Expected Performance (77 GHz vs 150 GHz)

| Parameter | mWATTBAT @150G | Expected @77G | Reason |
|-----------|:--------------:|:-------------:|--------|
| LNA Gain | 8-12 dB | 12-18 dB | Further from fmax → more available gain |
| LNA NF | 8-12 dB | 4-6 dB | Lower freq → less transit time noise |
| Mixer CG | 0-5 dB | 5-10 dB | Better switching at lower freq |
| PA Psat | -5 to 0 dBm | 3-8 dBm | More efficient at 77G |

## Blocks Still To Design

1. **VCO_77G** - Cross-coupled SiGe HBT with TL resonator (~590µm stub)
2. **PLL_77G** - Charge-pump PLL locking VCO to reference, low phase noise
3. **PHASE_SHIFTER_77G** - 4-bit switched transmission line (per element)
4. **LO_DIST_16** - 4-stage Wilkinson tree (1→16 distribution)
5. **TXAMP_77GD** - PA retuned from TXAMP_150GD (same methodology as LNA)
6. **SPI_CTRL** - Digital beam controller (RTL, synthesized in SKY130 or on-chip)

## Directory Structure

```
77GHz_phased_array/
└── xschem/
    ├── RXAMP_77GD.sch          # LNA schematic (modified)
    ├── RXAMP_77GD_TB.sch       # LNA testbench
    ├── MIXER_77GD.sch          # Mixer schematic (modified)
    ├── WILKINSON_77GD.sch      # Power divider (modified)
    └── (future: VCO, PLL, phase shifter, PA, top-level)
```

## References

- mWATTBAT: https://github.com/EngGhaith/mWATTBAT_RADAR_150GHz_TO_July2025
- IHP SG13G2 PDK: https://github.com/IHP-GmbH/IHP-Open-PDK
- IIC-OSIC-TOOLS: https://github.com/iic-jku/IIC-OSIC-TOOLS
- npn13G2l fT: ~350 GHz, fmax: ~450 GHz (77 GHz is 17% of fmax)

## License

Apache 2.0 (same as mWATTBAT source)
