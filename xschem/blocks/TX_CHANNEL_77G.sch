v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {TX Channel — Phase Shifter + PA} 0 -550 0 0 0.5 0.5 {}
C {PHASE_SHIFTER_77G.sym} 200 -400 0 0 {name=x_ps}
C {TXPA_77G.sym} 500 -400 0 0 {name=x_pa}
C {iopin.sym} 50 -410 0 1 {name=p1 lab=INP}
C {iopin.sym} 50 -390 0 1 {name=p2 lab=INN}
C {iopin.sym} 700 -410 0 0 {name=p3 lab=ANT_TXP}
C {iopin.sym} 700 -390 0 0 {name=p4 lab=ANT_TXN}
C {iopin.sym} 200 -500 0 0 {name=p5 lab=VCTRL_PS}
C {iopin.sym} 350 -500 0 0 {name=p6 lab=VCC}
C {iopin.sym} 350 -300 0 0 {name=p7 lab=GND}
C {iopin.sym} 400 -300 0 0 {name=p8 lab=sub!}
C {iopin.sym} 500 -500 0 0 {name=p9 lab=VREF}
C {lab_pin.sym} 200 -440 3 0 {name=l1 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 200 -360 1 0 {name=l2 sig_type=std_logic lab=GND}
C {lab_pin.sym} 200 -400 0 0 {name=l3 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 150 -420 0 0 {name=l4 sig_type=std_logic lab=INP}
C {lab_pin.sym} 150 -400 0 0 {name=l5 sig_type=std_logic lab=INN}
C {lab_pin.sym} 200 -460 3 0 {name=l6 sig_type=std_logic lab=VCTRL_PS}
C {lab_pin.sym} 250 -420 2 0 {name=l7 sig_type=std_logic lab=ps_op}
C {lab_pin.sym} 250 -400 2 0 {name=l8 sig_type=std_logic lab=ps_on}
C {lab_pin.sym} 500 -440 3 0 {name=l9 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 500 -360 1 0 {name=l10 sig_type=std_logic lab=GND}
C {lab_pin.sym} 500 -400 0 0 {name=l11 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 450 -420 0 0 {name=l12 sig_type=std_logic lab=ps_op}
C {lab_pin.sym} 450 -400 0 0 {name=l13 sig_type=std_logic lab=ps_on}
C {lab_pin.sym} 450 -440 0 0 {name=l14 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 550 -420 2 0 {name=l15 sig_type=std_logic lab=ANT_TXP}
C {lab_pin.sym} 550 -400 2 0 {name=l16 sig_type=std_logic lab=ANT_TXN}
