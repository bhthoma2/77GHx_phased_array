v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {77 GHz TX PA (TXAMP_77GD) — LVS-Equivalent Schematic} 50 -900 0 0 0.5 0.5 {}
T {Physical PDK cells only — matches generate_txpa_transistor.py} 50 -860 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 200 -300 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=4
m=2
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -300 0 1 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=4
m=2
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 200 -550 0 0 {name=Q3
model=npn13G2l
spiceprefix=X
Nx=4
m=2
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -550 0 1 {name=Q4
model=npn13G2l
spiceprefix=X
Nx=4
m=2
El=2.5
selft=0}
C {sg13g2_pr/rppd.sym} 350 -150 0 0 {name=R_bias
model=rppd
spiceprefix=X
w=3.0u
l=10.0u
m=1
b=0}
C {iopin.sym} 350 -750 0 0 {name=p1 lab=2V4}
C {iopin.sym} 350 -50 0 0 {name=p2 lab=GND}
C {iopin.sym} 50 -300 0 1 {name=p3 lab=INP}
C {iopin.sym} 650 -300 0 0 {name=p4 lab=INN}
C {iopin.sym} 50 -650 0 1 {name=p5 lab=OUTP}
C {iopin.sym} 650 -650 0 0 {name=p6 lab=OUTN}
C {iopin.sym} 350 -500 0 0 {name=p7 lab=VCB}
N 220 -270 220 -200 {lab=GND}
N 480 -270 480 -200 {lab=GND}
N 220 -200 480 -200 {lab=GND}
N 350 -200 350 -180 {lab=GND}
N 350 -120 350 -50 {lab=GND}
N 220 -330 220 -520 {lab=MIDL}
N 480 -330 480 -520 {lab=MIDR}
N 220 -580 220 -650 {lab=OUTP}
N 480 -580 480 -650 {lab=OUTN}
N 50 -650 220 -650 {lab=OUTP}
N 480 -650 650 -650 {lab=OUTN}
N 50 -300 180 -300 {lab=INP}
N 520 -300 650 -300 {lab=INN}
N 180 -550 180 -550 {lab=VCB}
N 520 -550 520 -550 {lab=VCB}
N 350 -500 350 -500 {lab=VCB}
N 220 -650 220 -750 {lab=2V4}
N 480 -650 480 -750 {lab=2V4}
N 220 -750 480 -750 {lab=2V4}
N 350 -750 350 -750 {lab=2V4}
C {lab_pin.sym} 180 -550 0 1 {name=p8 sig_type=std_logic lab=VCB}
C {lab_pin.sym} 520 -550 0 0 {name=p9 sig_type=std_logic lab=VCB}
C {lab_pin.sym} 220 -420 0 0 {name=p10 sig_type=std_logic lab=MIDL}
C {lab_pin.sym} 480 -420 0 0 {name=p11 sig_type=std_logic lab=MIDR}