v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {77 GHz Mixer (MIXER_77GD) — LVS-Equivalent Schematic} 50 -900 0 0 0.5 0.5 {}
T {Physical PDK cells only — matches generate_mixer_transistor.py} 50 -860 0 0 0.3 0.3 {layer=7}
N 220 -270 220 -200 {lab=GND}
N 480 -270 480 -200 {lab=GND}
N 350 -200 480 -200 {lab=GND}
N 350 -200 350 -50 {lab=GND}
N 220 -520 220 -330 {lab=ELOL}
N 480 -520 480 -330 {lab=ELOR}
N 170 -700 170 -580 {lab=IFP}
N 280 -700 280 -580 {lab=IFN}
N 420 -700 420 -580 {lab=IFN}
N 530 -700 530 -580 {lab=IFP}
N 200 -800 200 -730 {lab=2V4}
N 500 -800 500 -730 {lab=2V4}
N 200 -800 500 -800 {lab=2V4}
N 50 -300 180 -300 {lab=RFP}
N 520 -300 650 -300 {lab=RFN}
N 50 -550 130 -550 {lab=LOP}
N 570 -550 650 -550 {lab=LON}
N 220 -200 350 -200 {lab=GND}
C {sg13g2_pr/npn13G2l.sym} 200 -300 0 0 {name=Q20
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -300 0 1 {name=Q21
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 150 -550 0 0 {name=Q22
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 300 -550 0 1 {name=Q23
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 400 -550 0 0 {name=Q24
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 550 -550 0 1 {name=Q25
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 650 -200 0 0 {name=Q26
model=npn13G2l
spiceprefix=X
Nx=1
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 650 -100 0 0 {name=Q27
model=npn13G2l
spiceprefix=X
Nx=1
m=1
El=2.5
selft=0}
C {sg13g2_pr/rppd.sym} 200 -700 0 0 {name=R21
model=rppd
spiceprefix=X
w=3.0u
l=18.23u
m=2
b=0}
C {sg13g2_pr/rppd.sym} 500 -700 0 0 {name=R22
model=rppd
spiceprefix=X
w=3.0u
l=18.23u
m=2
b=0}
C {sg13g2_pr/rppd.sym} 650 -250 0 0 {name=R23
model=rppd
spiceprefix=X
w=3.0u
l=27.48u
m=1
b=0}
C {sg13g2_pr/cap_cmim.sym} 100 -450 0 0 {name=C37
model=cap_cmim
spiceprefix=X
W=5.0u
L=5.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 600 -450 0 0 {name=C38
model=cap_cmim
spiceprefix=X
W=5.0u
L=5.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 100 -250 0 0 {name=C39
model=cap_cmim
spiceprefix=X
W=4.0u
L=4.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 600 -250 0 0 {name=C40
model=cap_cmim
spiceprefix=X
W=4.0u
L=4.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 750 -750 0 0 {name=C41
model=cap_cmim
spiceprefix=X
W=30.0u
L=30.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 750 -700 0 0 {name=C42
model=cap_cmim
spiceprefix=X
W=30.0u
L=30.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 750 -650 0 0 {name=C43
model=cap_cmim
spiceprefix=X
W=30.0u
L=30.0u
m=1}
C {iopin.sym} 350 -800 0 0 {name=p1 lab=2V4}
C {iopin.sym} 350 -50 0 0 {name=p2 lab=GND}
C {iopin.sym} 50 -300 0 1 {name=p3 lab=RFP}
C {iopin.sym} 650 -300 0 0 {name=p4 lab=RFN}
C {iopin.sym} 50 -550 0 1 {name=p5 lab=LOP}
C {iopin.sym} 650 -550 0 0 {name=p6 lab=LON}
C {iopin.sym} 200 -750 0 0 {name=p7 lab=IFP}
C {iopin.sym} 500 -750 0 0 {name=p8 lab=IFN}
C {lab_pin.sym} 220 -420 0 0 {name=p9 sig_type=std_logic lab=ELOL}
C {lab_pin.sym} 480 -420 0 0 {name=p10 sig_type=std_logic lab=ELOR}
