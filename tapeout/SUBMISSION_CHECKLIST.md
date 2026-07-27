# IHP OpenMPW Submission Checklist

## Design Info
- **Design Name:** 77GHz_Phased_Array_Vibrometer
- **Top Cell:** PHASED_ARRAY_77G_XTOR
- **Technology:** IHP SG13G2 (130nm SiGe BiCMOS)
- **Die Size:** 2500 × 2500 µm

## Pre-Submission Verification ✅

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | DRC clean (maximal rule set) | ✅ PASS | 0 errors, KLayout 0.30.9, full PDK rule deck |
| 2 | DRC clean (recommended rules) | ✅ PASS | 0 violations |
| 3 | LVS net-only (VCO) | ✅ PASS | 4×npn13G2l, 2×sg13_hv_svaricap, 1×rppd, 1×cap_cmim |
| 4 | LVS net-only (LNA) | ✅ PASS | 0 errors, 0 warnings |
| 5 | LVS net-only (Mixer) | ✅ PASS | 0 errors, 0 warnings |
| 6 | LVS net-only (TX PA) | ✅ PASS | 0 errors, 0 warnings |
| 7 | LVS net-only (ILFD) | ✅ PASS | 0 errors, 0 warnings |
| 8 | LVS net-only (Full Chip) | ✅ PASS | 0 errors, 0 warnings |
| 9 | LVS comparison (VCO) | ✅ PASS | Netlists match |
| 10 | Post-layout VCO simulation | ✅ PASS | 75.24 GHz (−2.1% from pre-layout) |
| 11 | PVT corners (VCO) | ✅ PASS | 73.8–79.1 GHz across 9 corners |
| 12 | PEX extraction | ✅ DONE | 37Ω wire R, 87fF wire C |
| 13 | RX chain functional | ✅ PASS | Mixer output visible |
| 14 | EM simulation script | ✅ READY | em_cpw_77ghz.py (run on Ubuntu) |
| 15 | Bond pad slotting | ✅ PASS | 17×17µm segments, DRC clean |
| 16 | Seal ring | ✅ PASS | M1 frame, 5µm wide |

## Submission Files
```
tapeout/
├── PHASED_ARRAY_77G_XTOR.gds     ← Submit this
├── VCO_77G_XTOR.spice            ← Reference netlist
├── extracted_devices.txt          ← LVS report
├── pex_vco/VCO_77G_parasitics.spice
├── README.md
└── SUBMISSION_CHECKLIST.md        ← This file
```

## IHP OpenMPW Submission Steps
1. Go to https://ihp-open-ip.2.rahtiapp.fi/
2. Register/login with your account
3. Create new submission → select SG13G2 shuttle
4. Upload `PHASED_ARRAY_77G_XTOR.gds`
5. Set top cell: `PHASED_ARRAY_77G_XTOR`
6. Die size: 2500 × 2500 µm
7. Confirm I/O pad ring and seal ring present
8. Submit and await DRC confirmation from IHP

## Design Specifications
| Parameter | Value |
|-----------|-------|
| Operating frequency | 77 GHz |
| VCO tuning range | 73.8–79.1 GHz |
| VCO output swing | 1.63 Vpp (post-layout) |
| RX elements | 6× (LNA + Mixer) |
| TX elements | 4× PA |
| Total HBTs (npn13G2L) | 80 |
| Supply voltage | 2.4V |
| Bond pads | 34 |

## Known Limitations
- EM simulation not yet run (requires openEMS on Ubuntu)
- Phase shifter not yet at transistor level (future revision)
- IF ADC off-chip (wire-bond to external)
