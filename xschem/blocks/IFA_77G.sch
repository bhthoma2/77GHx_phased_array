v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {IFA — 2-Stage IF Amplifier, 44dB} 0 -650 0 0 0.5 0.5 {}
C {sg13g2_pr/npn13G2l.sym} 200 -400 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=2
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 400 -400 0 1 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=2
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 200 -200 0 0 {name=Q3
model=npn13G2l
spiceprefix=X
Nx=2
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 400 -200 0 1 {name=Q4
model=npn13G2l
spiceprefix=X
Nx=2
El=2.5
selft=0}
C {devices/res.sym} 220 -500 0 0 {name=RL1
value=500}
C {devices/res.sym} 380 -500 0 0 {name=RL2
value=500}
C {devices/res.sym} 220 -300 0 0 {name=RL3
value=500}
C {devices/res.sym} 380 -300 0 0 {name=RL4
value=500}
C {devices/isource.sym} 300 -340 0 0 {name=ITAIL1
value="DC 2m"}
C {devices/isource.sym} 300 -140 0 0 {name=ITAIL2
value="DC 2m"}
C {iopin.sym} 80 -400 0 1 {name=p1 lab=INP}
C {iopin.sym} 520 -400 0 0 {name=p2 lab=INN}
C {iopin.sym} 80 -260 0 1 {name=p3 lab=OUTP}
C {iopin.sym} 520 -260 0 0 {name=p4 lab=OUTN}
C {iopin.sym} 300 -600 0 0 {name=p5 lab=VCC}
C {iopin.sym} 300 -40 0 0 {name=p6 lab=GND}
C {iopin.sym} 350 -40 0 0 {name=p7 lab=sub!}
C {lab_pin.sym} 220 -430 3 0 {name=l1 sig_type=std_logic lab=out1p}
C {lab_pin.sym} 180 -400 0 0 {name=l2 sig_type=std_logic lab=INP}
C {lab_pin.sym} 220 -370 1 0 {name=l3 sig_type=std_logic lab=tail1}
C {lab_pin.sym} 220 -400 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -430 3 0 {name=l5 sig_type=std_logic lab=out1n}
C {lab_pin.sym} 420 -400 2 0 {name=l6 sig_type=std_logic lab=INN}
C {lab_pin.sym} 380 -370 1 0 {name=l7 sig_type=std_logic lab=tail1}
C {lab_pin.sym} 380 -400 2 0 {name=l8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 220 -230 3 0 {name=l9 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 180 -200 0 0 {name=l10 sig_type=std_logic lab=out1p}
C {lab_pin.sym} 220 -170 1 0 {name=l11 sig_type=std_logic lab=tail2}
C {lab_pin.sym} 220 -200 0 0 {name=l12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -230 3 0 {name=l13 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 420 -200 2 0 {name=l14 sig_type=std_logic lab=out1n}
C {lab_pin.sym} 380 -170 1 0 {name=l15 sig_type=std_logic lab=tail2}
C {lab_pin.sym} 380 -200 2 0 {name=l16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 220 -530 3 0 {name=l17 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 220 -470 1 0 {name=l18 sig_type=std_logic lab=out1p}
C {lab_pin.sym} 380 -530 3 0 {name=l19 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 380 -470 1 0 {name=l20 sig_type=std_logic lab=out1n}
C {lab_pin.sym} 220 -330 3 0 {name=l21 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 220 -270 1 0 {name=l22 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 380 -330 3 0 {name=l23 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 380 -270 1 0 {name=l24 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 300 -370 3 0 {name=l25 sig_type=std_logic lab=tail1}
C {lab_pin.sym} 300 -310 1 0 {name=l26 sig_type=std_logic lab=GND}
C {lab_pin.sym} 300 -170 3 0 {name=l27 sig_type=std_logic lab=tail2}
C {lab_pin.sym} 300 -110 1 0 {name=l28 sig_type=std_logic lab=GND}
