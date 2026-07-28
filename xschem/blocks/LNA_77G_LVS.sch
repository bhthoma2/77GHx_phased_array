v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {77 GHz LNA (RXAMP_77GD) — LVS-Equivalent Schematic} 50 -900 0 0 0.5 0.5 {}
T {Physical PDK cells only — matches generate_lna_transistor.py} 50 -860 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 200 -400 0 0 {name=Q33
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -400 0 1 {name=Q34
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 200 -600 0 0 {name=Q35
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -600 0 1 {name=Q36
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 100 -200 0 0 {name=Q37
model=npn13G2l
spiceprefix=X
Nx=1
m=1
El=2.5
selft=0}
C {sg13g2_pr/rppd.sym} 350 -250 0 0 {name=R29
model=rppd
spiceprefix=X
w=7.0u
l=38.8u
m=4
b=0}
C {sg13g2_pr/rppd.sym} 650 -650 0 0 {name=R30
model=rppd
spiceprefix=X
w=3.0u
l=18.23u
m=2
b=0}
C {sg13g2_pr/rppd.sym} 650 -600 0 0 {name=R31
model=rppd
spiceprefix=X
w=3.0u
l=18.23u
m=1
b=0}
C {sg13g2_pr/rppd.sym} 100 -130 0 0 {name=R32
model=rppd
spiceprefix=X
w=3.0u
l=18.23u
m=2
b=0}
C {sg13g2_pr/rppd.sym} 100 -80 0 0 {name=R33
model=rppd
spiceprefix=X
w=2.5u
l=10.53u
m=14
b=0}
C {sg13g2_pr/cap_cmim.sym} 150 -350 0 0 {name=C53
model=cap_cmim
spiceprefix=X
W=6.0u
L=6.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 550 -350 0 0 {name=C54
model=cap_cmim
spiceprefix=X
W=6.0u
L=6.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 150 -700 0 0 {name=C55
model=cap_cmim
spiceprefix=X
W=4.0u
L=4.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 550 -700 0 0 {name=C56
model=cap_cmim
spiceprefix=X
W=4.0u
L=4.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 700 -750 0 0 {name=C57
model=cap_cmim
spiceprefix=X
W=100.0u
L=15.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 700 -700 0 0 {name=C58
model=cap_cmim
spiceprefix=X
W=100.0u
L=20.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 700 -650 0 0 {name=C59
model=cap_cmim
spiceprefix=X
W=100.0u
L=20.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 700 -600 0 0 {name=C60
model=cap_cmim
spiceprefix=X
W=100.0u
L=15.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 700 -550 0 0 {name=C61
model=cap_cmim
spiceprefix=X
W=100.0u
L=15.0u
m=1}
C {iopin.sym} 350 -800 0 0 {name=p1 lab=2V4}
C {iopin.sym} 350 -50 0 0 {name=p2 lab=GND}
C {iopin.sym} 50 -400 0 1 {name=p3 lab=INP}
C {iopin.sym} 650 -400 0 0 {name=p4 lab=INN}
C {iopin.sym} 50 -700 0 1 {name=p5 lab=OUTP}
C {iopin.sym} 650 -700 0 0 {name=p6 lab=OUTN}
C {iopin.sym} 650 -650 0 0 {name=p7 lab=B35&36}
C {iopin.sym} 100 -200 0 1 {name=p8 lab=BIAS6}
N 220 -370 220 -300 {lab=GND}
N 480 -370 480 -300 {lab=GND}
N 220 -300 480 -300 {lab=GND}
N 350 -300 350 -280 {lab=GND}
N 350 -220 350 -50 {lab=GND}
N 220 -430 220 -570 {lab=MIDL}
N 480 -430 480 -570 {lab=MIDR}
N 220 -630 220 -700 {lab=OUTP}
N 480 -630 480 -700 {lab=OUTN}
N 50 -700 220 -700 {lab=OUTP}
N 480 -700 650 -700 {lab=OUTN}
N 180 -400 180 -400 {lab=INP}
N 50 -400 180 -400 {lab=INP}
N 520 -400 650 -400 {lab=INN}
N 180 -600 180 -600 {lab=B35&36}
N 520 -600 520 -600 {lab=B35&36}
N 350 -800 350 -750 {lab=2V4}
C {lab_pin.sym} 180 -600 0 1 {name=p9 sig_type=std_logic lab=B35&36}
C {lab_pin.sym} 520 -600 0 0 {name=p10 sig_type=std_logic lab=B35&36}
C {lab_pin.sym} 220 -500 0 0 {name=p11 sig_type=std_logic lab=MIDL}
C {lab_pin.sym} 480 -500 0 0 {name=p12 sig_type=std_logic lab=MIDR}