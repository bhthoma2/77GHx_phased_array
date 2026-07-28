v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {77 GHz VCO — LVS-Equivalent Schematic} 50 -700 0 0 0.5 0.5 {}
T {Physical implementation: SVaricap, rppd tail, CPW tank stubs} 50 -660 0 0 0.3 0.3 {layer=7}
T {Matches generate_vco_transistor.py layout for LVS} 50 -630 0 0 0.3 0.3 {layer=7}
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
C {sg13g2_pr/SVaricap.sym} 260 -420 0 0 {name=CV1
model=SVaricap
spiceprefix=X
w=0.6u
l=0.6u
m=1}
C {sg13g2_pr/SVaricap.sym} 340 -420 0 1 {name=CV2
model=SVaricap
spiceprefix=X
w=0.6u
l=0.6u
m=1}
C {sg13g2_pr/rppd.sym} 300 -120 0 0 {name=R1
model=rppd
spiceprefix=X
w=0.5u
l=5.0u
m=1
b=0}
C {sg13g2_pr/cap_cmim.sym} 450 -500 0 0 {name=Cdecap
model=cap_cmim
spiceprefix=X
W=7.0u
L=7.0u
m=1}
C {iopin.sym} 100 -550 0 1 {name=p1 lab=VCC}
C {iopin.sym} 300 -60 0 0 {name=p2 lab=GND}
C {iopin.sym} 140 -380 0 1 {name=p3 lab=OUTP}
C {iopin.sym} 460 -380 0 0 {name=p4 lab=OUTN}
C {iopin.sym} 300 -420 0 0 {name=p5 lab=VTUNE}
N 220 -550 380 -550 {lab=VCC}
N 100 -550 220 -550 {lab=VCC}
N 220 -380 260 -380 {lab=OUTP}
N 340 -380 380 -380 {lab=OUTN}
N 140 -380 220 -380 {lab=OUTP}
N 380 -380 460 -380 {lab=OUTN}
N 180 -300 180 -300 {lab=OUTN}
N 420 -300 420 -300 {lab=OUTP}
N 220 -270 220 -220 {lab=TAIL}
N 380 -270 380 -220 {lab=TAIL}
N 220 -220 380 -220 {lab=TAIL}
N 300 -220 300 -150 {lab=TAIL}
N 300 -90 300 -60 {lab=GND}
N 260 -450 260 -420 {lab=OUTP}
N 340 -450 340 -420 {lab=OUTN}
N 300 -420 300 -420 {lab=VTUNE}
N 220 -550 220 -380 {lab=VCC}
N 380 -550 380 -380 {lab=VCC}
N 450 -530 450 -550 {lab=VCC}
N 380 -550 450 -550 {lab=VCC}
N 450 -470 450 -60 {lab=GND}
N 300 -60 450 -60 {lab=GND}
C {lab_pin.sym} 180 -300 0 1 {name=p7 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 420 -300 0 0 {name=p8 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 300 -180 0 0 {name=p9 sig_type=std_logic lab=TAIL}