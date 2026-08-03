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
N 80 -300 180 -300 {lab=INP}
N 420 -300 520 -300 {lab=INN}
N 220 -330 220 -370 {lab=OUTP}
N 380 -330 380 -370 {lab=OUTN}
N 220 -370 80 -370 {lab=OUTP}
N 380 -370 520 -370 {lab=OUTN}
N 220 -270 220 -240 {lab=tail}
N 220 -240 380 -240 {lab=tail}
N 380 -270 380 -240 {lab=tail}
N 320 -180 320 -240 {lab=tail}
N 220 -430 220 -470 {lab=VCC}
N 380 -430 380 -470 {lab=VCC}
N 220 -470 300 -470 {lab=VCC}
N 300 -470 380 -470 {lab=VCC}
N 300 -500 300 -470 {lab=VCC}
N 180 -150 280 -150 {lab=VCTRL}
N 320 -120 320 -90 {lab=etail}
N 320 -30 320 20 {lab=GND}
N 320 20 350 20 {lab=GND}
C {lab_wire.sym} 220 -300 0 0 {name=lw1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 380 -300 2 0 {name=lw2 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 320 -150 0 0 {name=lw3 sig_type=std_logic lab=sub!}
