v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {77 GHz Cross-Coupled LC VCO} 50 -700 0 0 0.5 0.5 {}
T {f_osc=76.1GHz, Vdiff=1.05V, Pdc=19.8mW} 50 -660 0 0 0.3 0.3 {layer=7}
T {Tank: L=27pH, Cvar=15fF, Q1/Q2 cross-coupled} 50 -630 0 0 0.3 0.3 {layer=7}
N 220 -550 220 -480 {lab=VCC}
N 380 -550 380 -480 {lab=VCC}
N 220 -550 380 -550 {lab=VCC}
N 100 -550 220 -550 {lab=VCC}
N 220 -420 220 -380 {lab=OUTP}
N 380 -420 380 -380 {lab=OUTN}
N 220 -380 270 -380 {lab=OUTP}
N 330 -380 380 -380 {lab=OUTN}
N 220 -340 270 -340 {lab=OUTP}
N 330 -340 380 -340 {lab=OUTN}
N 220 -270 220 -220 {lab=TAIL}
N 380 -270 380 -220 {lab=TAIL}
N 300 -220 380 -220 {lab=TAIL}
N 300 -220 300 -150 {lab=TAIL}
N 300 -90 300 -60 {lab=GND}
N 140 -380 220 -380 {lab=OUTP}
N 380 -380 460 -380 {lab=OUTN}
N 220 -220 300 -220 {lab=TAIL}
C {sg13g2_pr/npn13G2l.sym} 200 -300 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=1
m=2
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 400 -300 0 1 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=1
m=2
El=2.5
selft=0}
C {devices/ind.sym} 220 -450 0 0 {name=L1
value=27p}
C {devices/ind.sym} 380 -450 0 0 {name=L2
value=27p}
C {devices/capa.sym} 300 -380 3 0 {name=CVAR1
value=15f}
C {devices/capa.sym} 300 -340 3 0 {name=CVAR2
value=12f}
C {devices/isource.sym} 300 -120 0 0 {name=ITAIL
value="DC 5m"}
C {iopin.sym} 100 -550 0 1 {name=p1 lab=VCC}
C {iopin.sym} 300 -60 0 0 {name=p2 lab=GND}
C {iopin.sym} 140 -380 0 1 {name=p3 lab=OUTP}
C {iopin.sym} 460 -380 0 0 {name=p4 lab=OUTN}
C {iopin.sym} 300 -340 0 0 {name=p5 lab=VTUNE}
C {iopin.sym} 100 -300 0 1 {name=p6 lab=sub|}
C {lab_pin.sym} 180 -300 0 1 {name=p7 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 420 -300 0 0 {name=p8 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 220 -300 0 0 {name=p9 sig_type=std_logic lab=sub|}
C {lab_pin.sym} 380 -300 0 0 {name=p10 sig_type=std_logic lab=sub|}
