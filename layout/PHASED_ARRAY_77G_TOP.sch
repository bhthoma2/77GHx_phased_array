v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
L 7 -30 -920 310 -920 {}
L 7 -30 -920 -30 -680 {}
L 7 -30 -680 310 -680 {}
L 7 310 -920 310 -680 {}
L 7 700 -620 700 -280 {}
L 7 700 -620 1100 -620 {}
L 7 1100 -620 1100 -280 {}
L 7 700 -280 1100 -280 {}
L 7 -750 -620 -750 -280 {}
L 7 -750 -620 -350 -620 {}
L 7 -350 -620 -350 -280 {}
L 7 -750 -280 -350 -280 {}
L 7 250 -200 250 200 {}
L 7 250 -200 780 -200 {}
L 7 780 -200 780 200 {}
L 7 250 200 780 200 {}
L 7 -100 300 -100 650 {}
L 7 -100 300 300 300 {}
L 7 300 300 300 650 {}
L 7 -100 650 300 650 {}
L 7 350 -900 350 -680 {}
L 7 350 -900 750 -900 {}
L 7 750 -900 750 -680 {}
L 7 350 -680 750 -680 {}
T {PHASED_ARRAY_77G_TOP} -30 -1000 0 0 0.6 0.6 {}
T {VCO} 20 -910 0 0 0.3 0.3 {layer=7}
T {TXPA - Diff Cascode} 750 -610 0 0 0.3 0.3 {layer=7}
T {LNA - Diff Cascode} -700 -610 0 0 0.3 0.3 {layer=7}
T {MIXER - Gilbert Cell} 300 -190 0 0 0.3 0.3 {layer=7}
T {ILFD - Inj-Locked Div} -50 310 0 0 0.3 0.3 {layer=7}
T {BIAS NETWORK} 400 -890 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 80 -800 0 0 {name=Q49
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 200 -800 0 1 {name=Q50
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/rppd.sym} 140 -720 0 0 {name=R81
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {sg13g2_pr/sg13_svaricap.sym} 60 -870 0 1 {name=CVAR1
model=sg13_hv_svaricap
spiceprefix=X
w=3.74e-6
l=0.3e-6
Nx=1}
C {sg13g2_pr/sg13_svaricap.sym} 220 -870 0 0 {name=CVAR2
model=sg13_hv_svaricap
spiceprefix=X
w=3.74e-6
l=0.3e-6
Nx=1}
C {sg13g2_pr/npn13G2l.sym} 820 -420 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=8
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 980 -420 0 1 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=8
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 820 -540 0 0 {name=Q25
model=npn13G2l
spiceprefix=X
Nx=8
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 980 -540 0 1 {name=Q26
model=npn13G2l
spiceprefix=X
Nx=8
El=1.0}
C {sg13g2_pr/npn13G2l.sym} -600 -420 0 0 {name=Q45
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} -500 -420 0 1 {name=Q46
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} -600 -540 0 0 {name=Q61
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} -500 -540 0 1 {name=Q62
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 400 -40 0 0 {name=Q41
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 620 -40 0 1 {name=Q42
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 370 -140 0 0 {name=Q65
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 490 -140 0 1 {name=Q66
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 530 -140 0 0 {name=Q67
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 650 -140 0 1 {name=Q68
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 20 420 0 0 {name=Q21
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 180 420 0 1 {name=Q22
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 20 540 0 0 {name=Q11
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 180 540 0 1 {name=Q12
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/rppd.sym} 400 -800 0 0 {name=R77
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {sg13g2_pr/rppd.sym} 470 -800 0 0 {name=R78
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {sg13g2_pr/rppd.sym} 540 -800 0 0 {name=R79
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {sg13g2_pr/rppd.sym} 610 -800 0 0 {name=R80
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {sg13g2_pr/rppd.sym} 680 -800 0 0 {name=R82
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {sg13g2_pr/rppd.sym} 400 -720 0 0 {name=R83
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {sg13g2_pr/cap_cmim.sym} 500 -720 0 0 {name=C84
w=6.99e-6
l=6.99e-6
model=cap_cmim
spiceprefix=X
m=1}
C {sg13g2_pr/cap_cmim.sym} 570 -720 0 0 {name=C85
w=6.99e-6
l=6.99e-6
model=cap_cmim
spiceprefix=X
m=1}
C {sg13g2_pr/cap_cmim.sym} 640 -720 0 0 {name=C86
w=6.99e-6
l=6.99e-6
model=cap_cmim
spiceprefix=X
m=1}
N 100 -830 100 -830 {lab=OUTP}
N 180 -830 180 -830 {lab=OUTN}
N 60 -800 60 -800 {lab=OUTN}
N 220 -800 220 -800 {lab=OUTP}
N 100 -800 100 -800 {lab=sub!}
N 180 -800 180 -800 {lab=sub!}
N 100 -770 100 -750 {lab=VCO_TAIL}
N 180 -770 180 -750 {lab=VCO_TAIL}
N 100 -750 180 -750 {lab=VCO_TAIL}
N 140 -750 140 -690 {lab=VCO_TAIL}
N 20 -870 20 -870 {lab=G2}
N 260 -870 260 -870 {lab=G2_1}
N 60 -900 60 -900 {lab=OUTP}
N 220 -900 220 -900 {lab=OUTP}
N 60 -840 60 -840 {lab=sub!}
N 220 -840 220 -840 {lab=sub!}
N 100 -870 100 -870 {lab=OUTP}
N 180 -870 180 -870 {lab=G1}
N 840 -450 840 -510 {lab=TXP_MID}
N 960 -450 960 -510 {lab=TXN_MID}
N 840 -570 840 -600 {lab=ANT_TX}
N 960 -570 960 -600 {lab=ANT_TX}
N 840 -600 960 -600 {lab=ANT_TX}
N 800 -540 800 -540 {lab=VCB}
N 1000 -540 1000 -540 {lab=VCB}
N 800 -420 800 -420 {lab=OUTP}
N 1000 -420 1000 -420 {lab=OUTN}
N 840 -390 960 -390 {lab=TX_TAIL}
N 900 -390 900 -340 {lab=TX_TAIL}
N -580 -450 -580 -510 {lab=LNA_MIDP}
N -520 -450 -520 -510 {lab=LNA_MIDN}
N -580 -570 -580 -600 {lab=RF_P}
N -520 -570 -520 -600 {lab=RF_N}
N -620 -540 -620 -540 {lab=LNA_INP}
N -480 -540 -480 -540 {lab=LNA_INP}
N -620 -420 -620 -420 {lab=LNA_VCB}
N -480 -420 -480 -420 {lab=LNA_VCB2}
N -580 -390 -520 -390 {lab=LNA_TAIL}
N -550 -390 -550 -340 {lab=LNA_TAIL}
N 420 -10 600 -10 {lab=MIX_TAIL}
N 510 -10 510 30 {lab=MIX_TAIL}
N 420 -70 420 -110 {lab=MIX_MIDP}
N 600 -70 600 -110 {lab=MIX_MIDN}
N 390 -110 470 -110 {lab=MIX_MIDP}
N 550 -110 630 -110 {lab=MIX_MIDN}
N 390 -170 390 -185 {lab=IFP}
N 470 -170 470 -185 {lab=IFN}
N 550 -170 550 -185 {lab=IFN}
N 630 -170 630 -185 {lab=IFP}
N 350 -140 350 -140 {lab=OUTP}
N 510 -140 510 -140 {lab=OUTN}
N 670 -140 670 -140 {lab=OUTP}
N 380 -40 380 -40 {lab=RF_P}
N 640 -40 640 -40 {lab=RF_N}
N 40 450 40 510 {lab=ILFD_MID}
N 160 450 160 510 {lab=ILFD_MID}
N 40 450 160 450 {lab=ILFD_MID}
N 40 570 160 570 {lab=ILFD_TAIL}
N 100 570 100 620 {lab=ILFD_TAIL}
N 40 390 40 370 {lab=DIV_P}
N 40 370 200 370 {lab=DIV_P}
N 200 370 200 420 {lab=DIV_P}
N 160 390 160 350 {lab=DIV_N}
N 160 350 0 350 {lab=DIV_N}
N 0 350 0 420 {lab=DIV_N}
N 0 540 0 540 {lab=OUTP}
N 200 540 200 540 {lab=OUTN}
N 140 -690 140 -690 {lab=VCO_TAIL}
C {devices/iopin.sym} 180 -870 0 1 {name=p1 lab=G1}
C {devices/iopin.sym} 100 -830 0 1 {name=p2 lab=OUTP}
C {devices/iopin.sym} 20 -870 0 1 {name=p3 lab=G2}
C {devices/iopin.sym} 260 -870 0 0 {name=p4 lab=G2_1}
C {lab_pin.sym} 60 -800 0 1 {name=l30 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 220 -800 0 0 {name=l31 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 100 -800 0 0 {name=l32 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 180 -800 0 0 {name=l33 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 60 -840 0 1 {name=l28 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 220 -840 0 0 {name=l29 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 60 -900 0 1 {name=l52 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 220 -900 0 0 {name=l53 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 800 -540 0 1 {name=l6 sig_type=std_logic lab=VCB}
C {lab_pin.sym} 1000 -540 0 0 {name=l7 sig_type=std_logic lab=VCB}
C {lab_pin.sym} -620 -420 0 1 {name=l8 sig_type=std_logic lab=LNA_VCB}
C {lab_pin.sym} -480 -420 0 0 {name=l9 sig_type=std_logic lab=LNA_VCB2}
C {lab_pin.sym} 800 -420 0 1 {name=l10 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 1000 -420 0 0 {name=l11 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 350 -140 0 1 {name=l12 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 510 -140 0 0 {name=l13 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 670 -140 0 0 {name=l15 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 0 540 0 1 {name=l16 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 200 540 0 0 {name=l17 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 380 -40 0 1 {name=l18 sig_type=std_logic lab=RF_P}
C {lab_pin.sym} 640 -40 0 0 {name=l19 sig_type=std_logic lab=RF_N}
C {lab_pin.sym} -580 -600 0 1 {name=l20 sig_type=std_logic lab=RF_P}
C {lab_pin.sym} -520 -600 0 0 {name=l21 sig_type=std_logic lab=RF_N}
C {lab_pin.sym} -620 -540 0 1 {name=l22 sig_type=std_logic lab=LNA_INP}
C {lab_pin.sym} -480 -540 0 0 {name=l23 sig_type=std_logic lab=LNA_INP}
C {lab_pin.sym} 840 -420 0 0 {name=l34 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 960 -420 0 0 {name=l35 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 840 -540 0 0 {name=l36 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 960 -540 0 0 {name=l37 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -580 -420 0 0 {name=l38 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -520 -420 0 0 {name=l39 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -580 -540 0 0 {name=l40 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -520 -540 0 0 {name=l41 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 420 -40 0 0 {name=l42 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 600 -40 0 0 {name=l43 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 390 -140 0 0 {name=l44 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 470 -140 0 0 {name=l45 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 550 -140 0 0 {name=l46 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 630 -140 0 0 {name=l47 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 40 420 0 0 {name=l48 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 160 420 0 0 {name=l49 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 40 540 0 0 {name=l50 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 160 540 0 0 {name=l51 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 140 -690 3 0 {name=l54 sig_type=std_logic lab=VCO_DECAP}
C {lab_pin.sym} 570 -690 3 0 {name=l55 sig_type=std_logic lab=VCO_DECAP}
C {lab_pin.sym} 500 -690 3 0 {name=l56 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 570 -750 0 0 {name=l57 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 500 -750 0 0 {name=l58 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 640 -690 3 0 {name=l59 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 640 -750 0 0 {name=l60 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 400 -770 0 0 {name=l61 sig_type=std_logic lab=BIAS_R77_P}
C {lab_pin.sym} 400 -830 0 0 {name=l62 sig_type=std_logic lab=BIAS_R77_M}
C {lab_pin.sym} 470 -770 0 0 {name=l63 sig_type=std_logic lab=BIAS_R78_P}
C {lab_pin.sym} 470 -830 0 0 {name=l64 sig_type=std_logic lab=BIAS_R78_M}
C {lab_pin.sym} 540 -770 0 0 {name=l65 sig_type=std_logic lab=BIAS_R79_P}
C {lab_pin.sym} 540 -830 0 0 {name=l66 sig_type=std_logic lab=BIAS_R79_M}
C {lab_pin.sym} 610 -770 0 0 {name=l67 sig_type=std_logic lab=BIAS_R80_P}
C {lab_pin.sym} 610 -830 0 0 {name=l68 sig_type=std_logic lab=BIAS_R80_M}
C {lab_pin.sym} 680 -770 0 0 {name=l69 sig_type=std_logic lab=BIAS_R82_P}
C {lab_pin.sym} 680 -830 0 0 {name=l70 sig_type=std_logic lab=BIAS_R82_M}
C {lab_pin.sym} 400 -690 3 0 {name=l71 sig_type=std_logic lab=BIAS_R83_P}
C {lab_pin.sym} 400 -750 0 0 {name=l72 sig_type=std_logic lab=BIAS_R83_M}
C {lab_wire.sym} 140 -750 0 0 {name=lw1 sig_type=std_logic lab=VCO_TAIL}
C {lab_wire.sym} 840 -480 0 0 {name=lw2 sig_type=std_logic lab=TXP_MID}
C {lab_wire.sym} 960 -480 0 0 {name=lw3 sig_type=std_logic lab=TXN_MID}
C {lab_wire.sym} -580 -480 0 0 {name=lw4 sig_type=std_logic lab=LNA_MIDP}
C {lab_wire.sym} -520 -480 0 0 {name=lw5 sig_type=std_logic lab=LNA_MIDN}
C {lab_wire.sym} 420 -90 0 0 {name=lw6 sig_type=std_logic lab=MIX_MIDP}
C {lab_wire.sym} 600 -90 0 0 {name=lw7 sig_type=std_logic lab=MIX_MIDN}
C {lab_pin.sym} 390 -185 3 0 {name=l73 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 470 -185 3 0 {name=l74 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 550 -185 3 0 {name=l75 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 630 -185 3 0 {name=l76 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 510 30 3 0 {name=l77 sig_type=std_logic lab=MIX_TAIL}
C {lab_wire.sym} 100 -810 0 0 {name=lw8 sig_type=std_logic lab=OUTP}
C {lab_wire.sym} 180 -810 0 0 {name=lw9 sig_type=std_logic lab=OUTN}
C {lab_wire.sym} 100 470 0 0 {name=lw10 sig_type=std_logic lab=ILFD_MID}
N 100 -680 100 -650 {lab=OUTP}
N 100 -650 780 -650 {lab=OUTP}
N 780 -650 780 -420 {lab=OUTP}
N 780 -420 800 -420 {lab=OUTP}
N 180 -680 180 -640 {lab=OUTN}
N 180 -640 1020 -640 {lab=OUTN}
N 1020 -640 1020 -420 {lab=OUTN}
N 1020 -420 1000 -420 {lab=OUTN}
N 100 -650 100 -230 {lab=OUTP}
N 100 -230 350 -230 {lab=OUTP}
N 350 -230 350 -140 {lab=OUTP}
N 180 -640 180 -220 {lab=OUTN}
N 180 -220 510 -220 {lab=OUTN}
N 510 -220 510 -140 {lab=OUTN}
N -580 -600 -580 -630 {lab=RF_P}
N -580 -630 380 -630 {lab=RF_P}
N 380 -630 380 -40 {lab=RF_P}
N -520 -600 -520 -620 {lab=RF_N}
N -520 -620 640 -620 {lab=RF_N}
N 640 -620 640 -40 {lab=RF_N}
N 100 -650 100 220 {lab=OUTP}
N 100 220 0 220 {lab=OUTP}
N 0 220 0 540 {lab=OUTP}
N 180 -640 180 230 {lab=OUTN}
N 180 230 200 230 {lab=OUTN}
N 200 230 200 540 {lab=OUTN}
C {lab_pin.sym} -550 -340 3 0 {name=l86 sig_type=std_logic lab=LNA_TAIL}
C {lab_pin.sym} 900 -340 3 0 {name=l84 sig_type=std_logic lab=TX_TAIL}
C {lab_pin.sym} 840 -600 0 0 {name=l85 sig_type=std_logic lab=ANT_TX}
C {lab_pin.sym} 40 390 0 0 {name=l78 sig_type=std_logic lab=DIV_P}
C {lab_pin.sym} 160 390 0 0 {name=l79 sig_type=std_logic lab=DIV_N}
C {lab_pin.sym} 0 420 0 1 {name=l80 sig_type=std_logic lab=DIV_N}
C {lab_pin.sym} 200 420 0 0 {name=l81 sig_type=std_logic lab=DIV_P}
C {lab_pin.sym} 40 570 3 0 {name=l82 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 160 570 3 0 {name=l83 sig_type=std_logic lab=ILFD_TAIL}
