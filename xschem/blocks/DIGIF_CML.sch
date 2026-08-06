v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {DIGIF — CML Buffer, 50ohm, 4mA} 0 -450 0 0 0.5 0.5 {}
C {sg13g2_pr/npn13G2l.sym} 200 -250 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=2
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 400 -250 0 1 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=2
El=2.5
selft=0}
C {devices/res.sym} 220 -350 0 0 {name=RT1
value=50}
C {devices/res.sym} 380 -350 0 0 {name=RT2
value=50}
C {devices/isource.sym} 300 -160 0 0 {name=ITAIL
value="DC 4m"}
C {iopin.sym} 80 -250 0 1 {name=p1 lab=DIN_P}
C {iopin.sym} 520 -250 0 0 {name=p2 lab=DIN_N}
C {iopin.sym} 80 -310 0 1 {name=p3 lab=DOUT_P}
C {iopin.sym} 520 -310 0 0 {name=p4 lab=DOUT_N}
C {iopin.sym} 300 -430 0 0 {name=p5 lab=VCC}
C {iopin.sym} 300 -70 0 0 {name=p6 lab=GND}
C {iopin.sym} 350 -70 0 0 {name=p7 lab=sub!}
C {lab_pin.sym} 220 -250 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -250 2 0 {name=l8 sig_type=std_logic lab=sub!}
N 80 -250 180 -250 {lab=DIN_P}
N 520 -250 420 -250 {lab=DIN_N}
N 220 -320 220 -280 {lab=DOUT_P}
N 80 -310 220 -310 {lab=DOUT_P}
N 380 -320 380 -280 {lab=DOUT_N}
N 520 -310 380 -310 {lab=DOUT_N}
N 220 -380 380 -380 {lab=VCC}
N 300 -430 300 -380 {lab=VCC}
N 300 -130 300 -70 {lab=GND}
N 220 -220 380 -220 {lab=tail}
N 300 -220 300 -190 {lab=tail}
