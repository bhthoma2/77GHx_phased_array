v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {77 GHz Injection-Locked Frequency Divider (div-by-2)} 50 -800 0 0 0.5 0.5 {}
T {f_in=77GHz, f_out=38.5GHz, TL-stub resonators} 50 -760 0 0 0.3 0.3 {layer=7}
T {Cross-coupled pair + tail injection topology} 50 -730 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 200 -350 0 0 {name=Q1_XC
model=npn13G2l
spiceprefix=X
Nx=2
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 450 -350 0 1 {name=Q2_XC
model=npn13G2l
spiceprefix=X
Nx=2
m=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 325 -180 0 0 {name=Q_INJ
model=npn13G2l
spiceprefix=X
Nx=2
m=1
El=2.5
selft=0}
C {YTRANSLINE.sym} 220 -550 1 0 {name=TL_STUB_P R=22.16k L=445.9n C=61.5p len=280u lumps=50 Z0=85}
C {YTRANSLINE.sym} 430 -550 3 1 {name=TL_STUB_N R=22.16k L=445.9n C=61.5p len=280u lumps=50 Z0=85}
C {devices/isource.sym} 345 -80 0 0 {name=ITAIL
value="DC 3m"}
C {devices/capa.sym} 270 -180 3 0 {name=C_INJ
value=100f}
C {iopin.sym} 100 -650 0 1 {name=p1 lab=VCC}
C {iopin.sym} 345 -30 0 0 {name=p2 lab=GND}
C {iopin.sym} 140 -450 0 1 {name=p3 lab=OUTP}
C {iopin.sym} 510 -450 0 0 {name=p4 lab=OUTN}
C {iopin.sym} 200 -180 0 1 {name=p5 lab=INJ_P}
C {iopin.sym} 100 -350 0 1 {name=p6 lab=sub|}
N 220 -650 220 -580 {lab=VCC}
N 430 -650 430 -580 {lab=VCC}
N 100 -650 220 -650 {lab=VCC}
N 220 -650 430 -650 {lab=VCC}
N 220 -520 220 -450 {lab=OUTP}
N 430 -520 430 -450 {lab=OUTN}
N 140 -450 220 -450 {lab=OUTP}
N 430 -450 510 -450 {lab=OUTN}
N 220 -450 220 -380 {lab=OUTP}
N 430 -450 430 -380 {lab=OUTN}
N 180 -350 180 -350 {lab=OUTN}
N 470 -350 470 -350 {lab=OUTP}
N 220 -320 220 -260 {lab=TAIL_XC}
N 430 -320 430 -260 {lab=TAIL_XC}
N 220 -260 430 -260 {lab=TAIL_XC}
N 345 -260 345 -210 {lab=TAIL_XC}
N 345 -150 345 -110 {lab=TAIL_INJ}
N 345 -50 345 -30 {lab=GND}
N 200 -180 240 -180 {lab=INJ_P}
N 300 -180 305 -180 {lab=INJ_INT}
N 220 -350 220 -350 {lab=sub|}
N 430 -350 430 -350 {lab=sub|}
N 345 -180 345 -180 {lab=sub|}
C {lab_pin.sym} 180 -350 0 1 {name=p7 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 470 -350 0 0 {name=p8 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 220 -350 0 0 {name=p9 sig_type=std_logic lab=sub|}
C {lab_pin.sym} 430 -350 0 0 {name=p10 sig_type=std_logic lab=sub|}
C {lab_pin.sym} 345 -180 0 0 {name=p11 sig_type=std_logic lab=sub|}
