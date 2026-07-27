v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Level Shifter — Emitter Follower, -0.85V CM shift} 0 -400 0 0 0.4 0.4 {}
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
C {devices/isource.sym} 220 -130 0 0 {name=IEE1
value="DC 2m"}
C {devices/isource.sym} 380 -130 0 0 {name=IEE2
value="DC 2m"}
C {iopin.sym} 80 -250 0 1 {name=p1 lab=INP}
C {iopin.sym} 520 -250 0 0 {name=p2 lab=INN}
C {iopin.sym} 80 -190 0 1 {name=p3 lab=OUTP}
C {iopin.sym} 520 -190 0 0 {name=p4 lab=OUTN}
C {iopin.sym} 300 -340 0 0 {name=p5 lab=VCC}
C {iopin.sym} 300 -30 0 0 {name=p6 lab=GND}
C {iopin.sym} 350 -30 0 0 {name=p7 lab=sub!}
C {lab_pin.sym} 220 -280 3 0 {name=l1 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 180 -250 0 0 {name=l2 sig_type=std_logic lab=INP}
C {lab_pin.sym} 220 -220 1 0 {name=l3 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 220 -250 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 380 -280 3 0 {name=l5 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 420 -250 2 0 {name=l6 sig_type=std_logic lab=INN}
C {lab_pin.sym} 380 -220 1 0 {name=l7 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 380 -250 2 0 {name=l8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 220 -160 3 0 {name=l9 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 220 -100 1 0 {name=l10 sig_type=std_logic lab=GND}
C {lab_pin.sym} 380 -160 3 0 {name=l11 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 380 -100 1 0 {name=l12 sig_type=std_logic lab=GND}
