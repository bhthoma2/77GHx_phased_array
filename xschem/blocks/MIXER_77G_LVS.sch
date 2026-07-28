v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {77 GHz Mixer — LVS Equivalent} 50 -950 0 0 0.5 0.5 {}
T {Gilbert cell: Q20/Q21 gm, Q22-Q25 switch, Q26/Q27 bias} 50 -910 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 250 -300 0 0 {name=Q20
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 450 -300 0 1 {name=Q21
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 180 -550 0 0 {name=Q22
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 320 -550 0 1 {name=Q23
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 380 -550 0 0 {name=Q24
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 520 -550 0 1 {name=Q25
model=npn13G2l
spiceprefix=X
Nx=4
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 700 -200 0 0 {name=Q26
model=npn13G2l
spiceprefix=X
Nx=1
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 700 -100 0 0 {name=Q27
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
C {sg13g2_pr/rppd.sym} 700 -300 0 0 {name=R23
model=rppd
spiceprefix=X
w=3.0u
l=27.48u
m=1
b=0}
C {sg13g2_pr/rppd.sym} 700 -400 0 0 {name=R24
model=rppd
spiceprefix=X
w=3.0u
l=27.48u
m=1
b=0}
C {sg13g2_pr/cap_cmim.sym} 100 -480 0 0 {name=C37
model=cap_cmim
spiceprefix=X
W=5.0u
L=5.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 600 -480 0 0 {name=C38
model=cap_cmim
spiceprefix=X
W=5.0u
L=5.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 150 -250 0 0 {name=C39
model=cap_cmim
spiceprefix=X
W=4.0u
L=4.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 550 -250 0 0 {name=C40
model=cap_cmim
spiceprefix=X
W=4.0u
L=4.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 850 -800 0 0 {name=C41
model=cap_cmim
spiceprefix=X
W=30.0u
L=30.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 850 -720 0 0 {name=C42
model=cap_cmim
spiceprefix=X
W=30.0u
L=30.0u
m=1}
C {sg13g2_pr/cap_cmim.sym} 850 -640 0 0 {name=C43
model=cap_cmim
spiceprefix=X
W=30.0u
L=30.0u
m=1}
C {iopin.sym} 350 -860 0 0 {name=p1 lab=2V4}
C {iopin.sym} 350 -50 0 0 {name=p2 lab=GND}
C {iopin.sym} 50 -300 0 1 {name=p3 lab=RFP}
C {iopin.sym} 650 -300 0 0 {name=p4 lab=RFN}
C {iopin.sym} 50 -550 0 1 {name=p5 lab=LOP}
C {iopin.sym} 650 -550 0 0 {name=p6 lab=LON}
C {iopin.sym} 50 -750 0 1 {name=p7 lab=IFP}
C {iopin.sym} 650 -750 0 0 {name=p8 lab=IFN}
N 270 -270 270 -200 {lab=GND}
N 430 -270 430 -200 {lab=GND}
N 270 -200 430 -200 {lab=GND}
N 350 -200 350 -50 {lab=GND}
N 270 -330 270 -520 {lab=ELOL}
N 430 -330 430 -520 {lab=ELOR}
N 200 -520 300 -520 {lab=ELOL}
N 400 -520 500 -520 {lab=ELOR}
N 200 -580 200 -670 {lab=IFP}
N 200 -730 200 -860 {lab=2V4}
N 500 -730 500 -860 {lab=2V4}
N 200 -860 850 -860 {lab=2V4}
N 200 -670 200 -750 {lab=IFP}
N 50 -750 200 -750 {lab=IFP}
N 500 -670 500 -750 {lab=IFN}
N 500 -750 650 -750 {lab=IFN}
N 700 -330 700 -860 {lab=2V4}
N 720 -170 720 -130 {lab=BIAS_MID}
N 720 -70 720 -50 {lab=GND}
N 350 -50 720 -50 {lab=GND}
N 700 -270 700 -230 {lab=BIAS}
N 720 -50 850 -50 {lab=GND}
N 50 -300 150 -300 {lab=RFP}
N 150 -300 150 -280 {lab=RFP}
N 550 -300 550 -280 {lab=RFN}
N 550 -300 650 -300 {lab=RFN}
N 50 -550 100 -550 {lab=LOP}
N 100 -550 100 -510 {lab=LOP}
N 600 -550 600 -510 {lab=LON}
N 600 -550 650 -550 {lab=LON}
C {lab_pin.sym} 230 -300 0 1 {name=p9 sig_type=std_logic lab=RFP_I}
C {lab_pin.sym} 470 -300 0 0 {name=p10 sig_type=std_logic lab=RFN_I}
C {lab_pin.sym} 150 -220 0 0 {name=p11 sig_type=std_logic lab=RFP_I}
C {lab_pin.sym} 550 -220 0 0 {name=p12 sig_type=std_logic lab=RFN_I}
C {lab_pin.sym} 150 -280 0 0 {name=p13 sig_type=std_logic lab=RFP}
C {lab_pin.sym} 100 -450 0 0 {name=p16 sig_type=std_logic lab=LOP_I}
C {lab_pin.sym} 600 -450 0 0 {name=p17 sig_type=std_logic lab=LON_I}
C {lab_pin.sym} 160 -550 0 1 {name=p18 sig_type=std_logic lab=LOP_I}
C {lab_pin.sym} 540 -550 0 0 {name=p19 sig_type=std_logic lab=LON_I}
C {lab_pin.sym} 340 -550 0 0 {name=p20 sig_type=std_logic lab=LON_I}
C {lab_pin.sym} 360 -550 0 0 {name=p21 sig_type=std_logic lab=LOP_I}
C {lab_pin.sym} 300 -580 0 0 {name=p22 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 400 -580 0 0 {name=p23 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 500 -580 0 0 {name=p24 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 500 -670 0 0 {name=p30 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 680 -200 0 1 {name=p25 sig_type=std_logic lab=BIAS}
C {lab_pin.sym} 680 -100 0 1 {name=p26 sig_type=std_logic lab=BIAS_MID}
C {lab_pin.sym} 720 -230 0 0 {name=p27 sig_type=std_logic lab=BIAS}
C {lab_pin.sym} 700 -430 0 0 {name=p40 sig_type=std_logic lab=2V4}
C {lab_pin.sym} 700 -370 0 0 {name=p41 sig_type=std_logic lab=BIAS}
C {lab_pin.sym} 720 -130 0 0 {name=p31 sig_type=std_logic lab=BIAS_MID}
C {lab_pin.sym} 270 -520 0 0 {name=p28 sig_type=std_logic lab=ELOL}
C {lab_pin.sym} 430 -520 0 0 {name=p29 sig_type=std_logic lab=ELOR}
C {lab_pin.sym} 850 -830 0 0 {name=p32 sig_type=std_logic lab=2V4}
C {lab_pin.sym} 850 -770 0 0 {name=p33 sig_type=std_logic lab=GND}
C {lab_pin.sym} 850 -750 0 0 {name=p34 sig_type=std_logic lab=2V4}
C {lab_pin.sym} 850 -690 0 0 {name=p35 sig_type=std_logic lab=GND}
C {lab_pin.sym} 850 -670 0 0 {name=p36 sig_type=std_logic lab=2V4}
C {lab_pin.sym} 850 -610 0 0 {name=p37 sig_type=std_logic lab=GND}
C {lab_pin.sym} 100 -510 0 0 {name=p38 sig_type=std_logic lab=LOP}
C {lab_pin.sym} 600 -510 0 0 {name=p39 sig_type=std_logic lab=LON}
