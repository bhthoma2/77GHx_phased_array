v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {BIAS — Brokaw BGR, 1.17V} 0 -550 0 0 0.5 0.5 {}
N 220 -270 220 -230 {lab=e1}
N 320 -460 420 -460 {lab=VCC}
N 320 -530 320 -460 {lab=VCC}
N 200 -340 200 -330 {lab=c1}
N 200 -400 220 -400 {lab=c1}
N 200 -330 220 -330 {lab=c1}
N 180 -340 180 -300 {lab=c1}
N 180 -340 200 -340 {lab=c1}
N 200 -410 310 -410 {lab=c1}
N 440 -350 440 -330 {lab=c2}
N 420 -400 440 -400 {lab=c2}
N 420 -330 440 -330 {lab=c2}
N 380 -350 380 -300 {lab=c2}
N 380 -350 440 -350 {lab=c2}
N 440 -410 470 -410 {lab=c2}
N 550 -300 600 -300 {lab=VREF}
N 470 -350 470 -300 {lab=VREF}
N 550 -330 550 -300 {lab=VREF}
N 450 -80 550 -80 {lab=GND}
N 220 -80 450 -80 {lab=GND}
N 220 -170 220 -80 {lab=GND}
N 420 -270 450 -270 {lab=GND}
N 450 -270 450 -80 {lab=GND}
N 550 -270 550 -80 {lab=GND}
N 220 -460 320 -460 {lab=VCC}
N 200 -410 200 -400 {lab=c1}
N 200 -400 200 -340 {lab=c1}
N 440 -410 440 -400 {lab=c2}
N 310 -350 380 -350 {lab=c2}
N 440 -400 440 -350 {lab=c2}
N 470 -300 550 -300 {lab=VREF}
C {sg13g2_pr/npn13G2l.sym} 200 -300 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=1
El=2.5
selft=0}
C {sg13g2_pr/npn13G2l.sym} 400 -300 0 0 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=8
El=2.5
selft=0}
C {devices/res.sym} 220 -200 0 0 {name=R1
value=5.4k}
C {devices/res.sym} 550 -300 0 0 {name=R2
value=18k}
C {devices/res.sym} 310 -380 0 0 {name=Rfb
value=50}
C {devices/res.sym} 470 -380 0 0 {name=Rout
value=100}
C {devices/isource.sym} 220 -430 0 0 {name=I1
value="DC 200u"}
C {devices/isource.sym} 420 -430 0 0 {name=I2
value="DC 200u"}
C {iopin.sym} 600 -300 0 0 {name=p1 lab=VREF}
C {iopin.sym} 320 -530 0 0 {name=p2 lab=VCC}
C {iopin.sym} 320 -80 0 0 {name=p3 lab=GND}
C {iopin.sym} 370 -80 0 0 {name=p4 lab=sub!}
C {lab_pin.sym} 220 -300 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 420 -300 0 0 {name=l8 sig_type=std_logic lab=sub!}
