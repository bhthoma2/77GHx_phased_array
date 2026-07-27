v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {77 GHz FMCW Phased Array Radar - Top Level} 100 -1200 0 0 0.7 0.7 {}
T {IHP SG13G2 130nm SiGe BiCMOS - Landmine Detection} 100 -1150 0 0 0.4 0.4 {layer=7}
T {10 Blocks: VCO, LNA, Mixer, TXPA, ILFD, IFA, VGA, ADC, BIAS, DIGIF} 100 -1110 0 0 0.3 0.3 {layer=7}
T {Total PDC ~ 831mW, VCC_33=3.3V (HBT) / VDD_12=1.2V (CMOS)} 100 -1080 0 0 0.3 0.3 {layer=7}
T {=== RX CHAIN ===} 100 -950 0 0 0.4 0.4 {layer=4}
T {14.9dB NF @ 77GHz, 2-stage TL-matched} 165 -760 0 0 0.2 0.2 {layer=7}
T {25.7dB CG, Gilbert Cell} 415 -760 0 0 0.2 0.2 {layer=7}
T {40dB, 10MHz BW, 2-stage diff pair} 665 -760 0 0 0.2 0.2 {layer=7}
T {0-31dB range, Variable-gm} 915 -760 0 0 0.2 0.2 {layer=7}
T {12-bit SAR, StrongARM+CDAC} 1165 -760 0 0 0.2 0.2 {layer=7}
T {CML Buffer, 50ohm, 819mV} 1415 -760 0 0 0.2 0.2 {layer=7}
T {=== TX/LO CHAIN ===} 100 -640 0 0 0.4 0.4 {layer=4}
T {76.1GHz X-coupled LC VCO} 165 -510 0 0 0.2 0.2 {layer=7}
T {~0dBm diff, TL-matched Nx=8} 415 -510 0 0 0.2 0.2 {layer=7}
T {div-by-2, 38.5GHz out} 665 -510 0 0 0.2 0.2 {layer=7}
T {=== SUPPORT ===} 100 -390 0 0 0.4 0.4 {layer=4}
T {1.177V BGR, 8.6ppm/C} 165 -260 0 0 0.2 0.2 {layer=7}
C {/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks/LNA_77G.sym} 200 -800 0 0 {name=x_lna}
C {/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks/MIXER_77G.sym} 450 -800 0 0 {name=x_mixer}
C {/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks/IFA_77G.sym} 700 -800 0 0 {name=x_ifa}
C {/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks/VGA_77G.sym} 950 -800 0 0 {name=x_vga}
C {/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks/ADC_SAR_12B.sym} 1200 -800 0 0 {name=x_adc}
C {/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks/DIGIF_CML.sym} 1450 -800 0 0 {name=x_digif}
C {/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks/VCO_77G.sym} 200 -550 0 0 {name=x_vco}
C {/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks/TXPA_77G.sym} 450 -550 0 0 {name=x_txpa}
C {/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks/ILFD_77G.sym} 700 -550 0 0 {name=x_ilfd}
C {/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks/BIAS_BGR.sym} 200 -300 0 0 {name=x_bias}
C {iopin.sym} 50 -810 0 1 {name=p_antrxp lab=ANT_RXP}
C {iopin.sym} 50 -790 0 1 {name=p_antrxn lab=ANT_RXN}
C {iopin.sym} 1600 -810 0 0 {name=p_doutp lab=DOUT_P}
C {iopin.sym} 1600 -790 0 0 {name=p_doutn lab=DOUT_N}
C {iopin.sym} 50 -550 0 1 {name=p_vtune lab=VTUNE}
C {iopin.sym} 600 -560 0 0 {name=p_anttxp lab=ANT_TXP}
C {iopin.sym} 600 -540 0 0 {name=p_anttxn lab=ANT_TXN}
C {iopin.sym} 800 -785 0 1 {name=p_vctrl lab=VCTRL}
C {iopin.sym} 1050 -785 0 1 {name=p_clk lab=CLK_ADC}
C {iopin.sym} 50 -850 0 1 {name=p_vcc33 lab=VCC_33}
C {iopin.sym} 1200 -900 0 1 {name=p_vdd12 lab=VDD_12}
C {iopin.sym} 190 -720 0 0 {name=p_gnd_rx lab=GND}
C {iopin.sym} 190 -480 0 0 {name=p_gnd_tx lab=GND}
C {iopin.sym} 190 -240 0 0 {name=p_gnd_bias lab=GND}
N 50 -810 150 -810 {lab=ANT_RXP}
N 50 -790 150 -790 {lab=ANT_RXN}
N 250 -810 325 -810 {lab=RF_P}
N 325 -810 325 -820 {lab=RF_P}
N 325 -820 400 -820 {lab=RF_P}
N 250 -790 335 -790 {lab=RF_N}
N 335 -790 335 -808 {lab=RF_N}
N 335 -808 400 -808 {lab=RF_N}
N 500 -810 650 -810 {lab=IF_P}
N 500 -790 650 -790 {lab=IF_N}
N 750 -810 825 -810 {lab=IFA_OUTP}
N 825 -810 825 -815 {lab=IFA_OUTP}
N 825 -815 900 -815 {lab=IFA_OUTP}
N 750 -790 825 -790 {lab=IFA_OUTN}
N 825 -790 825 -800 {lab=IFA_OUTN}
N 825 -800 900 -800 {lab=IFA_OUTN}
N 1000 -810 1075 -810 {lab=VGA_OUTP}
N 1075 -810 1075 -815 {lab=VGA_OUTP}
N 1075 -815 1150 -815 {lab=VGA_OUTP}
N 1000 -790 1075 -790 {lab=VGA_OUTN}
N 1075 -790 1075 -800 {lab=VGA_OUTN}
N 1075 -800 1150 -800 {lab=VGA_OUTN}
N 1250 -810 1400 -810 {lab=ADC_DOUTP}
N 1250 -790 1400 -790 {lab=ADC_DOUTN}
N 1500 -810 1600 -810 {lab=DOUT_P}
N 1500 -790 1600 -790 {lab=DOUT_N}
N 50 -550 150 -550 {lab=VTUNE}
N 250 -560 650 -560 {lab=VCO_OUTP}
N 380 -560 380 -792 {lab=VCO_OUTP}
N 380 -792 400 -792 {lab=VCO_OUTP}
N 400 -560 400 -565 {lab=VCO_OUTP}
N 650 -560 650 -550 {lab=VCO_OUTP}
N 250 -540 385 -540 {lab=VCO_OUTN}
N 385 -540 385 -780 {lab=VCO_OUTN}
N 385 -780 400 -780 {lab=VCO_OUTN}
N 385 -550 400 -550 {lab=VCO_OUTN}
N 385 -540 385 -550 {lab=VCO_OUTN}
N 500 -560 600 -560 {lab=ANT_TXP}
N 500 -540 600 -540 {lab=ANT_TXN}
N 800 -785 900 -785 {lab=VCTRL}
N 1050 -785 1150 -785 {lab=CLK_ADC}
N 250 -310 250 -535 {lab=VREF}
N 250 -535 400 -535 {lab=VREF}
N 250 -290 310 -290 {lab=IBIAS_OUT}
N 50 -850 200 -850 {lab=VCC_33}
N 200 -850 1500 -850 {lab=VCC_33}
N 200 -850 200 -840 {lab=VCC_33}
N 450 -850 450 -840 {lab=VCC_33}
N 700 -850 700 -840 {lab=VCC_33}
N 950 -850 950 -840 {lab=VCC_33}
N 1450 -850 1450 -840 {lab=VCC_33}
N 150 -600 750 -600 {lab=VCC_33}
N 200 -600 200 -590 {lab=VCC_33}
N 450 -600 450 -590 {lab=VCC_33}
N 700 -600 700 -590 {lab=VCC_33}
N 1200 -900 1200 -840 {lab=VDD_12}
N 200 -350 200 -340 {lab=VDD_12}
N 190 -760 190 -720 {lab=GND}
N 440 -760 440 -720 {lab=GND}
N 690 -760 690 -720 {lab=GND}
N 940 -760 940 -720 {lab=GND}
N 1190 -760 1190 -720 {lab=GND}
N 1440 -760 1440 -720 {lab=GND}
N 190 -510 190 -480 {lab=GND}
N 440 -510 440 -480 {lab=GND}
N 690 -510 690 -480 {lab=GND}
N 190 -260 190 -240 {lab=GND}
