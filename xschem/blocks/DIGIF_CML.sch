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
C {lab_pin.sym} 220 -280 3 0 {name=l1 sig_type=std_logic lab=DOUT_P}
C {lab_pin.sym} 180 -250 0 0 {name=l2 sig_type=std_logic lab=DIN_P}
C {lab_pin.sym} 220 -220 1 0 {name=l3 sig_type=std_logic lab=tail}
C {lab_pin.sym} 220 -250 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -280 3 0 {name=l5 sig_type=std_logic lab=DOUT_N}
C {lab_pin.sym} 420 -250 2 0 {name=l6 sig_type=std_logic lab=DIN_N}
C {lab_pin.sym} 380 -220 1 0 {name=l7 sig_type=std_logic lab=tail}
C {lab_pin.sym} 380 -250 2 0 {name=l8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 220 -380 3 0 {name=l9 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 220 -320 1 0 {name=l10 sig_type=std_logic lab=DOUT_P}
C {lab_pin.sym} 380 -380 3 0 {name=l11 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 380 -320 1 0 {name=l12 sig_type=std_logic lab=DOUT_N}
C {lab_pin.sym} 300 -190 3 0 {name=l13 sig_type=std_logic lab=tail}
C {lab_pin.sym} 300 -130 1 0 {name=l14 sig_type=std_logic lab=GND}
