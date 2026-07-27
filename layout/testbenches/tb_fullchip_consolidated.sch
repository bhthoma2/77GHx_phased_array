v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {77 GHz Phased Array — Consolidated Full-Chip Testbench} -400 -1200 0 0 0.6 0.6 {}
T {PDK devices (varactors, rppd, npn13G2l) + on-chip bias + stimulus} -400 -1160 0 0 0.3 0.3 {layer=7}
T {=== VCO (cross-coupled, PDK varactors) ===} 50 -1050 0 0 0.4 0.4 {layer=4}
T {=== TXPA (diff cascode Nx=8) ===} 700 -800 0 0 0.4 0.4 {layer=4}
T {=== LNA (diff cascode Nx=4) ===} -500 -800 0 0 0.4 0.4 {layer=4}
T {=== MIXER (Gilbert cell) ===} 100 -550 0 0 0.4 0.4 {layer=4}
T {=== ILFD (inj-locked divider) ===} 100 -250 0 0 0.4 0.4 {layer=4}
T {=== BIAS NETWORK ===} 600 -1050 0 0 0.4 0.4 {layer=4}
T {=== SUPPLIES & STIMULUS ===} -600 -1050 0 0 0.4 0.4 {layer=4}
C {sg13g2_pr/npn13G2l.sym} 180 -900 0 0 {name=Q49
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 380 -900 0 1 {name=Q50
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/sg13_svaricap.sym} 160 -970 0 1 {name=CVAR1
model=sg13_hv_svaricap
spiceprefix=X
w=3.74e-6
l=0.3e-6
Nx=1}
C {sg13g2_pr/sg13_svaricap.sym} 400 -970 0 0 {name=CVAR2
model=sg13_hv_svaricap
spiceprefix=X
w=3.74e-6
l=0.3e-6
Nx=1}
C {sg13g2_pr/rppd.sym} 280 -820 0 0 {name=R_TAIL
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {devices/ind.sym} 200 -1020 0 0 {name=L_VCOP
value=27p}
C {devices/ind.sym} 360 -1020 0 0 {name=L_VCON
value=27p}
C {lab_pin.sym} 200 -930 0 0 {name=pv1 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 160 -900 0 1 {name=pv2 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 200 -870 0 0 {name=pv3 sig_type=std_logic lab=VCO_TAIL}
C {lab_pin.sym} 200 -900 0 0 {name=pv4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 360 -930 0 0 {name=pv5 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 400 -900 0 0 {name=pv6 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 360 -870 0 0 {name=pv7 sig_type=std_logic lab=VCO_TAIL}
C {lab_pin.sym} 360 -900 0 0 {name=pv8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 200 -1050 0 0 {name=pv9 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 200 -990 0 0 {name=pv10 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 360 -1050 0 0 {name=pv11 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 360 -990 0 0 {name=pv12 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 160 -1000 0 0 {name=pv13 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 160 -940 0 0 {name=pv14 sig_type=std_logic lab=VTUNE}
C {lab_pin.sym} 400 -1000 0 0 {name=pv15 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 400 -940 0 0 {name=pv16 sig_type=std_logic lab=VTUNE}
C {lab_pin.sym} 280 -850 0 0 {name=pv17 sig_type=std_logic lab=VCO_TAIL}
C {lab_pin.sym} 280 -790 0 0 {name=pv18 sig_type=std_logic lab=GND}
C {sg13g2_pr/npn13G2l.sym} 750 -600 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=8
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 950 -600 0 1 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=8
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 750 -720 0 0 {name=Q25
model=npn13G2l
spiceprefix=X
Nx=8
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 950 -720 0 1 {name=Q26
model=npn13G2l
spiceprefix=X
Nx=8
El=1.0}
C {devices/res.sym} 770 -820 0 0 {name=RL_TXP
value=50}
C {devices/res.sym} 930 -820 0 0 {name=RL_TXN
value=50}
C {devices/capa.sym} 660 -720 0 0 {name=C_CPTXP
value=100f}
C {devices/capa.sym} 660 -650 0 0 {name=C_CPTXN
value=100f}
C {devices/res.sym} 620 -720 0 0 {name=R_BIASTXP
value=10k}
C {devices/res.sym} 620 -650 0 0 {name=R_BIASTXN
value=10k}
C {devices/isource.sym} 850 -500 0 0 {name=I_TX
value="PWL(0 0 0.2n 10m 10n 10m)"}
C {devices/vsource.sym} 1050 -720 0 0 {name=V_VCB_TX
value="PWL(0 0 0.2n 2.0 10n 2.0)"}
C {lab_pin.sym} 770 -630 0 0 {name=pt1 sig_type=std_logic lab=TXP_MID}
C {lab_pin.sym} 730 -600 0 1 {name=pt2 sig_type=std_logic lab=TX_INP}
C {lab_pin.sym} 770 -570 0 0 {name=pt3 sig_type=std_logic lab=TX_TAIL}
C {lab_pin.sym} 770 -600 0 0 {name=pt4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 930 -630 0 0 {name=pt5 sig_type=std_logic lab=TXN_MID}
C {lab_pin.sym} 970 -600 0 0 {name=pt6 sig_type=std_logic lab=TX_INN}
C {lab_pin.sym} 930 -570 0 0 {name=pt7 sig_type=std_logic lab=TX_TAIL}
C {lab_pin.sym} 930 -600 0 0 {name=pt8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 770 -750 0 0 {name=pt9 sig_type=std_logic lab=ANT_TXP}
C {lab_pin.sym} 730 -720 0 1 {name=pt10 sig_type=std_logic lab=VCB_TX}
C {lab_pin.sym} 770 -690 0 0 {name=pt11 sig_type=std_logic lab=TXP_MID}
C {lab_pin.sym} 770 -720 0 0 {name=pt12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 930 -750 0 0 {name=pt13 sig_type=std_logic lab=ANT_TXN}
C {lab_pin.sym} 970 -720 0 0 {name=pt14 sig_type=std_logic lab=VCB_TX}
C {lab_pin.sym} 930 -690 0 0 {name=pt15 sig_type=std_logic lab=TXN_MID}
C {lab_pin.sym} 930 -720 0 0 {name=pt16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 770 -850 0 0 {name=pt17 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 770 -790 0 0 {name=pt18 sig_type=std_logic lab=ANT_TXP}
C {lab_pin.sym} 930 -850 0 0 {name=pt19 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 930 -790 0 0 {name=pt20 sig_type=std_logic lab=ANT_TXN}
C {lab_pin.sym} 660 -750 0 0 {name=pt21 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 660 -690 0 0 {name=pt22 sig_type=std_logic lab=TX_INP}
C {lab_pin.sym} 660 -680 0 0 {name=pt23 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 660 -620 0 0 {name=pt24 sig_type=std_logic lab=TX_INN}
C {lab_pin.sym} 620 -750 0 0 {name=pt25 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 620 -690 0 0 {name=pt26 sig_type=std_logic lab=TX_INP}
C {lab_pin.sym} 620 -680 0 0 {name=pt27 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 620 -620 0 0 {name=pt28 sig_type=std_logic lab=TX_INN}
N 850 -530 870 -530 {lab=TX_TAIL}
N 850 -470 870 -470 {lab=GND}
C {lab_pin.sym} 870 -530 0 0 {name=pt29 sig_type=std_logic lab=TX_TAIL}
C {lab_pin.sym} 870 -470 0 0 {name=pt30 sig_type=std_logic lab=GND}
N 1050 -750 1070 -750 {lab=VCB_TX}
N 1050 -690 1070 -690 {lab=GND}
C {lab_pin.sym} 1070 -750 0 0 {name=pt31 sig_type=std_logic lab=VCB_TX}
C {lab_pin.sym} 1070 -690 0 0 {name=pt32 sig_type=std_logic lab=GND}
C {sg13g2_pr/npn13G2l.sym} -400 -600 0 0 {name=Q61
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} -200 -600 0 1 {name=Q62
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} -400 -720 0 0 {name=Q45
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} -200 -720 0 1 {name=Q46
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {devices/res.sym} -380 -820 0 0 {name=RL_LNAP
value=200}
C {devices/res.sym} -220 -820 0 0 {name=RL_LNAN
value=200}
C {devices/isource.sym} -300 -500 0 0 {name=I_LNA
value="PWL(0 0 0.2n 6m 10n 6m)"}
C {devices/vsource.sym} -550 -720 0 0 {name=V_VCB_LNA
value="PWL(0 0 0.2n 2.0 10n 2.0)"}
C {devices/vsource.sym} -550 -600 0 0 {name=V_RFP
value="DC 0.9 SIN(0.9 0.001 77e9)"}
C {devices/vsource.sym} -50 -600 0 0 {name=V_RFN
value="DC 0.9 SIN(0.9 -0.001 77e9)"}
C {lab_pin.sym} -380 -630 0 0 {name=pl1 sig_type=std_logic lab=LNA_MIDP}
C {lab_pin.sym} -420 -600 0 1 {name=pl2 sig_type=std_logic lab=RF_INP}
C {lab_pin.sym} -380 -570 0 0 {name=pl3 sig_type=std_logic lab=LNA_TAIL}
C {lab_pin.sym} -380 -600 0 0 {name=pl4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -220 -630 0 0 {name=pl5 sig_type=std_logic lab=LNA_MIDN}
C {lab_pin.sym} -180 -600 0 0 {name=pl6 sig_type=std_logic lab=RF_INN}
C {lab_pin.sym} -220 -570 0 0 {name=pl7 sig_type=std_logic lab=LNA_TAIL}
C {lab_pin.sym} -220 -600 0 0 {name=pl8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -380 -750 0 0 {name=pl9 sig_type=std_logic lab=RF_P}
C {lab_pin.sym} -420 -720 0 1 {name=pl10 sig_type=std_logic lab=VCB_LNA}
C {lab_pin.sym} -380 -690 0 0 {name=pl11 sig_type=std_logic lab=LNA_MIDP}
C {lab_pin.sym} -380 -720 0 0 {name=pl12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -220 -750 0 0 {name=pl13 sig_type=std_logic lab=RF_N}
C {lab_pin.sym} -180 -720 0 0 {name=pl14 sig_type=std_logic lab=VCB_LNA}
C {lab_pin.sym} -220 -690 0 0 {name=pl15 sig_type=std_logic lab=LNA_MIDN}
C {lab_pin.sym} -220 -720 0 0 {name=pl16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -380 -850 0 0 {name=pl17 sig_type=std_logic lab=VCC}
C {lab_pin.sym} -380 -790 0 0 {name=pl18 sig_type=std_logic lab=RF_P}
C {lab_pin.sym} -220 -850 0 0 {name=pl19 sig_type=std_logic lab=VCC}
C {lab_pin.sym} -220 -790 0 0 {name=pl20 sig_type=std_logic lab=RF_N}
N -300 -530 -280 -530 {lab=LNA_TAIL}
N -300 -470 -280 -470 {lab=GND}
C {lab_pin.sym} -280 -530 0 0 {name=pl21 sig_type=std_logic lab=LNA_TAIL}
C {lab_pin.sym} -280 -470 0 0 {name=pl22 sig_type=std_logic lab=GND}
N -550 -750 -530 -750 {lab=VCB_LNA}
N -550 -690 -530 -690 {lab=GND}
C {lab_pin.sym} -530 -750 0 0 {name=pl23 sig_type=std_logic lab=VCB_LNA}
C {lab_pin.sym} -530 -690 0 0 {name=pl24 sig_type=std_logic lab=GND}
N -550 -630 -530 -630 {lab=RF_INP}
N -550 -570 -530 -570 {lab=GND}
C {lab_pin.sym} -530 -630 0 0 {name=pl25 sig_type=std_logic lab=RF_INP}
C {lab_pin.sym} -530 -570 0 0 {name=pl26 sig_type=std_logic lab=GND}
N -50 -630 -30 -630 {lab=RF_INN}
N -50 -570 -30 -570 {lab=GND}
C {lab_pin.sym} -30 -630 0 0 {name=pl27 sig_type=std_logic lab=RF_INN}
C {lab_pin.sym} -30 -570 0 0 {name=pl28 sig_type=std_logic lab=GND}
C {sg13g2_pr/npn13G2l.sym} 180 -400 0 0 {name=Q41
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 480 -400 0 1 {name=Q42
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 150 -500 0 0 {name=Q65
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 250 -500 0 1 {name=Q66
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 380 -500 0 0 {name=Q67
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 480 -500 0 1 {name=Q68
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {devices/res.sym} 200 -600 0 0 {name=RL_IFP
value=1k}
C {devices/res.sym} 400 -600 0 0 {name=RL_IFN
value=1k}
C {devices/capa.sym} 100 -500 0 0 {name=C_CPLOP
value=100f}
C {devices/capa.sym} 100 -430 0 0 {name=C_CPLON
value=100f}
C {devices/res.sym} 60 -500 0 0 {name=R_BIASLOP
value=10k}
C {devices/res.sym} 60 -430 0 0 {name=R_BIASLON
value=10k}
C {devices/isource.sym} 330 -310 0 0 {name=I_MIX
value="PWL(0 0 0.2n 4m 10n 4m)"}
C {lab_pin.sym} 200 -430 0 0 {name=pm1 sig_type=std_logic lab=MIX_MIDP}
C {lab_pin.sym} 160 -400 0 1 {name=pm2 sig_type=std_logic lab=RF_P}
C {lab_pin.sym} 200 -370 0 0 {name=pm3 sig_type=std_logic lab=MIX_TAIL}
C {lab_pin.sym} 200 -400 0 0 {name=pm4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 460 -430 0 0 {name=pm5 sig_type=std_logic lab=MIX_MIDN}
C {lab_pin.sym} 500 -400 0 0 {name=pm6 sig_type=std_logic lab=RF_N}
C {lab_pin.sym} 460 -370 0 0 {name=pm7 sig_type=std_logic lab=MIX_TAIL}
C {lab_pin.sym} 460 -400 0 0 {name=pm8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 170 -530 0 0 {name=pm9 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 130 -500 0 1 {name=pm10 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 170 -470 0 0 {name=pm11 sig_type=std_logic lab=MIX_MIDP}
C {lab_pin.sym} 170 -500 0 0 {name=pm12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 230 -530 0 0 {name=pm13 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 270 -500 0 0 {name=pm14 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 230 -470 0 0 {name=pm15 sig_type=std_logic lab=MIX_MIDP}
C {lab_pin.sym} 230 -500 0 0 {name=pm16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 400 -530 0 0 {name=pm17 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 360 -500 0 1 {name=pm18 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 400 -470 0 0 {name=pm19 sig_type=std_logic lab=MIX_MIDN}
C {lab_pin.sym} 400 -500 0 0 {name=pm20 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 460 -530 0 0 {name=pm21 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 500 -500 0 0 {name=pm22 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 460 -470 0 0 {name=pm23 sig_type=std_logic lab=MIX_MIDN}
C {lab_pin.sym} 460 -500 0 0 {name=pm24 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 200 -630 0 0 {name=pm25 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 200 -570 0 0 {name=pm26 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 400 -630 0 0 {name=pm27 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 400 -570 0 0 {name=pm28 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 100 -530 0 0 {name=pm29 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 100 -470 0 0 {name=pm30 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 100 -460 0 0 {name=pm31 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 100 -400 0 0 {name=pm32 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 60 -530 0 0 {name=pm33 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 60 -470 0 0 {name=pm34 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 60 -460 0 0 {name=pm35 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 60 -400 0 0 {name=pm36 sig_type=std_logic lab=LO_N}
N 330 -340 350 -340 {lab=MIX_TAIL}
N 330 -280 350 -280 {lab=GND}
C {lab_pin.sym} 350 -340 0 0 {name=pm37 sig_type=std_logic lab=MIX_TAIL}
C {lab_pin.sym} 350 -280 0 0 {name=pm38 sig_type=std_logic lab=GND}
C {sg13g2_pr/npn13G2l.sym} 180 -80 0 0 {name=Q21
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 380 -80 0 1 {name=Q22
model=npn13G2l
spiceprefix=X
Nx=4
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 180 -180 0 0 {name=Q11
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {sg13g2_pr/npn13G2l.sym} 380 -180 0 1 {name=Q12
model=npn13G2l
spiceprefix=X
Nx=2
El=1.0}
C {devices/ind.sym} 200 -260 0 0 {name=L_DIVP
value=120p}
C {devices/ind.sym} 360 -260 0 0 {name=L_DIVN
value=120p}
C {devices/capa.sym} 140 -120 0 0 {name=C_DIVP
value=20f}
C {devices/capa.sym} 420 -120 0 0 {name=C_DIVN
value=20f}
C {devices/capa.sym} 100 -180 0 0 {name=C_CPINJP
value=100f}
C {devices/capa.sym} 480 -180 0 0 {name=C_CPINJN
value=100f}
C {devices/res.sym} 60 -180 0 0 {name=R_BIASINJP
value=10k}
C {devices/res.sym} 520 -180 0 0 {name=R_BIASINJN
value=10k}
C {devices/isource.sym} 280 10 0 0 {name=I_ILFD
value="PWL(0 0 0.2n 4m 10n 4m)"}
C {lab_pin.sym} 200 -110 0 0 {name=pi1 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 160 -80 0 1 {name=pi2 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 200 -50 0 0 {name=pi3 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 200 -80 0 0 {name=pi4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 360 -110 0 0 {name=pi5 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 400 -80 0 0 {name=pi6 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 360 -50 0 0 {name=pi7 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 360 -80 0 0 {name=pi8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 200 -210 0 0 {name=pi9 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 160 -180 0 1 {name=pi10 sig_type=std_logic lab=INJ_P}
C {lab_pin.sym} 200 -150 0 0 {name=pi11 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 200 -180 0 0 {name=pi12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 360 -210 0 0 {name=pi13 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 400 -180 0 0 {name=pi14 sig_type=std_logic lab=INJ_N}
C {lab_pin.sym} 360 -150 0 0 {name=pi15 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 360 -180 0 0 {name=pi16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 200 -290 0 0 {name=pi17 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 200 -230 0 0 {name=pi18 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 360 -290 0 0 {name=pi19 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 360 -230 0 0 {name=pi20 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 140 -150 0 0 {name=pi25 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 140 -90 0 0 {name=pi26 sig_type=std_logic lab=GND}
C {lab_pin.sym} 420 -150 0 0 {name=pi27 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 420 -90 0 0 {name=pi28 sig_type=std_logic lab=GND}
C {lab_pin.sym} 100 -210 0 0 {name=pi29 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 100 -150 0 0 {name=pi30 sig_type=std_logic lab=INJ_P}
C {lab_pin.sym} 480 -210 0 0 {name=pi31 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 480 -150 0 0 {name=pi32 sig_type=std_logic lab=INJ_N}
C {lab_pin.sym} 60 -210 0 0 {name=pi33 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 60 -150 0 0 {name=pi34 sig_type=std_logic lab=INJ_P}
C {lab_pin.sym} 520 -210 0 0 {name=pi35 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 520 -150 0 0 {name=pi36 sig_type=std_logic lab=INJ_N}
N 280 -20 300 -20 {lab=ILFD_TAIL}
N 280 40 300 40 {lab=GND}
C {lab_pin.sym} 300 -20 0 0 {name=pi37 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 300 40 0 0 {name=pi38 sig_type=std_logic lab=GND}
C {devices/vsource.sym} -600 -950 0 0 {name=VCC
value="PWL(0 0 0.2n 3.3 10n 3.3)"}
C {devices/vsource.sym} -600 -870 0 0 {name=VTUNE_SRC
value=1.5}
N -600 -980 -580 -980 {lab=VCC}
N -600 -920 -580 -920 {lab=GND}
C {lab_pin.sym} -580 -980 0 0 {name=ps1 sig_type=std_logic lab=VCC}
C {lab_pin.sym} -580 -920 0 0 {name=ps2 sig_type=std_logic lab=GND}
N -600 -900 -580 -900 {lab=VTUNE}
N -600 -840 -580 -840 {lab=GND}
C {lab_pin.sym} -580 -900 0 0 {name=ps3 sig_type=std_logic lab=VTUNE}
C {lab_pin.sym} -580 -840 0 0 {name=ps4 sig_type=std_logic lab=GND}
C {sg13g2_pr/rppd.sym} 650 -950 0 0 {name=R77
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {sg13g2_pr/rppd.sym} 720 -950 0 0 {name=R78
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {sg13g2_pr/rppd.sym} 790 -950 0 0 {name=R79
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1}
C {sg13g2_pr/cap_cmim.sym} 650 -880 0 0 {name=C84
w=6.99e-6
l=6.99e-6
model=cap_cmim
spiceprefix=X
m=1}
C {sg13g2_pr/cap_cmim.sym} 720 -880 0 0 {name=C85
w=6.99e-6
l=6.99e-6
model=cap_cmim
spiceprefix=X
m=1}
C {sg13g2_pr/cap_cmim.sym} 790 -880 0 0 {name=C86
w=6.99e-6
l=6.99e-6
model=cap_cmim
spiceprefix=X
m=1}
C {lab_pin.sym} 650 -980 0 0 {name=lb1 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 650 -920 0 0 {name=lb2 sig_type=std_logic lab=BIAS1}
C {lab_pin.sym} 720 -980 0 0 {name=lb3 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 720 -920 0 0 {name=lb4 sig_type=std_logic lab=BIAS2}
C {lab_pin.sym} 790 -980 0 0 {name=lb5 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 790 -920 0 0 {name=lb6 sig_type=std_logic lab=BIAS3}
C {lab_pin.sym} 650 -910 0 0 {name=lb7 sig_type=std_logic lab=BIAS1}
C {lab_pin.sym} 650 -850 0 0 {name=lb8 sig_type=std_logic lab=GND}
C {lab_pin.sym} 720 -910 0 0 {name=lb9 sig_type=std_logic lab=BIAS2}
C {lab_pin.sym} 720 -850 0 0 {name=lb10 sig_type=std_logic lab=GND}
C {lab_pin.sym} 790 -910 0 0 {name=lb11 sig_type=std_logic lab=BIAS3}
C {lab_pin.sym} 790 -850 0 0 {name=lb12 sig_type=std_logic lab=GND}
C {devices/gnd.sym} 280 100 0 0 {name=l1 lab=GND}
C {simulator_commands_shown.sym} -600 -450 0 0 {name=SIM
simulator=ngspice
only_toplevel=false
value="tcleval(
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ
.options gmin=1e-10 reltol=5e-3 abstol=1e-10 vntol=1e-4
.options itl1=1000 itl2=200 itl4=500
.options method=gear maxord=3
.options noopiter
.tran 0.2p 4n uic
* === Measurements ===
.meas tran vco_freq trig v(outp) val=1.65 rise=200 targ v(outp) val=1.65 rise=201
.meas tran vco_swing pp v(outp) from=3n to=4n
.meas tran txpa_swing pp v(ant_txp) from=3n to=4n
.meas tran lna_gain_db param='20*log10(v(rf_p)/0.001)' from=3n to=4n
.meas tran mixer_ifp pp v(ifp) from=3n to=4n
.meas tran ilfd_freq trig v(divp) val=1.65 rise=100 targ v(divp) val=1.65 rise=101
.meas tran ilfd_swing pp v(divp) from=3n to=4n
.meas tran ilfd_lock_ratio param='vco_freq/ilfd_freq'
)"}
