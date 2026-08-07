v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {RX Channel — LNA+Mixer+IFA+VGA+ADC+DIGIF} 0 -650 0 0 0.5 0.5 {}
C {LNA_77G.sym} 150 -500 0 0 {name=x_lna}
C {MIXER_77G.sym} 350 -500 0 0 {name=x_mixer}
C {IFA_77G.sym} 550 -500 0 0 {name=x_ifa}
C {VGA_77G.sym} 750 -500 0 0 {name=x_vga}
C {ADC_SAR_12B.sym} 950 -500 0 0 {name=x_adc}
C {DIGIF_CML.sym} 1150 -500 0 0 {name=x_digif}
C {iopin.sym} 50 -500 0 1 {name=p1 lab=ANT_RXP}
C {iopin.sym} 50 -470 0 1 {name=p2 lab=ANT_RXN}
C {iopin.sym} 1300 -500 0 0 {name=p3 lab=DOUT_P}
C {iopin.sym} 1300 -470 0 0 {name=p4 lab=DOUT_N}
C {iopin.sym} 350 -600 0 0 {name=p5 lab=LO_P}
C {iopin.sym} 350 -570 0 0 {name=p6 lab=LO_N}
C {iopin.sym} 750 -600 0 0 {name=p7 lab=VCTRL}
C {iopin.sym} 950 -600 0 0 {name=p8 lab=CLK_ADC}
C {iopin.sym} 600 -650 0 0 {name=p9 lab=VCC}
C {iopin.sym} 600 -350 0 0 {name=p10 lab=GND}
C {iopin.sym} 650 -350 0 0 {name=p11 lab=sub!}
C {iopin.sym} 950 -650 0 0 {name=p12 lab=VDD}
C {lab_pin.sym} 150 -530 3 0 {name=l1 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 150 -470 1 0 {name=l2 sig_type=std_logic lab=GND}
C {lab_pin.sym} 150 -500 0 0 {name=l3 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 130 -510 0 0 {name=l4 sig_type=std_logic lab=ANT_RXP}
C {lab_pin.sym} 130 -490 0 0 {name=l5 sig_type=std_logic lab=ANT_RXN}
C {lab_pin.sym} 170 -510 2 0 {name=l6 sig_type=std_logic lab=lna_op}
C {lab_pin.sym} 170 -490 2 0 {name=l7 sig_type=std_logic lab=lna_on}
C {lab_pin.sym} 350 -530 3 0 {name=l8 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 350 -470 1 0 {name=l9 sig_type=std_logic lab=GND}
C {lab_pin.sym} 350 -500 0 0 {name=l10 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 330 -520 0 0 {name=l11 sig_type=std_logic lab=lna_op}
C {lab_pin.sym} 330 -490 0 0 {name=l12 sig_type=std_logic lab=lna_on}
C {lab_pin.sym} 330 -540 0 0 {name=l13 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 330 -460 0 0 {name=l14 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 370 -510 2 0 {name=l15 sig_type=std_logic lab=if_p}
C {lab_pin.sym} 370 -490 2 0 {name=l16 sig_type=std_logic lab=if_n}
C {lab_pin.sym} 550 -530 3 0 {name=l17 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 550 -470 1 0 {name=l18 sig_type=std_logic lab=GND}
C {lab_pin.sym} 550 -500 0 0 {name=l19 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 530 -510 0 0 {name=l20 sig_type=std_logic lab=if_p}
C {lab_pin.sym} 530 -490 0 0 {name=l21 sig_type=std_logic lab=if_n}
C {lab_pin.sym} 570 -510 2 0 {name=l22 sig_type=std_logic lab=ifa_op}
C {lab_pin.sym} 570 -490 2 0 {name=l23 sig_type=std_logic lab=ifa_on}
C {lab_pin.sym} 750 -530 3 0 {name=l24 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 750 -470 1 0 {name=l25 sig_type=std_logic lab=GND}
C {lab_pin.sym} 750 -500 0 0 {name=l26 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 730 -510 0 0 {name=l27 sig_type=std_logic lab=ifa_op}
C {lab_pin.sym} 730 -490 0 0 {name=l28 sig_type=std_logic lab=ifa_on}
C {lab_pin.sym} 730 -540 0 0 {name=l29 sig_type=std_logic lab=VCTRL}
C {lab_pin.sym} 770 -510 2 0 {name=l30 sig_type=std_logic lab=vga_op}
C {lab_pin.sym} 770 -490 2 0 {name=l31 sig_type=std_logic lab=vga_on}
C {lab_pin.sym} 950 -530 3 0 {name=l32 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 950 -470 1 0 {name=l33 sig_type=std_logic lab=GND}
C {lab_pin.sym} 950 -500 0 0 {name=l34 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 930 -510 0 0 {name=l35 sig_type=std_logic lab=vga_op}
C {lab_pin.sym} 930 -490 0 0 {name=l36 sig_type=std_logic lab=vga_on}
C {lab_pin.sym} 930 -540 0 0 {name=l37 sig_type=std_logic lab=CLK_ADC}
C {lab_pin.sym} 970 -510 2 0 {name=l38 sig_type=std_logic lab=adc_op}
C {lab_pin.sym} 970 -490 2 0 {name=l39 sig_type=std_logic lab=adc_on}
C {lab_pin.sym} 1150 -530 3 0 {name=l40 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 1150 -470 1 0 {name=l41 sig_type=std_logic lab=GND}
C {lab_pin.sym} 1150 -500 0 0 {name=l42 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 1130 -510 0 0 {name=l43 sig_type=std_logic lab=adc_op}
C {lab_pin.sym} 1130 -490 0 0 {name=l44 sig_type=std_logic lab=adc_on}
C {lab_pin.sym} 1170 -510 2 0 {name=l45 sig_type=std_logic lab=DOUT_P}
C {lab_pin.sym} 1170 -490 2 0 {name=l46 sig_type=std_logic lab=DOUT_N}
