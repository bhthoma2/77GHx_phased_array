v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {StrongARM Comparator — 9T CMOS} 0 -750 0 0 0.5 0.5 {}
C {sg13g2_pr/sg13_lv_nmos.sym} 200 -200 0 0 {name=M1
l=200n
w=8u
ng=4
m=4
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 500 -200 0 1 {name=M2
l=200n
w=8u
ng=4
m=4
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 350 -50 0 0 {name=M9
l=200n
w=8u
ng=4
m=2
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 200 -380 0 0 {name=M5
l=200n
w=4u
ng=2
m=2
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 500 -380 0 1 {name=M6
l=200n
w=4u
ng=2
m=2
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 200 -550 0 0 {name=M3
l=200n
w=4u
ng=2
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 500 -550 0 1 {name=M4
l=200n
w=4u
ng=2
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 200 -680 0 0 {name=M7
l=200n
w=2u
ng=1
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 500 -680 0 1 {name=M8
l=200n
w=2u
ng=1
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 80 -200 0 1 {name=p1 lab=ainp}
C {iopin.sym} 620 -200 0 0 {name=p2 lab=ainn}
C {iopin.sym} 350 30 0 0 {name=p3 lab=clk}
C {iopin.sym} 80 -500 0 1 {name=p4 lab=doutp}
C {iopin.sym} 620 -500 0 0 {name=p5 lab=doutn}
C {iopin.sym} 350 -780 0 0 {name=p6 lab=vdd}
C {iopin.sym} 350 60 0 0 {name=p7 lab=vss}
C {lab_pin.sym} 220 -230 3 0 {name=l1 sig_type=std_logic lab=dn1}
C {lab_pin.sym} 180 -200 0 0 {name=l2 sig_type=std_logic lab=ainp}
C {lab_pin.sym} 220 -170 1 0 {name=l3 sig_type=std_logic lab=tail}
C {lab_pin.sym} 220 -200 0 0 {name=l4 sig_type=std_logic lab=vss}
C {lab_pin.sym} 480 -230 3 0 {name=l5 sig_type=std_logic lab=dn2}
C {lab_pin.sym} 520 -200 2 0 {name=l6 sig_type=std_logic lab=ainn}
C {lab_pin.sym} 480 -170 1 0 {name=l7 sig_type=std_logic lab=tail}
C {lab_pin.sym} 480 -200 2 0 {name=l8 sig_type=std_logic lab=vss}
C {lab_pin.sym} 370 -80 3 0 {name=l9 sig_type=std_logic lab=tail}
C {lab_pin.sym} 330 -50 0 0 {name=l10 sig_type=std_logic lab=clk}
C {lab_pin.sym} 370 -20 1 0 {name=l11 sig_type=std_logic lab=vss}
C {lab_pin.sym} 370 -50 0 0 {name=l12 sig_type=std_logic lab=vss}
C {lab_pin.sym} 220 -410 3 0 {name=l13 sig_type=std_logic lab=doutp}
C {lab_pin.sym} 180 -380 0 0 {name=l14 sig_type=std_logic lab=doutn}
C {lab_pin.sym} 220 -350 1 0 {name=l15 sig_type=std_logic lab=dn1}
C {lab_pin.sym} 220 -380 0 0 {name=l16 sig_type=std_logic lab=vss}
C {lab_pin.sym} 480 -410 3 0 {name=l17 sig_type=std_logic lab=doutn}
C {lab_pin.sym} 520 -380 2 0 {name=l18 sig_type=std_logic lab=doutp}
C {lab_pin.sym} 480 -350 1 0 {name=l19 sig_type=std_logic lab=dn2}
C {lab_pin.sym} 480 -380 2 0 {name=l20 sig_type=std_logic lab=vss}
C {lab_pin.sym} 220 -520 1 0 {name=l21 sig_type=std_logic lab=doutp}
C {lab_pin.sym} 180 -550 0 0 {name=l22 sig_type=std_logic lab=doutn}
C {lab_pin.sym} 220 -580 3 0 {name=l23 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 220 -550 0 0 {name=l24 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 480 -520 1 0 {name=l25 sig_type=std_logic lab=doutn}
C {lab_pin.sym} 520 -550 2 0 {name=l26 sig_type=std_logic lab=doutp}
C {lab_pin.sym} 480 -580 3 0 {name=l27 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 480 -550 2 0 {name=l28 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 220 -650 1 0 {name=l29 sig_type=std_logic lab=doutp}
C {lab_pin.sym} 180 -680 0 0 {name=l30 sig_type=std_logic lab=clk}
C {lab_pin.sym} 220 -710 3 0 {name=l31 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 220 -680 0 0 {name=l32 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 480 -650 1 0 {name=l33 sig_type=std_logic lab=doutn}
C {lab_pin.sym} 520 -680 2 0 {name=l34 sig_type=std_logic lab=clk}
C {lab_pin.sym} 480 -710 3 0 {name=l35 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 480 -680 2 0 {name=l36 sig_type=std_logic lab=vdd}
N 80 -200 80 -200 {lab=ainp}
N 620 -200 620 -200 {lab=ainn}
N 350 30 350 30 {lab=clk}
N 80 -500 80 -500 {lab=doutp}
N 620 -500 620 -500 {lab=doutn}
N 350 -780 350 -780 {lab=vdd}
N 350 60 350 60 {lab=vss}
