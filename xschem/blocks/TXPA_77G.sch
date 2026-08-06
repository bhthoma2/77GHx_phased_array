v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {77 GHz TL-Matched Power Amplifier} 50 -900 0 0 0.5 0.5 {}
T {Pout~0dBm diff, Nx=8, TL matching, Ic=101mA} 50 -860 0 0 0.3 0.3 {layer=7}
T {Architecture: Common-emitter cascode with TL input/output matching} 50 -830 0 0 0.3 0.3 {layer=7}
N 220 -780 220 -770 {lab=VCC}
N 480 -780 480 -770 {lab=VCC}
N 50 -780 220 -780 {lab=VCC}
N 220 -780 480 -780 {lab=VCC}
N 220 -680 250 -680 {lab=COL_P}
N 250 -680 250 -530 {lab=COL_P}
N 250 -530 220 -530 {lab=COL_P}
N 480 -680 450 -680 {lab=COL_N}
N 450 -680 450 -530 {lab=COL_N}
N 450 -530 480 -530 {lab=COL_N}
N 220 -620 200 -620 {lab=OUTP}
N 200 -620 200 -710 {lab=OUTP}
N 200 -710 220 -710 {lab=OUTP}
N 480 -620 500 -620 {lab=OUTN}
N 500 -620 500 -710 {lab=OUTN}
N 500 -710 480 -710 {lab=OUTN}
N 220 -470 220 -330 {lab=MID_P}
N 480 -470 480 -330 {lab=MID_N}
N 220 -270 220 -210 {lab=EM_P}
N 480 -270 480 -210 {lab=EM_N}
N 220 -150 220 -100 {lab=GND}
N 480 -150 480 -100 {lab=GND}
N 350 -100 480 -100 {lab=GND}
N 350 -100 350 -80 {lab=GND}
N 50 -300 120 -300 {lab=INP}
N 150 -300 180 -300 {lab=INP}
N 580 -300 650 -300 {lab=INN}
N 520 -300 550 -300 {lab=INN}
N 350 -500 350 -460 {lab=VBIAS_CB}
N 350 -430 350 -100 {lab=GND}
N 220 -100 350 -100 {lab=GND}
C {sg13g2_pr/npn13G2l.sym} 200 -300 0 0 {name=Q1_CE
model=npn13G2l
spiceprefix=X
Nx=8
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -300 0 1 {name=Q2_CE
model=npn13G2l
spiceprefix=X
Nx=8
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 200 -500 0 0 {name=Q3_CB
model=npn13G2l
spiceprefix=X
Nx=8
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 500 -500 0 1 {name=Q4_CB
model=npn13G2l
spiceprefix=X
Nx=8
m=1
El=2.5
selft=0}
C {YTRANSLINE.sym} 120 -300 2 0 {name=TL_INP R=22.16k L=445.9n C=61.5p len=97u lumps=50 Z0=85}
C {YTRANSLINE.sym} 580 -300 2 0 {name=TL_INN R=22.16k L=445.9n C=61.5p len=97u lumps=50 Z0=85}
C {YTRANSLINE.sym} 220 -650 1 0 {name=TL_OUTP R=22.16k L=445.9n C=61.5p len=210u lumps=50 Z0=85}
C {YTRANSLINE.sym} 480 -650 3 1 {name=TL_OUTN R=22.16k L=445.9n C=61.5p len=210u lumps=50 Z0=85}
C {YTRANSLINE.sym} 220 -180 1 0 {name=TL_DEG_P R=22.16k L=445.9n C=61.5p len=58u lumps=50 Z0=85}
C {YTRANSLINE.sym} 480 -180 3 1 {name=TL_DEG_N R=22.16k L=445.9n C=61.5p len=58u lumps=50 Z0=85}
C {sg13g2_pr/rppd.sym} 350 -460 0 0 {name=RB_CB
w=3e-6
l=18.23e-6
model=rppd
spiceprefix=X}
C {devices/capa.sym} 220 -740 0 0 {name=CDC_P
value=500f}
C {devices/capa.sym} 480 -740 0 0 {name=CDC_N
value=500f}
C {iopin.sym} 50 -780 0 1 {name=p1 lab=VCC}
C {iopin.sym} 350 -80 0 0 {name=p2 lab=GND}
C {iopin.sym} 50 -300 0 1 {name=p3 lab=INP}
C {iopin.sym} 650 -300 0 0 {name=p4 lab=INN}
C {iopin.sym} 220 -780 0 0 {name=p5 lab=OUTP}
C {iopin.sym} 480 -780 0 0 {name=p6 lab=OUTN}
C {iopin.sym} 350 -500 0 0 {name=p7 lab=VBIAS_CB}
C {iopin.sym} 50 -500 0 1 {name=p8 lab=sub|}
C {lab_pin.sym} 180 -500 0 1 {name=p9 sig_type=std_logic lab=VBIAS_CB}
C {lab_pin.sym} 520 -500 0 0 {name=p10 sig_type=std_logic lab=VBIAS_CB}
C {lab_pin.sym} 220 -300 0 0 {name=p11 sig_type=std_logic lab=sub|}
C {lab_pin.sym} 480 -300 0 0 {name=p12 sig_type=std_logic lab=sub|}
C {lab_pin.sym} 220 -500 0 0 {name=p13 sig_type=std_logic lab=sub|}
C {lab_pin.sym} 480 -500 0 0 {name=p14 sig_type=std_logic lab=sub|}
