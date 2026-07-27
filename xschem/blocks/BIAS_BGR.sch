v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {BIAS — Brokaw BGR, 1.17V} 0 -550 0 0 0.5 0.5 {}
C {sg13g2_pr/npn13G2l.sym} 200 -300 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 400 -300 0 0 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=8
El=2.5
selft=0}
C {devices/res.sym} 220 -200 0 0 {name=R1
value=5.4k}
C {devices/res.sym} 550 -300 0 0 {name=R2
value=18k}
C {devices/res.sym} 310 -380 0 0 {name=Rfb
value=50}
C {devices/res.sym} 470 -380 0 0 {name=Rout
value=100}
C {devices/isource.sym} 220 -430 0 0 {name=I1
value="DC 200u"}
C {devices/isource.sym} 420 -430 0 0 {name=I2
value="DC 200u"}
C {iopin.sym} 600 -300 0 0 {name=p1 lab=VREF}
C {iopin.sym} 320 -530 0 0 {name=p2 lab=VCC}
C {iopin.sym} 320 -80 0 0 {name=p3 lab=GND}
C {iopin.sym} 370 -80 0 0 {name=p4 lab=sub!}
C {lab_pin.sym} 220 -330 3 0 {name=l1 sig_type=std_logic lab=c1}
C {lab_pin.sym} 180 -300 0 0 {name=l2 sig_type=std_logic lab=c1}
C {lab_pin.sym} 220 -270 1 0 {name=l3 sig_type=std_logic lab=e1}
C {lab_pin.sym} 220 -300 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 420 -330 3 0 {name=l5 sig_type=std_logic lab=c2}
C {lab_pin.sym} 380 -300 0 0 {name=l6 sig_type=std_logic lab=c2}
C {lab_pin.sym} 420 -270 1 0 {name=l7 sig_type=std_logic lab=GND}
C {lab_pin.sym} 420 -300 0 0 {name=l8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 220 -230 3 0 {name=l9 sig_type=std_logic lab=e1}
C {lab_pin.sym} 220 -170 1 0 {name=l10 sig_type=std_logic lab=GND}
C {lab_pin.sym} 550 -330 3 0 {name=l11 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 550 -270 1 0 {name=l12 sig_type=std_logic lab=GND}
C {lab_pin.sym} 310 -410 3 0 {name=l13 sig_type=std_logic lab=c1}
C {lab_pin.sym} 310 -350 1 0 {name=l14 sig_type=std_logic lab=c2}
C {lab_pin.sym} 470 -410 3 0 {name=l15 sig_type=std_logic lab=c2}
C {lab_pin.sym} 470 -350 1 0 {name=l16 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 220 -460 3 0 {name=l17 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 220 -400 1 0 {name=l18 sig_type=std_logic lab=c1}
C {lab_pin.sym} 420 -460 3 0 {name=l19 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 420 -400 1 0 {name=l20 sig_type=std_logic lab=c2}
