# 77 GHz Phased Array Vibrometer — Tapeout Package
## IHP SG13G2 130nm SiGe BiCMOS

### Die Summary
| Parameter | Value |
|-----------|-------|
| Die Size | 2000 × 2000 µm |
| Process | IHP SG13G2 (130nm SiGe BiCMOS) |
| Top Cell | PHASED_ARRAY_77G_TOP |
| GDS File | PHASED_ARRAY_77G_TOP.gds |
| Metal Stack | M1-M5 + TM1 + TM2 (7 metal) |
| Bond Pads | 40 total (70×70µm TM2) |
| DRC | CLEAN (0 violations) |
| LVS | PASS (comparison mode) |

### Block Summary
| Block | Function | Size (µm) | Position | Transistors |
|-------|----------|-----------|----------|-------------|
| VCO | Cross-coupled LC oscillator | 250×450 | (900,1125) | 2× npn13G2l m=2, 2× varicap |
| LNA | Differential cascode LNA | 300×500 | (200,1100) | 4× npn13G2l m=4 |
| MIXER | Gilbert cell downconverter | 300×450 | (550,1125) | 8× npn13G2l m=2/4 |
| TXPA | Differential cascode PA | 350×550 | (900,300) | 4× npn13G2l m=8 |
| ILFD | Injection-locked freq divider | 300×600 | (200,300) | 4× npn13G2l m=2 |
| BIAS | PTAT current mirror network | 200×300 | (550,500) | 8× npn13G2l + 6× rppd |

### Pad Map

#### South Edge (left to right)
| Pad# | Name | Type | Function |
|------|------|------|----------|
| S0 | GND | Power | Ground |
| S1 | VCC | Power | Supply |
| S2 | TAIL_BIAS | Analog | Bias reference current input |
| S3 | VCB_BIAS | Analog | Cascode bias voltage input |
| S4 | LO_TUNE | Analog | VCO frequency tuning (current) |
| S5 | VCC | Power | Supply |
| S6 | GND | Power | Ground |
| S7 | INJ_P | Test | Injection test point P |
| S8 | INJ_N | Test | Injection test point N |
| S9 | GND | Power | Ground |

#### West Edge (bottom to top)
| Pad# | Name | Type | Function |
|------|------|------|----------|
| W0 | GND | Power | Ground |
| W1 | ANT_RX_P | RF I/O | RX antenna input + |
| W2 | ANT_RX_N | RF I/O | RX antenna input − |
| W3 | GND | Power | Ground |
| W4 | LNA_VCC | Power | LNA supply |
| W5 | GND | Power | Ground |
| W6 | RF_MON_P | Test | RF monitor output + |
| W7 | RF_MON_N | Test | RF monitor output − |
| W8 | GND | Power | Ground |
| W9 | GND | Power | Ground |

#### North Edge (left to right)
| Pad# | Name | Type | Function |
|------|------|------|----------|
| N0 | GND | Power | Ground |
| N1 | DIV_P | Output | Divider output + |
| N2 | DIV_N | Output | Divider output − |
| N3 | GND | Power | Ground |
| N4 | VCC | Power | Supply |
| N5 | GND | Power | Ground |
| N6 | IF_P | Output | IF output + |
| N7 | IF_N | Output | IF output − |
| N8 | GND | Power | Ground |
| N9 | GND | Power | Ground |

#### East Edge (bottom to top)
| Pad# | Name | Type | Function |
|------|------|------|----------|
| E0 | GND | Power | Ground |
| E1 | ANT_TX_P | RF I/O | TX antenna output + |
| E2 | ANT_TX_N | RF I/O | TX antenna output − |
| E3 | GND | Power | Ground |
| E4 | PA_VCC | Power | PA supply |
| E5 | GND | Power | Ground |
| E6 | VCO_VCC | Power | VCO supply |
| E7 | GND | Power | Ground |
| E8 | VTUNE | Analog | VCO varactor tuning voltage |
| E9 | GND | Power | Ground |

### Power Supply Requirements
| Supply | Typical Voltage | Pads |
|--------|----------------|------|
| VCC | 3.3V | S1, S5, N4, W4 (LNA), E4 (PA), E6 (VCO) |
| GND | 0V | All GND pads (TM1 ground mesh) |
| VTUNE | 0–3.3V | E8 (varactor tuning) |
| TAIL_BIAS | ~0.8V | S2 (sets reference current) |
| VCB_BIAS | ~1.6V | S3 (cascode gate bias) |

### ESD Protection
- Diode-connected npn13G2l (m=2) on all 16 signal pads
- Clamp: pad-to-ground (C=B=PAD, E=GND)
- Cell size: 30×30µm, placed inboard of pad ring

### Design Notes
1. All inter-block RF signal routing uses CPW transmission lines on TM2 within blocks, transitioning to M5/M4 stripline for inter-block connections
2. TM1 serves as ground plane/shield for all CPW structures
3. Differential signals use over-under routing: OUTP on M5, OUTN on M4
4. Bias distribution uses M3 (above y=900) and M4 (below y=900) to avoid signal crossings
5. Metal fill on M1-M5 for density compliance (2-3µm squares, 10-15µm pitch)

### Test Plan
1. DC bias: Apply VCC=3.3V, TAIL_BIAS=0.8V (via 4kΩ ext resistor), VCB_BIAS=1.6V
2. VCO tuning: Sweep VTUNE 0–3.3V, measure DIV_P/N frequency (should be ~38.5GHz = f_osc/2)
3. TX output: Measure ANT_TX_P/N power at 77GHz
4. RX chain: Apply 77GHz signal at ANT_RX_P/N, measure IF_P/N
5. LO leakage: Check isolation between TX and RX paths
