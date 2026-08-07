v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {PHASE_SHIFTER — 2-Bit Switched-Line (45deg + 22.5deg)} 0 -700 0 0 0.5 0.5 {}
T {Topology: SPDT HBT switches select between reference and delayed LC paths} 0 -670 0 0 0.3 0.3 {layer=7}
T {VCTRL_PS[1]: Bit1 (45 deg), VCTRL_PS[0]: Bit0 (22.5 deg)} 0 -650 0 0 0.3 0.3 {layer=7}
T {LC delay line: L=20.3pH, C=8.1fF per section (4 sections = 45deg @ 77GHz)} 0 -630 0 0 0.3 0.3 {layer=7}
T {Switch: npn13G2l Nx=4, Ron~5ohm, Roff~500ohm} 0 -610 0 0 0.3 0.3 {layer=7}
T {Insertion loss: ~1.5 dB/bit, compensated by PA (+10 dB)} 0 -590 0 0 0.3 0.3 {layer=7}
T {=== BIT 1: 45 deg ===} 50 -530 0 0 0.4 0.4 {layer=4}
C {sg13g2_pr/npn13G2l.sym} 150 -450 0 0 {name=QSW1A
model=npn13G2l
spiceprefix=X
Nx=4
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 150 -350 0 0 {name=QSW1B
model=npn13G2l
spiceprefix=X
Nx=4
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -450 0 0 {name=QSW2A
model=npn13G2l
spiceprefix=X
Nx=4
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -350 0 0 {name=QSW2B
model=npn13G2l
spiceprefix=X
Nx=4
El=2.5
selft=0}
C {devices/ind.sym} 270 -450 1 0 {name=Ld1 value=20.3p}
C {devices/ind.sym} 320 -450 1 0 {name=Ld2 value=20.3p}
C {devices/ind.sym} 370 -450 1 0 {name=Ld3 value=20.3p}
C {devices/ind.sym} 420 -450 1 0 {name=Ld4 value=20.3p}
C {devices/capa.sym} 280 -420 0 0 {name=Cd1 value=8.1f}
C {devices/capa.sym} 330 -420 0 0 {name=Cd2 value=8.1f}
C {devices/capa.sym} 380 -420 0 0 {name=Cd3 value=8.1f}
C {devices/capa.sym} 430 -420 0 0 {name=Cd4 value=8.1f}
T {=== BIT 0: 22.5 deg ===} 50 -280 0 0 0.4 0.4 {layer=4}
C {sg13g2_pr/npn13G2l.sym} 150 -200 0 0 {name=QSW3A
model=npn13G2l
spiceprefix=X
Nx=4
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 150 -100 0 0 {name=QSW3B
model=npn13G2l
spiceprefix=X
Nx=4
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -200 0 0 {name=QSW4A
model=npn13G2l
spiceprefix=X
Nx=4
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -100 0 0 {name=QSW4B
model=npn13G2l
spiceprefix=X
Nx=4
El=2.5
selft=0}
C {devices/ind.sym} 270 -200 1 0 {name=Ld5 value=10.2p}
C {devices/ind.sym} 320 -200 1 0 {name=Ld6 value=10.2p}
C {devices/ind.sym} 370 -200 1 0 {name=Ld7 value=10.2p}
C {devices/ind.sym} 420 -200 1 0 {name=Ld8 value=10.2p}
C {devices/capa.sym} 280 -170 0 0 {name=Cd5 value=4.0f}
C {devices/capa.sym} 330 -170 0 0 {name=Cd6 value=4.0f}
C {devices/capa.sym} 380 -170 0 0 {name=Cd7 value=4.0f}
C {devices/capa.sym} 430 -170 0 0 {name=Cd8 value=4.0f}
C {iopin.sym} 50 -450 0 1 {name=p1 lab=INP}
C {iopin.sym} 600 -450 0 0 {name=p2 lab=OUTP}
C {iopin.sym} 50 -200 0 1 {name=p3 lab=INN}
C {iopin.sym} 600 -200 0 0 {name=p4 lab=OUTN}
C {iopin.sym} 100 -530 0 1 {name=p5 lab=VCTRL_PS}
C {iopin.sym} 300 -50 0 0 {name=p6 lab=GND}
C {iopin.sym} 300 -530 0 0 {name=p7 lab=VCC}
C {iopin.sym} 350 -50 0 0 {name=p8 lab=sub!}
