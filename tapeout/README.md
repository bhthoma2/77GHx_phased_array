# 77 GHz Phased Array Vibrometer — IHP OpenMPW Tapeout

## Design Summary
- **Technology:** IHP SG13G2 (130nm SiGe BiCMOS)
- **Application:** 77 GHz phased array vibrometer for drone-based landmine detection
- **Die Size:** 2.5 × 2.5 mm
- **Top Cell:** PHASED_ARRAY_77G_XTOR

## Block List
| Block | Instances | Devices | Function |
|-------|-----------|---------|----------|
| VCO_77G_XTOR | 1 | 4×npn13G2L + 2×SVaricap + 1×rppd + 1×cmim | 76.9 GHz oscillator |
| LNA_77G_XTOR | 6 | 16×npn13G2L + 2×cmim + 1×rppd | Low-noise amplifier |
| MIXER_77G_XTOR | 6 | 16×npn13G2L + 3×rppd | Gilbert-cell mixer |
| TXPA_77G_XTOR | 4 | 32×npn13G2L + 1×rppd | TX power amplifier |
| ILFD_77G_XTOR | 1 | 8×npn13G2L + 1×rppd | ÷2 frequency divider |

## Verification Status
| Check | Result |
|-------|--------|
| DRC (full chip) | ✅ 0 errors |
| LVS (VCO) | ✅ Device count match |
| PEX (VCO) | ✅ Extracted (37Ω wire R, 87fF wire C) |
| Simulation (pre-layout) | ✅ All blocks functional |
| PVT Corners (VCO) | ✅ 73.8–79.1 GHz across 9 corners |

## Files
- `PHASED_ARRAY_77G_XTOR.gds` — Final tapeout GDS
- `VCO_77G_XTOR.spice` — VCO schematic netlist
- `pex_vco/VCO_77G_parasitics.spice` — Extracted parasitics

## Bond Pad Assignment (34 pads)
- Bottom (9): VCC, GND, VTUNE, IF_P, IF_N, CLK_REF, GND, VCC, GND
- Top (9): ANT1-4, TX1-4, GND
- Left (8): RX_IF1-6, VCC, GND
- Right (8): TX_OUT1-4, LO_OUT, PLL_LOCK, VCC, GND
