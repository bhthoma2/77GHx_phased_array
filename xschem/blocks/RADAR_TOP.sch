v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {77 GHz FMCW 6-Channel Phased Array Radar} 100 -1200 0 0 0.7 0.7 {}
T {IHP SG13G2 130nm SiGe BiCMOS - Landmine Detection} 100 -1150 0 0 0.4 0.4 {layer=7}
T {6x RX (LNA+Mixer+IFA+VGA+ADC+DIGIF) + 6x TX (PS+PA) + VCO + BGR} 100 -1110 0 0 0.3 0.3 {layer=7}
T {=== 6-CHANNEL RX ARRAY ===} 100 -1050 0 0 0.4 0.4 {layer=4}
T {=== 6-CHANNEL TX ARRAY ===} 800 -1050 0 0 0.4 0.4 {layer=4}
T {=== TX/LO ===} 100 -380 0 0 0.4 0.4 {layer=4}
T {=== BIAS ===} 100 -180 0 0 0.4 0.4 {layer=4}
C {RX_CHANNEL_77G.sym} 400 -950 0 0 {name=x_rx0}
C {RX_CHANNEL_77G.sym} 400 -850 0 0 {name=x_rx1}
C {RX_CHANNEL_77G.sym} 400 -750 0 0 {name=x_rx2}
C {RX_CHANNEL_77G.sym} 400 -650 0 0 {name=x_rx3}
C {RX_CHANNEL_77G.sym} 400 -550 0 0 {name=x_rx4}
C {RX_CHANNEL_77G.sym} 400 -450 0 0 {name=x_rx5}
C {TX_CHANNEL_77G.sym} 1000 -950 0 0 {name=x_tx0}
C {TX_CHANNEL_77G.sym} 1000 -850 0 0 {name=x_tx1}
C {TX_CHANNEL_77G.sym} 1000 -750 0 0 {name=x_tx2}
C {TX_CHANNEL_77G.sym} 1000 -650 0 0 {name=x_tx3}
C {TX_CHANNEL_77G.sym} 1000 -550 0 0 {name=x_tx4}
C {TX_CHANNEL_77G.sym} 1000 -450 0 0 {name=x_tx5}
C {VCO_77G.sym} 200 -300 0 0 {name=x_vco}
C {BIAS_BGR.sym} 200 -100 0 0 {name=x_bias}
C {iopin.sym} 50 -980 0 1 {name=p1 lab=ANT_RX0P}
C {iopin.sym} 50 -940 0 1 {name=p2 lab=ANT_RX0N}
C {iopin.sym} 50 -880 0 1 {name=p3 lab=ANT_RX1P}
C {iopin.sym} 50 -840 0 1 {name=p4 lab=ANT_RX1N}
C {iopin.sym} 50 -780 0 1 {name=p5 lab=ANT_RX2P}
C {iopin.sym} 50 -740 0 1 {name=p6 lab=ANT_RX2N}
C {iopin.sym} 50 -680 0 1 {name=p7 lab=ANT_RX3P}
C {iopin.sym} 50 -640 0 1 {name=p8 lab=ANT_RX3N}
C {iopin.sym} 50 -580 0 1 {name=p9 lab=ANT_RX4P}
C {iopin.sym} 50 -540 0 1 {name=p10 lab=ANT_RX4N}
C {iopin.sym} 50 -480 0 1 {name=p11 lab=ANT_RX5P}
C {iopin.sym} 50 -440 0 1 {name=p12 lab=ANT_RX5N}
C {iopin.sym} 700 -980 0 0 {name=p13 lab=DOUT0_P}
C {iopin.sym} 700 -940 0 0 {name=p14 lab=DOUT0_N}
C {iopin.sym} 700 -880 0 0 {name=p15 lab=DOUT1_P}
C {iopin.sym} 700 -840 0 0 {name=p16 lab=DOUT1_N}
C {iopin.sym} 700 -780 0 0 {name=p17 lab=DOUT2_P}
C {iopin.sym} 700 -740 0 0 {name=p18 lab=DOUT2_N}
C {iopin.sym} 700 -680 0 0 {name=p19 lab=DOUT3_P}
C {iopin.sym} 700 -640 0 0 {name=p20 lab=DOUT3_N}
C {iopin.sym} 700 -580 0 0 {name=p21 lab=DOUT4_P}
C {iopin.sym} 700 -540 0 0 {name=p22 lab=DOUT4_N}
C {iopin.sym} 700 -480 0 0 {name=p23 lab=DOUT5_P}
C {iopin.sym} 700 -440 0 0 {name=p24 lab=DOUT5_N}
C {iopin.sym} 50 -300 0 1 {name=p25 lab=VTUNE}
C {iopin.sym} 1300 -980 0 0 {name=p33 lab=ANT_TX0P}
C {iopin.sym} 1300 -940 0 0 {name=p34 lab=ANT_TX0N}
C {iopin.sym} 1300 -880 0 0 {name=p35 lab=ANT_TX1P}
C {iopin.sym} 1300 -840 0 0 {name=p36 lab=ANT_TX1N}
C {iopin.sym} 1300 -780 0 0 {name=p37 lab=ANT_TX2P}
C {iopin.sym} 1300 -740 0 0 {name=p38 lab=ANT_TX2N}
C {iopin.sym} 1300 -680 0 0 {name=p39 lab=ANT_TX3P}
C {iopin.sym} 1300 -640 0 0 {name=p40 lab=ANT_TX3N}
C {iopin.sym} 1300 -580 0 0 {name=p41 lab=ANT_TX4P}
C {iopin.sym} 1300 -540 0 0 {name=p42 lab=ANT_TX4N}
C {iopin.sym} 1300 -480 0 0 {name=p43 lab=ANT_TX5P}
C {iopin.sym} 1300 -440 0 0 {name=p44 lab=ANT_TX5N}
C {iopin.sym} 800 -1100 0 1 {name=p45 lab=VCTRL_PS0}
C {iopin.sym} 800 -1080 0 1 {name=p46 lab=VCTRL_PS1}
C {iopin.sym} 800 -1060 0 1 {name=p47 lab=VCTRL_PS2}
C {iopin.sym} 800 -1040 0 1 {name=p48 lab=VCTRL_PS3}
C {iopin.sym} 800 -1020 0 1 {name=p49 lab=VCTRL_PS4}
C {iopin.sym} 800 -1000 0 1 {name=p50 lab=VCTRL_PS5}
C {iopin.sym} 50 -1100 0 1 {name=p28 lab=VCC_33}
C {iopin.sym} 50 -1070 0 1 {name=p29 lab=VDD_12}
C {iopin.sym} 50 -1040 0 1 {name=p30 lab=GND}
C {iopin.sym} 700 -1050 0 0 {name=p31 lab=VCTRL}
C {iopin.sym} 700 -1020 0 0 {name=p32 lab=CLK_ADC}
C {lab_pin.sym} 250 -980 0 0 {name=la1 sig_type=std_logic lab=ANT_RX0P}
C {lab_pin.sym} 250 -940 0 0 {name=la2 sig_type=std_logic lab=ANT_RX0N}
C {lab_pin.sym} 250 -880 0 0 {name=la3 sig_type=std_logic lab=ANT_RX1P}
C {lab_pin.sym} 250 -840 0 0 {name=la4 sig_type=std_logic lab=ANT_RX1N}
C {lab_pin.sym} 250 -780 0 0 {name=la5 sig_type=std_logic lab=ANT_RX2P}
C {lab_pin.sym} 250 -740 0 0 {name=la6 sig_type=std_logic lab=ANT_RX2N}
C {lab_pin.sym} 250 -680 0 0 {name=la7 sig_type=std_logic lab=ANT_RX3P}
C {lab_pin.sym} 250 -640 0 0 {name=la8 sig_type=std_logic lab=ANT_RX3N}
C {lab_pin.sym} 250 -580 0 0 {name=la9 sig_type=std_logic lab=ANT_RX4P}
C {lab_pin.sym} 250 -540 0 0 {name=la10 sig_type=std_logic lab=ANT_RX4N}
C {lab_pin.sym} 250 -480 0 0 {name=la11 sig_type=std_logic lab=ANT_RX5P}
C {lab_pin.sym} 250 -440 0 0 {name=la12 sig_type=std_logic lab=ANT_RX5N}
C {lab_pin.sym} 550 -980 2 0 {name=ld1 sig_type=std_logic lab=DOUT0_P}
C {lab_pin.sym} 550 -940 2 0 {name=ld2 sig_type=std_logic lab=DOUT0_N}
C {lab_pin.sym} 550 -880 2 0 {name=ld3 sig_type=std_logic lab=DOUT1_P}
C {lab_pin.sym} 550 -840 2 0 {name=ld4 sig_type=std_logic lab=DOUT1_N}
C {lab_pin.sym} 550 -780 2 0 {name=ld5 sig_type=std_logic lab=DOUT2_P}
C {lab_pin.sym} 550 -740 2 0 {name=ld6 sig_type=std_logic lab=DOUT2_N}
C {lab_pin.sym} 550 -680 2 0 {name=ld7 sig_type=std_logic lab=DOUT3_P}
C {lab_pin.sym} 550 -640 2 0 {name=ld8 sig_type=std_logic lab=DOUT3_N}
C {lab_pin.sym} 550 -580 2 0 {name=ld9 sig_type=std_logic lab=DOUT4_P}
C {lab_pin.sym} 550 -540 2 0 {name=ld10 sig_type=std_logic lab=DOUT4_N}
C {lab_pin.sym} 550 -480 2 0 {name=ld11 sig_type=std_logic lab=DOUT5_P}
C {lab_pin.sym} 550 -440 2 0 {name=ld12 sig_type=std_logic lab=DOUT5_N}
C {lab_pin.sym} 330 -1010 1 0 {name=ll1 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 360 -1010 1 0 {name=ll2 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 330 -910 1 0 {name=ll3 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 360 -910 1 0 {name=ll4 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 330 -810 1 0 {name=ll5 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 360 -810 1 0 {name=ll6 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 330 -710 1 0 {name=ll7 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 360 -710 1 0 {name=ll8 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 330 -610 1 0 {name=ll9 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 360 -610 1 0 {name=ll10 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 330 -510 1 0 {name=ll11 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 360 -510 1 0 {name=ll12 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 400 -1010 1 0 {name=lv1 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 430 -1010 1 0 {name=lv2 sig_type=std_logic lab=VDD_12}
C {lab_pin.sym} 460 -1010 1 0 {name=lv3 sig_type=std_logic lab=VCTRL}
C {lab_pin.sym} 490 -1010 1 0 {name=lv4 sig_type=std_logic lab=CLK_ADC}
C {lab_pin.sym} 400 -910 1 0 {name=lv5 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 430 -910 1 0 {name=lv6 sig_type=std_logic lab=VDD_12}
C {lab_pin.sym} 460 -910 1 0 {name=lv7 sig_type=std_logic lab=VCTRL}
C {lab_pin.sym} 490 -910 1 0 {name=lv8 sig_type=std_logic lab=CLK_ADC}
C {lab_pin.sym} 400 -810 1 0 {name=lv9 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 430 -810 1 0 {name=lv10 sig_type=std_logic lab=VDD_12}
C {lab_pin.sym} 460 -810 1 0 {name=lv11 sig_type=std_logic lab=VCTRL}
C {lab_pin.sym} 490 -810 1 0 {name=lv12 sig_type=std_logic lab=CLK_ADC}
C {lab_pin.sym} 400 -710 1 0 {name=lv13 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 430 -710 1 0 {name=lv14 sig_type=std_logic lab=VDD_12}
C {lab_pin.sym} 460 -710 1 0 {name=lv15 sig_type=std_logic lab=VCTRL}
C {lab_pin.sym} 490 -710 1 0 {name=lv16 sig_type=std_logic lab=CLK_ADC}
C {lab_pin.sym} 400 -610 1 0 {name=lv17 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 430 -610 1 0 {name=lv18 sig_type=std_logic lab=VDD_12}
C {lab_pin.sym} 460 -610 1 0 {name=lv19 sig_type=std_logic lab=VCTRL}
C {lab_pin.sym} 490 -610 1 0 {name=lv20 sig_type=std_logic lab=CLK_ADC}
C {lab_pin.sym} 400 -510 1 0 {name=lv21 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 430 -510 1 0 {name=lv22 sig_type=std_logic lab=VDD_12}
C {lab_pin.sym} 460 -510 1 0 {name=lv23 sig_type=std_logic lab=VCTRL}
C {lab_pin.sym} 490 -510 1 0 {name=lv24 sig_type=std_logic lab=CLK_ADC}
C {lab_pin.sym} 400 -990 3 0 {name=lg1 sig_type=std_logic lab=GND}
C {lab_pin.sym} 430 -990 3 0 {name=ls1 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 400 -890 3 0 {name=lg2 sig_type=std_logic lab=GND}
C {lab_pin.sym} 430 -890 3 0 {name=ls2 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 400 -790 3 0 {name=lg3 sig_type=std_logic lab=GND}
C {lab_pin.sym} 430 -790 3 0 {name=ls3 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 400 -690 3 0 {name=lg4 sig_type=std_logic lab=GND}
C {lab_pin.sym} 430 -690 3 0 {name=ls4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 400 -590 3 0 {name=lg5 sig_type=std_logic lab=GND}
C {lab_pin.sym} 430 -590 3 0 {name=ls5 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 400 -490 3 0 {name=lg6 sig_type=std_logic lab=GND}
C {lab_pin.sym} 430 -490 3 0 {name=ls6 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 200 -330 3 0 {name=lvc1 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 200 -270 1 0 {name=lgv1 sig_type=std_logic lab=GND}
C {lab_pin.sym} 200 -300 0 0 {name=lsv1 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 150 -300 0 0 {name=lvt1 sig_type=std_logic lab=VTUNE}
C {lab_pin.sym} 250 -310 2 0 {name=llo1 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 250 -290 2 0 {name=llo2 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 850 -980 0 0 {name=lt1 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 850 -940 0 0 {name=lt2 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 850 -880 0 0 {name=lt3 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 850 -840 0 0 {name=lt4 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 850 -780 0 0 {name=lt5 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 850 -740 0 0 {name=lt6 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 850 -680 0 0 {name=lt7 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 850 -640 0 0 {name=lt8 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 850 -580 0 0 {name=lt9 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 850 -540 0 0 {name=lt10 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 850 -480 0 0 {name=lt11 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 850 -440 0 0 {name=lt12 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 930 -1010 1 0 {name=ltps0 sig_type=std_logic lab=VCTRL_PS0}
C {lab_pin.sym} 930 -910 1 0 {name=ltps1 sig_type=std_logic lab=VCTRL_PS1}
C {lab_pin.sym} 930 -810 1 0 {name=ltps2 sig_type=std_logic lab=VCTRL_PS2}
C {lab_pin.sym} 930 -710 1 0 {name=ltps3 sig_type=std_logic lab=VCTRL_PS3}
C {lab_pin.sym} 930 -610 1 0 {name=ltps4 sig_type=std_logic lab=VCTRL_PS4}
C {lab_pin.sym} 930 -510 1 0 {name=ltps5 sig_type=std_logic lab=VCTRL_PS5}
C {lab_pin.sym} 1000 -1010 1 0 {name=ltv1 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 1030 -1010 1 0 {name=ltv2 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 1000 -910 1 0 {name=ltv3 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 1030 -910 1 0 {name=ltv4 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 1000 -810 1 0 {name=ltv5 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 1030 -810 1 0 {name=ltv6 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 1000 -710 1 0 {name=ltv7 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 1030 -710 1 0 {name=ltv8 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 1000 -610 1 0 {name=ltv9 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 1030 -610 1 0 {name=ltv10 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 1000 -510 1 0 {name=ltv11 sig_type=std_logic lab=VCC_33}
C {lab_pin.sym} 1030 -510 1 0 {name=ltv12 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 1000 -990 3 0 {name=ltg1 sig_type=std_logic lab=GND}
C {lab_pin.sym} 1030 -990 3 0 {name=lts1 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 1000 -890 3 0 {name=ltg2 sig_type=std_logic lab=GND}
C {lab_pin.sym} 1030 -890 3 0 {name=lts2 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 1000 -790 3 0 {name=ltg3 sig_type=std_logic lab=GND}
C {lab_pin.sym} 1030 -790 3 0 {name=lts3 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 1000 -690 3 0 {name=ltg4 sig_type=std_logic lab=GND}
C {lab_pin.sym} 1030 -690 3 0 {name=lts4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 1000 -590 3 0 {name=ltg5 sig_type=std_logic lab=GND}
C {lab_pin.sym} 1030 -590 3 0 {name=lts5 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 1000 -490 3 0 {name=ltg6 sig_type=std_logic lab=GND}
C {lab_pin.sym} 1030 -490 3 0 {name=lts6 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 1150 -980 2 0 {name=lta1 sig_type=std_logic lab=ANT_TX0P}
C {lab_pin.sym} 1150 -940 2 0 {name=lta2 sig_type=std_logic lab=ANT_TX0N}
C {lab_pin.sym} 1150 -880 2 0 {name=lta3 sig_type=std_logic lab=ANT_TX1P}
C {lab_pin.sym} 1150 -840 2 0 {name=lta4 sig_type=std_logic lab=ANT_TX1N}
C {lab_pin.sym} 1150 -780 2 0 {name=lta5 sig_type=std_logic lab=ANT_TX2P}
C {lab_pin.sym} 1150 -740 2 0 {name=lta6 sig_type=std_logic lab=ANT_TX2N}
C {lab_pin.sym} 1150 -680 2 0 {name=lta7 sig_type=std_logic lab=ANT_TX3P}
C {lab_pin.sym} 1150 -640 2 0 {name=lta8 sig_type=std_logic lab=ANT_TX3N}
C {lab_pin.sym} 1150 -580 2 0 {name=lta9 sig_type=std_logic lab=ANT_TX4P}
C {lab_pin.sym} 1150 -540 2 0 {name=lta10 sig_type=std_logic lab=ANT_TX4N}
C {lab_pin.sym} 1150 -480 2 0 {name=lta11 sig_type=std_logic lab=ANT_TX5P}
C {lab_pin.sym} 1150 -440 2 0 {name=lta12 sig_type=std_logic lab=ANT_TX5N}
C {lab_pin.sym} 200 -130 3 0 {name=lbv1 sig_type=std_logic lab=VDD_12}
C {lab_pin.sym} 200 -70 1 0 {name=lbg1 sig_type=std_logic lab=GND}
C {lab_pin.sym} 200 -100 0 0 {name=lbs1 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 250 -110 2 0 {name=lbr1 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 250 -90 2 0 {name=lbi1 sig_type=std_logic lab=IBIAS_OUT}
