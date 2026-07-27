v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VGA — Variable-gm, 0-31dB} 0 -550 0 0 0.5 0.5 {}
C {sg13g2_pr/npn13G2l.sym} 200 -300 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=2
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 400 -300 0 1 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=2
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 300 -150 0 0 {name=Qtail
model=npn13G2l
spiceprefix=X
Nx=4
El=2.5
selft=0}
C {devices/res.sym} 220 -400 0 0 {name=RL1
value=500}
C {devices/res.sym} 380 -400 0 0 {name=RL2
value=500}
C {devices/res.sym} 320 -60 0 0 {name=RE
value=10}
C {iopin.sym} 80 -300 0 1 {name=p1 lab=INP}
C {iopin.sym} 520 -300 0 0 {name=p2 lab=INN}
C {iopin.sym} 80 -370 0 1 {name=p3 lab=OUTP}
C {iopin.sym} 520 -370 0 0 {name=p4 lab=OUTN}
C {iopin.sym} 180 -150 0 1 {name=p5 lab=VCTRL}
C {iopin.sym} 300 -500 0 0 {name=p6 lab=VCC}
C {iopin.sym} 320 20 0 0 {name=p7 lab=GND}
C {iopin.sym} 350 20 0 0 {name=p8 lab=sub!}
C {lab_pin.sym} 220 -330 3 0 {name=l1 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 180 -300 0 0 {name=l2 sig_type=std_logic lab=INP}
C {lab_pin.sym} 220 -270 1 0 {name=l3 sig_type=std_logic lab=tail}
C {lab_pin.sym} 220 -300 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -330 3 0 {name=l5 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 420 -300 2 0 {name=l6 sig_type=std_logic lab=INN}
C {lab_pin.sym} 380 -270 1 0 {name=l7 sig_type=std_logic lab=tail}
C {lab_pin.sym} 380 -300 2 0 {name=l8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 320 -180 3 0 {name=l9 sig_type=std_logic lab=tail}
C {lab_pin.sym} 280 -150 0 0 {name=l10 sig_type=std_logic lab=VCTRL}
C {lab_pin.sym} 320 -120 1 0 {name=l11 sig_type=std_logic lab=etail}
C {lab_pin.sym} 320 -150 0 0 {name=l12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 220 -430 3 0 {name=l13 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 220 -370 1 0 {name=l14 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 380 -430 3 0 {name=l15 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 380 -370 1 0 {name=l16 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 320 -90 3 0 {name=l17 sig_type=std_logic lab=etail}
C {lab_pin.sym} 320 -30 1 0 {name=l18 sig_type=std_logic lab=GND}
