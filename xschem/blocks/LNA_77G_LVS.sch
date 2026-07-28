v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {77 GHz LNA — LVS Equivalent} 50 -1050 0 0 0.5 0.5 {}
T {Diff cascode: Q33/Q34 input, Q35/Q36 cascode, Q37 bias gen} 50 -1010 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 250 -400 0 0 {name=Q33
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 450 -400 0 1 {name=Q34
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 250 -600 0 0 {name=Q35
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 450 -600 0 1 {name=Q36
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 750 -300 0 0 {name=Q37
model=npn13G2l
spiceprefix=X
Nx=1
m=1
El=2.5
selft=0}
C {sg13g2_pr/rppd.sym} 350 -300 0 0 {name=R29
model=rppd
spiceprefix=X
w=7.0u
l=38.8u
m=4
b=0}
C {sg13g2_pr/rppd.sym} 650 -700 0 0 {name=R30
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
C {sg13g2_pr/rppd.sym} 750 -430 0 0 {name=R32
model=rppd
spiceprefix=X
w=3.0u
l=18.23u
m=2
b=0}
C {sg13g2_pr/rppd.sym} 770 -200 0 0 {name=R33
model=rppd
spiceprefix=X
w=2.5u
l=10.53u
m=14
b=0}
C {sg13g2_pr/cap_cmim.sym} 200 -370 1 0 {name=C53
model=cap_cmim
spiceprefix=X
W=6.0u
L=6.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 500 -370 1 1 {name=C54
model=cap_cmim
spiceprefix=X
W=6.0u
L=6.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 270 -690 0 0 {name=C55
model=cap_cmim
spiceprefix=X
W=4.0u
L=4.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 430 -690 0 0 {name=C56
model=cap_cmim
spiceprefix=X
W=4.0u
L=4.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 900 -800 0 0 {name=C57
model=cap_cmim
spiceprefix=X
W=100.0u
L=15.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 900 -700 0 0 {name=C58
model=cap_cmim
spiceprefix=X
W=100.0u
L=20.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 900 -600 0 0 {name=C59
model=cap_cmim
spiceprefix=X
W=100.0u
L=20.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 900 -500 0 0 {name=C60
model=cap_cmim
spiceprefix=X
W=100.0u
L=15.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 900 -400 0 0 {name=C61
model=cap_cmim
spiceprefix=X
W=100.0u
L=15.0u
m=1}
C {iopin.sym} 350 -920 0 0 {name=p1 lab=2V4}
C {iopin.sym} 350 -50 0 0 {name=p2 lab=GND}
C {iopin.sym} 50 -400 0 1 {name=p3 lab=INP}
C {iopin.sym} 650 -400 0 0 {name=p4 lab=INN}
C {iopin.sym} 50 -780 0 1 {name=p5 lab=OUTP}
C {iopin.sym} 650 -780 0 0 {name=p6 lab=OUTN}
C {iopin.sym} 750 -670 0 0 {name=p7 lab=B35&36}
C {iopin.sym} 650 -300 0 1 {name=p8 lab=BIAS6}
N 50 -400 170 -400 {lab=INP}
N 170 -400 170 -370 {lab=INP}
N 530 -400 530 -370 {lab=INN}
N 530 -400 650 -400 {lab=INN}
N 230 -370 230 -400 {lab=INP}
N 470 -370 470 -400 {lab=INN}
N 270 -370 270 -350 {lab=TAIL}
N 430 -370 430 -350 {lab=TAIL}
N 270 -350 430 -350 {lab=TAIL}
N 350 -350 350 -330 {lab=TAIL}
N 350 -270 350 -100 {lab=GND}
N 350 -100 350 -50 {lab=GND}
N 270 -430 270 -570 {lab=MIDL}
N 430 -430 430 -570 {lab=MIDR}
N 270 -630 270 -660 {lab=OUTP_I}
N 430 -630 430 -660 {lab=OUTN_I}
N 270 -720 270 -780 {lab=OUTP}
N 50 -780 270 -780 {lab=OUTP}
N 430 -720 430 -780 {lab=OUTN}
N 430 -780 650 -780 {lab=OUTN}
N 350 -920 350 -880 {lab=2V4}
N 350 -880 900 -880 {lab=2V4}
N 650 -730 650 -880 {lab=2V4}
N 650 -670 650 -630 {lab=B35&36}
N 650 -570 650 -100 {lab=GND}
N 350 -100 650 -100 {lab=GND}
N 650 -100 900 -100 {lab=GND}
N 650 -670 750 -670 {lab=B35&36}
N 900 -830 900 -880 {lab=2V4}
N 900 -770 900 -730 {lab=GND}
N 900 -670 900 -630 {lab=GND}
N 900 -570 900 -530 {lab=GND}
N 900 -470 900 -430 {lab=GND}
N 900 -370 900 -100 {lab=GND}
N 650 -300 730 -300 {lab=BIAS6}
N 770 -330 770 -300 {lab=BIAS6}
N 770 -300 730 -300 {lab=BIAS6}
N 770 -270 770 -230 {lab=BIAS6_E}
N 770 -170 770 -100 {lab=GND}
N 770 -100 900 -100 {lab=GND}
N 750 -460 750 -400 {lab=BIAS6}
N 750 -400 770 -400 {lab=BIAS6}
N 770 -400 770 -330 {lab=BIAS6}
C {lab_pin.sym} 230 -600 0 1 {name=p9 sig_type=std_logic lab=B35&36}
C {lab_pin.sym} 470 -600 0 0 {name=p10 sig_type=std_logic lab=B35&36}
C {lab_pin.sym} 750 -460 0 0 {name=p14 sig_type=std_logic lab=2V4}
