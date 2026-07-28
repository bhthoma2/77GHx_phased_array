v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {77 GHz Phased Array Radar — LVS Top Level} 50 -1200 0 0 0.6 0.6 {}
T {IHP SG13G2 130nm SiGe BiCMOS — Landmine Detection Vibrometer} 50 -1150 0 0 0.3 0.3 {layer=7}
T {All sub-blocks use physical PDK cells only (LVS-equivalent)} 50 -1120 0 0 0.3 0.3 {layer=7}
T {Die: 2.5×2.5mm, 6 RX elements, 4 TX elements, 1 VCO, 1 ILFD} 50 -1090 0 0 0.3 0.3 {layer=7}
T {=== RX CHAIN (×6) ===} 100 -1000 0 0 0.4 0.4 {layer=4}
C {VCO_77G_LVS.sym} 200 -600 0 0 {name=x_vco}
C {LNA_77G_LVS.sym} 200 -850 0 0 {name=x_lna0}
C {MIXER_77G_LVS.sym} 500 -850 0 0 {name=x_mixer0}
C {TXPA_77G_LVS.sym} 500 -600 0 0 {name=x_txpa0}
C {iopin.sym} 50 -870 0 1 {name=p1 lab=ANT_RXP}
C {iopin.sym} 50 -830 0 1 {name=p2 lab=ANT_RXN}
C {iopin.sym} 700 -870 0 0 {name=p3 lab=IFP}
C {iopin.sym} 700 -830 0 0 {name=p4 lab=IFN}
C {iopin.sym} 50 -620 0 1 {name=p5 lab=VTUNE}
C {iopin.sym} 700 -620 0 0 {name=p6 lab=ANT_TXP}
C {iopin.sym} 700 -580 0 0 {name=p7 lab=ANT_TXN}
C {iopin.sym} 50 -950 0 1 {name=p8 lab=2V4}
C {iopin.sym} 50 -100 0 1 {name=p9 lab=GND}
N 50 -870 150 -870 {lab=ANT_RXP}
N 50 -830 150 -830 {lab=ANT_RXN}
N 150 -870 150 -860 {lab=ANT_RXP}
N 150 -830 150 -840 {lab=ANT_RXN}
N 250 -870 450 -870 {lab=RF_LNA_P}
N 250 -830 450 -830 {lab=RF_LNA_N}
N 550 -870 700 -870 {lab=IFP}
N 550 -830 700 -830 {lab=IFN}
N 250 -620 450 -620 {lab=LO_P}
N 250 -580 450 -580 {lab=LO_N}
N 450 -620 450 -860 {lab=LO_P}
N 450 -580 445 -840 {lab=LO_N}
N 50 -620 150 -620 {lab=VTUNE}
N 550 -620 700 -620 {lab=ANT_TXP}
N 550 -580 700 -580 {lab=ANT_TXN}
N 50 -950 700 -950 {lab=2V4}
N 200 -950 200 -900 {lab=2V4}
N 500 -950 500 -900 {lab=2V4}
N 200 -650 200 -660 {lab=2V4}
N 500 -650 500 -660 {lab=2V4}
N 50 -100 700 -100 {lab=GND}
N 200 -100 200 -780 {lab=GND}
N 500 -100 500 -780 {lab=GND}
N 200 -100 200 -550 {lab=GND}
N 500 -100 500 -550 {lab=GND}
C {lab_pin.sym} 350 -870 0 0 {name=p10 sig_type=std_logic lab=RF_LNA_P}
C {lab_pin.sym} 350 -830 0 0 {name=p11 sig_type=std_logic lab=RF_LNA_N}
C {lab_pin.sym} 350 -620 0 0 {name=p12 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 350 -580 0 0 {name=p13 sig_type=std_logic lab=LO_N}