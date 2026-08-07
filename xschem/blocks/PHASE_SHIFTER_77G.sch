v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {PHASE_SHIFTER — Reflective-Type, Varactor-Loaded TL} 0 -550 0 0 0.5 0.5 {}
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
C {devices/res.sym} 300 -430 0 0 {name=Rbias
value=5k}
C {iopin.sym} 80 -300 0 1 {name=p1 lab=INP}
C {iopin.sym} 520 -300 0 0 {name=p2 lab=INN}
C {iopin.sym} 80 -350 0 1 {name=p3 lab=OUTP}
C {iopin.sym} 520 -350 0 0 {name=p4 lab=OUTN}
C {iopin.sym} 300 -500 0 0 {name=p5 lab=VCTRL_PS}
C {iopin.sym} 300 -200 0 0 {name=p6 lab=GND}
C {iopin.sym} 200 -430 0 0 {name=p7 lab=VCC}
C {iopin.sym} 350 -200 0 0 {name=p8 lab=sub!}
C {lab_pin.sym} 220 -330 3 0 {name=l1 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 180 -300 0 0 {name=l2 sig_type=std_logic lab=INP}
C {lab_pin.sym} 220 -270 1 0 {name=l3 sig_type=std_logic lab=tail}
C {lab_pin.sym} 220 -300 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -330 3 0 {name=l5 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 420 -300 2 0 {name=l6 sig_type=std_logic lab=INN}
C {lab_pin.sym} 380 -270 1 0 {name=l7 sig_type=std_logic lab=tail}
C {lab_pin.sym} 380 -300 2 0 {name=l8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 300 -460 3 0 {name=l9 sig_type=std_logic lab=VCTRL_PS}
C {lab_pin.sym} 300 -400 1 0 {name=l10 sig_type=std_logic lab=tail}
C {lab_pin.sym} 200 -430 0 0 {name=l11 sig_type=std_logic lab=VCC}
N 200 -430 220 -430 {lab=VCC}
N 220 -430 220 -330 {lab=VCC}
N 380 -430 380 -330 {lab=VCC}
N 220 -430 380 -430 {lab=VCC}
N 220 -270 300 -270 {lab=tail}
N 300 -270 380 -270 {lab=tail}
N 300 -270 300 -200 {lab=GND}
