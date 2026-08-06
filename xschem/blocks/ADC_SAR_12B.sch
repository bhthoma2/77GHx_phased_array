v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {StrongARM Comparator — 9T CMOS} 0 -800 0 0 0.5 0.5 {}
N 80 -200 180 -200 {lab=ainp}
N 520 -200 620 -200 {lab=ainn}
N 220 -170 220 -130 {lab=tail}
N 370 -130 480 -130 {lab=tail}
N 480 -170 480 -130 {lab=tail}
N 370 -130 370 -80 {lab=tail}
N 220 -350 220 -230 {lab=dn1}
N 480 -350 480 -230 {lab=dn2}
N 220 -460 220 -410 {lab=doutp}
N 220 -520 230 -520 {lab=doutp}
N 230 -650 230 -520 {lab=doutp}
N 220 -650 230 -650 {lab=doutp}
N 480 -460 480 -410 {lab=doutn}
N 470 -520 480 -520 {lab=doutn}
N 470 -650 470 -520 {lab=doutn}
N 470 -650 480 -650 {lab=doutn}
N 80 -460 220 -460 {lab=doutp}
N 480 -460 620 -460 {lab=doutn}
N 210 -580 220 -580 {lab=vdd}
N 210 -710 210 -580 {lab=vdd}
N 210 -710 350 -710 {lab=vdd}
N 480 -580 490 -580 {lab=vdd}
N 490 -710 490 -580 {lab=vdd}
N 350 -710 490 -710 {lab=vdd}
N 350 -760 350 -710 {lab=vdd}
N 100 -50 330 -50 {lab=clk}
N 100 -680 100 -50 {lab=clk}
N 100 -680 180 -680 {lab=clk}
N 520 -680 560 -680 {lab=clk}
N 560 -680 560 -30 {lab=clk}
N 330 -30 560 -30 {lab=clk}
N 330 -50 330 -30 {lab=clk}
N 370 -20 370 30 {lab=vss}
N 350 30 370 30 {lab=vss}
N 350 30 350 60 {lab=vss}
N 220 -130 370 -130 {lab=tail}
N 220 -520 220 -460 {lab=doutp}
N 480 -520 480 -460 {lab=doutn}
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
C {iopin.sym} 100 -50 0 1 {name=p3 lab=clk}
C {iopin.sym} 80 -460 0 1 {name=p4 lab=doutp}
C {iopin.sym} 620 -460 0 0 {name=p5 lab=doutn}
C {iopin.sym} 350 -760 0 0 {name=p6 lab=vdd}
C {iopin.sym} 350 60 0 0 {name=p7 lab=vss}
C {lab_wire.sym} 520 -380 2 0 {name=lw1 sig_type=std_logic lab=doutp}
C {lab_wire.sym} 520 -550 2 0 {name=lw2 sig_type=std_logic lab=doutp}
C {lab_wire.sym} 180 -380 0 0 {name=lw3 sig_type=std_logic lab=doutn}
C {lab_wire.sym} 180 -550 0 0 {name=lw4 sig_type=std_logic lab=doutn}
C {lab_wire.sym} 220 -200 0 0 {name=lw5 sig_type=std_logic lab=vss}
C {lab_wire.sym} 480 -200 2 0 {name=lw6 sig_type=std_logic lab=vss}
C {lab_wire.sym} 220 -380 0 0 {name=lw7 sig_type=std_logic lab=vss}
C {lab_wire.sym} 480 -380 2 0 {name=lw8 sig_type=std_logic lab=vss}
C {lab_wire.sym} 370 -50 0 0 {name=lw9 sig_type=std_logic lab=vss}
C {lab_wire.sym} 220 -550 0 0 {name=lw10 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 480 -550 2 0 {name=lw11 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 220 -680 0 0 {name=lw12 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 480 -680 2 0 {name=lw13 sig_type=std_logic lab=vdd}
