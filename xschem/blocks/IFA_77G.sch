v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {IFA — 2-Stage IF Amplifier, 44dB} 0 -650 0 0 0.5 0.5 {}
N 80 -400 180 -400 {lab=INP}
N 420 -400 520 -400 {lab=INN}
N 220 -370 380 -370 {lab=tail1}
N 220 -170 380 -170 {lab=tail2}
N 300 -600 300 -570 {lab=VCC}
N 380 -570 440 -570 {lab=VCC}
N 220 -570 220 -530 {lab=VCC}
N 380 -570 380 -530 {lab=VCC}
N 160 -570 160 -330 {lab=VCC}
N 160 -330 220 -330 {lab=VCC}
N 440 -570 440 -330 {lab=VCC}
N 380 -330 440 -330 {lab=VCC}
N 260 -40 300 -40 {lab=GND}
N 260 -110 260 -40 {lab=GND}
N 260 -310 300 -310 {lab=GND}
N 260 -110 300 -110 {lab=GND}
N 220 -470 220 -430 {lab=out1p}
N 70 -430 220 -430 {lab=out1p}
N 70 -430 70 -200 {lab=out1p}
N 70 -200 180 -200 {lab=out1p}
N 380 -470 380 -430 {lab=out1n}
N 380 -430 530 -430 {lab=out1n}
N 530 -430 530 -200 {lab=out1n}
N 420 -200 530 -200 {lab=out1n}
N 220 -260 220 -230 {lab=OUTP}
N 80 -260 220 -260 {lab=OUTP}
N 380 -260 380 -230 {lab=OUTN}
N 380 -260 520 -260 {lab=OUTN}
N 220 -570 300 -570 {lab=VCC}
N 160 -570 220 -570 {lab=VCC}
N 300 -570 380 -570 {lab=VCC}
N 260 -310 260 -110 {lab=GND}
N 220 -270 220 -260 {lab=OUTP}
N 380 -270 380 -260 {lab=OUTN}
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
C {lab_pin.sym} 220 -400 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -400 2 0 {name=l8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 220 -200 0 0 {name=l12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -200 2 0 {name=l16 sig_type=std_logic lab=sub!}
