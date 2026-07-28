v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {IFA — 2-Stage IF Amplifier, LVS Equivalent} 0 -850 0 0 0.5 0.5 {}
T {4×gm + 2×tail + 1×bias ref, 4×load R, 3×bias R, 2×bypass C} 0 -810 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 200 -500 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=2
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 400 -500 0 1 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=2
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 200 -250 0 0 {name=Q3
model=npn13G2l
spiceprefix=X
Nx=2
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 400 -250 0 1 {name=Q4
model=npn13G2l
spiceprefix=X
Nx=2
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 280 -380 0 0 {name=Q5
model=npn13G2l
spiceprefix=X
Nx=2
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 280 -130 0 0 {name=Q6
model=npn13G2l
spiceprefix=X
Nx=2
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 550 -350 0 0 {name=Q7
model=npn13G2l
spiceprefix=X
Nx=1
m=1
El=2.5
selft=0}
C {sg13g2_pr/rppd.sym} 220 -620 0 0 {name=R1
model=rppd
spiceprefix=X
w=3.0u
l=8.33u
m=1
b=0}
C {sg13g2_pr/rppd.sym} 380 -620 0 0 {name=R2
model=rppd
spiceprefix=X
w=3.0u
l=8.33u
m=1
b=0}
C {sg13g2_pr/rppd.sym} 220 -370 0 0 {name=R3
model=rppd
spiceprefix=X
w=3.0u
l=8.33u
m=1
b=0}
C {sg13g2_pr/rppd.sym} 380 -370 0 0 {name=R4
model=rppd
spiceprefix=X
w=3.0u
l=8.33u
m=1
b=0}
C {sg13g2_pr/rppd.sym} 570 -470 0 0 {name=R5
model=rppd
spiceprefix=X
w=3.0u
l=18.23u
m=1
b=0}
C {sg13g2_pr/rppd.sym} 570 -250 0 0 {name=R6
model=rppd
spiceprefix=X
w=3.0u
l=5.0u
m=1
b=0}
C {sg13g2_pr/rppd.sym} 300 -310 0 0 {name=R7
model=rppd
spiceprefix=X
w=3.0u
l=5.0u
m=1
b=0}
C {sg13g2_pr/cap_cmim.sym} 650 -600 0 0 {name=C1
model=cap_cmim
spiceprefix=X
W=30.0u
L=30.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 650 -500 0 0 {name=C2
model=cap_cmim
spiceprefix=X
W=30.0u
L=30.0u
m=1}
C {iopin.sym} 80 -500 0 1 {name=p1 lab=INP}
C {iopin.sym} 520 -500 0 0 {name=p2 lab=INN}
C {iopin.sym} 80 -280 0 1 {name=p3 lab=OUTP}
C {iopin.sym} 520 -280 0 0 {name=p4 lab=OUTN}
C {iopin.sym} 300 -750 0 0 {name=p5 lab=VCC}
C {iopin.sym} 300 -40 0 0 {name=p6 lab=GND}
C {iopin.sym} 350 -40 0 0 {name=p7 lab=sub!}
C {lab_pin.sym} 180 -500 0 1 {name=l1 sig_type=std_logic lab=INP}
C {lab_pin.sym} 420 -500 0 0 {name=l2 sig_type=std_logic lab=INN}
C {lab_pin.sym} 220 -530 0 0 {name=l3 sig_type=std_logic lab=out1p}
C {lab_pin.sym} 380 -530 0 0 {name=l4 sig_type=std_logic lab=out1n}
C {lab_pin.sym} 220 -470 0 0 {name=l5 sig_type=std_logic lab=tail1}
C {lab_pin.sym} 380 -470 0 0 {name=l6 sig_type=std_logic lab=tail1}
C {lab_pin.sym} 220 -500 0 0 {name=l7 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -500 0 0 {name=l8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 220 -650 0 0 {name=l9 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 380 -650 0 0 {name=l10 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 220 -590 0 0 {name=l11 sig_type=std_logic lab=out1p}
C {lab_pin.sym} 380 -590 0 0 {name=l12 sig_type=std_logic lab=out1n}
C {lab_pin.sym} 300 -410 0 0 {name=l13 sig_type=std_logic lab=tail1}
C {lab_pin.sym} 260 -380 0 1 {name=l14 sig_type=std_logic lab=BIAS}
C {lab_pin.sym} 300 -350 0 0 {name=l15 sig_type=std_logic lab=tail1_e}
C {lab_pin.sym} 300 -380 0 0 {name=l16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 300 -340 0 0 {name=l17 sig_type=std_logic lab=tail1_e}
C {lab_pin.sym} 300 -280 0 0 {name=l18 sig_type=std_logic lab=GND}
C {lab_pin.sym} 180 -250 0 1 {name=l19 sig_type=std_logic lab=out1p}
C {lab_pin.sym} 420 -250 0 0 {name=l20 sig_type=std_logic lab=out1n}
C {lab_pin.sym} 220 -280 0 0 {name=l21 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 380 -280 0 0 {name=l22 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 220 -220 0 0 {name=l23 sig_type=std_logic lab=tail2}
C {lab_pin.sym} 380 -220 0 0 {name=l24 sig_type=std_logic lab=tail2}
C {lab_pin.sym} 220 -250 0 0 {name=l25 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -250 0 0 {name=l26 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 220 -400 0 0 {name=l27 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 380 -400 0 0 {name=l28 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 220 -340 0 0 {name=l29 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 380 -340 0 0 {name=l30 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 300 -160 0 0 {name=l31 sig_type=std_logic lab=tail2}
C {lab_pin.sym} 260 -130 0 1 {name=l32 sig_type=std_logic lab=BIAS}
C {lab_pin.sym} 300 -100 0 0 {name=l33 sig_type=std_logic lab=GND}
C {lab_pin.sym} 300 -130 0 0 {name=l34 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 570 -380 0 0 {name=l35 sig_type=std_logic lab=BIAS}
C {lab_pin.sym} 530 -350 0 1 {name=l36 sig_type=std_logic lab=BIAS}
C {lab_pin.sym} 570 -320 0 0 {name=l37 sig_type=std_logic lab=BIAS_E}
C {lab_pin.sym} 570 -350 0 0 {name=l38 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 570 -500 0 0 {name=l39 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 570 -440 0 0 {name=l40 sig_type=std_logic lab=BIAS}
C {lab_pin.sym} 570 -280 0 0 {name=l41 sig_type=std_logic lab=BIAS_E}
C {lab_pin.sym} 570 -220 0 0 {name=l42 sig_type=std_logic lab=GND}
C {lab_pin.sym} 80 -280 0 1 {name=l43 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 520 -280 0 0 {name=l44 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 650 -630 0 0 {name=l45 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 650 -570 0 0 {name=l46 sig_type=std_logic lab=GND}
C {lab_pin.sym} 650 -530 0 0 {name=l47 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 650 -470 0 0 {name=l48 sig_type=std_logic lab=GND}