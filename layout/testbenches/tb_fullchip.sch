v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Full-Chip 77 GHz Phased Array Testbench} -400 -1100 0 0 0.6 0.6 {}
T {VCO -> TXPA, Mixer(LO), ILFD | LNA -> Mixer(RF)} -400 -1060 0 0 0.3 0.3 {layer=7}
T {Ramped supply + AC coupling between blocks} -400 -1030 0 0 0.3 0.3 {layer=7}
T {=== VCO ===} 100 -950 0 0 0.4 0.4 {layer=4}
T {=== TXPA ===} 600 -700 0 0 0.4 0.4 {layer=4}
T {=== LNA ===} -400 -700 0 0 0.4 0.4 {layer=4}
T {=== MIXER ===} 100 -450 0 0 0.4 0.4 {layer=4}
T {=== ILFD ===} 100 -200 0 0 0.4 0.4 {layer=4}
C {sg13g2_pr/npn13G2l.sym} 180 -800 0 0 {name=Q49
model=npn13G2l
spiceprefix=X
Nx=2}
C {sg13g2_pr/npn13G2l.sym} 380 -800 0 1 {name=Q50
model=npn13G2l
spiceprefix=X
Nx=2}
C {devices/ind.sym} 200 -900 0 0 {name=L_VCOP
value=27p}
C {devices/ind.sym} 360 -900 0 0 {name=L_VCON
value=27p}
C {devices/capa.sym} 280 -850 0 0 {name=C_VAR1
value=15f}
C {devices/capa.sym} 140 -850 0 0 {name=C_VAR2
value=12f}
C {devices/capa.sym} 420 -850 0 0 {name=C_VAR3
value=12f}
C {devices/isource.sym} 280 -720 0 0 {name=I_VCO
value="PWL(0 0 0.2n 5m 10n 5m)"}
C {lab_pin.sym} 200 -830 0 0 {name=pv1 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 160 -800 0 1 {name=pv2 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 200 -770 0 0 {name=pv3 sig_type=std_logic lab=VCO_TAIL}
C {lab_pin.sym} 200 -800 0 0 {name=pv4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 360 -830 0 0 {name=pv5 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 400 -800 0 0 {name=pv6 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 360 -770 0 0 {name=pv7 sig_type=std_logic lab=VCO_TAIL}
C {lab_pin.sym} 360 -800 0 0 {name=pv8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 200 -930 0 0 {name=pv9 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 200 -870 0 0 {name=pv10 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 360 -930 0 0 {name=pv11 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 360 -870 0 0 {name=pv12 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 280 -880 0 0 {name=pv13 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 280 -820 0 0 {name=pv14 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 140 -880 0 0 {name=pv15 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 140 -820 0 0 {name=pv16 sig_type=std_logic lab=GND}
C {lab_pin.sym} 420 -880 0 0 {name=pv17 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 420 -820 0 0 {name=pv18 sig_type=std_logic lab=GND}
N 280 -750 300 -750 {lab=VCO_TAIL}
N 280 -690 300 -690 {lab=GND}
C {lab_pin.sym} 300 -750 0 0 {name=pv19 sig_type=std_logic lab=VCO_TAIL}
C {lab_pin.sym} 300 -690 0 0 {name=pv20 sig_type=std_logic lab=GND}
C {sg13g2_pr/npn13G2l.sym} 600 -500 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=8}
C {sg13g2_pr/npn13G2l.sym} 800 -500 0 1 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=8}
C {sg13g2_pr/npn13G2l.sym} 600 -620 0 0 {name=Q25
model=npn13G2l
spiceprefix=X
Nx=8}
C {sg13g2_pr/npn13G2l.sym} 800 -620 0 1 {name=Q26
model=npn13G2l
spiceprefix=X
Nx=8}
C {devices/res.sym} 620 -720 0 0 {name=RL_TXP
value=50}
C {devices/res.sym} 780 -720 0 0 {name=RL_TXN
value=50}
C {devices/capa.sym} 520 -800 0 0 {name=C_CPTXP
value=100f}
C {devices/capa.sym} 520 -730 0 0 {name=C_CPTXN
value=100f}
C {devices/res.sym} 560 -560 0 0 {name=R_BIASTXP
value=10k}
C {devices/res.sym} 560 -490 0 0 {name=R_BIASTXN
value=10k}
C {devices/isource.sym} 700 -400 0 0 {name=I_TX
value="PWL(0 0 0.2n 10m 10n 10m)"}
C {devices/vsource.sym} 900 -620 0 0 {name=V_VCB_TX
value="PWL(0 0 0.2n 2.0 10n 2.0)"}
C {lab_pin.sym} 620 -530 0 0 {name=pt1 sig_type=std_logic lab=TXP_MID}
C {lab_pin.sym} 580 -500 0 1 {name=pt2 sig_type=std_logic lab=TX_INP}
C {lab_pin.sym} 620 -470 0 0 {name=pt3 sig_type=std_logic lab=TX_TAIL}
C {lab_pin.sym} 620 -500 0 0 {name=pt4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 780 -530 0 0 {name=pt5 sig_type=std_logic lab=TXN_MID}
C {lab_pin.sym} 820 -500 0 0 {name=pt6 sig_type=std_logic lab=TX_INN}
C {lab_pin.sym} 780 -470 0 0 {name=pt7 sig_type=std_logic lab=TX_TAIL}
C {lab_pin.sym} 780 -500 0 0 {name=pt8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 620 -650 0 0 {name=pt9 sig_type=std_logic lab=ANT_TXP}
C {lab_pin.sym} 580 -620 0 1 {name=pt10 sig_type=std_logic lab=VCB_TX}
C {lab_pin.sym} 620 -590 0 0 {name=pt11 sig_type=std_logic lab=TXP_MID}
C {lab_pin.sym} 620 -620 0 0 {name=pt12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 780 -650 0 0 {name=pt13 sig_type=std_logic lab=ANT_TXN}
C {lab_pin.sym} 820 -620 0 0 {name=pt14 sig_type=std_logic lab=VCB_TX}
C {lab_pin.sym} 780 -590 0 0 {name=pt15 sig_type=std_logic lab=TXN_MID}
C {lab_pin.sym} 780 -620 0 0 {name=pt16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 620 -750 0 0 {name=pt17 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 620 -690 0 0 {name=pt18 sig_type=std_logic lab=ANT_TXP}
C {lab_pin.sym} 780 -750 0 0 {name=pt19 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 780 -690 0 0 {name=pt20 sig_type=std_logic lab=ANT_TXN}
C {lab_pin.sym} 520 -830 0 0 {name=pt21 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 520 -770 0 0 {name=pt22 sig_type=std_logic lab=TX_INP}
C {lab_pin.sym} 520 -760 0 0 {name=pt23 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 520 -700 0 0 {name=pt24 sig_type=std_logic lab=TX_INN}
C {lab_pin.sym} 560 -530 0 0 {name=pt25 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 560 -590 0 0 {name=pt26 sig_type=std_logic lab=TX_INP}
C {lab_pin.sym} 560 -460 0 0 {name=pt27 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 560 -520 0 0 {name=pt28 sig_type=std_logic lab=TX_INN}
N 700 -430 720 -430 {lab=TX_TAIL}
N 700 -370 720 -370 {lab=GND}
C {lab_pin.sym} 720 -430 0 0 {name=pt29 sig_type=std_logic lab=TX_TAIL}
C {lab_pin.sym} 720 -370 0 0 {name=pt30 sig_type=std_logic lab=GND}
N 900 -650 920 -650 {lab=VCB_TX}
N 900 -590 920 -590 {lab=GND}
C {lab_pin.sym} 920 -650 0 0 {name=pt31 sig_type=std_logic lab=VCB_TX}
C {lab_pin.sym} 920 -590 0 0 {name=pt32 sig_type=std_logic lab=GND}
C {sg13g2_pr/npn13G2l.sym} -300 -500 0 0 {name=Q61
model=npn13G2l
spiceprefix=X
Nx=4}
C {sg13g2_pr/npn13G2l.sym} -100 -500 0 1 {name=Q62
model=npn13G2l
spiceprefix=X
Nx=4}
C {sg13g2_pr/npn13G2l.sym} -300 -620 0 0 {name=Q45
model=npn13G2l
spiceprefix=X
Nx=4}
C {sg13g2_pr/npn13G2l.sym} -100 -620 0 1 {name=Q46
model=npn13G2l
spiceprefix=X
Nx=4}
C {devices/res.sym} -280 -720 0 0 {name=RL_LNAP
value=200}
C {devices/res.sym} -120 -720 0 0 {name=RL_LNAN
value=200}
C {devices/isource.sym} -200 -400 0 0 {name=I_LNA
value="PWL(0 0 0.2n 6m 10n 6m)"}
C {devices/vsource.sym} -450 -620 0 0 {name=V_VCB_LNA
value="PWL(0 0 0.2n 2.0 10n 2.0)"}
C {devices/vsource.sym} -450 -500 0 0 {name=V_RFP
value="DC 0.9 SIN(0.9 0.001 77e9)"}
C {devices/vsource.sym} 50 -500 0 0 {name=V_RFN
value="DC 0.9 SIN(0.9 -0.001 77e9)"}
C {lab_pin.sym} -280 -530 0 0 {name=pl1 sig_type=std_logic lab=LNA_MIDP}
C {lab_pin.sym} -320 -500 0 1 {name=pl2 sig_type=std_logic lab=RF_INP}
C {lab_pin.sym} -280 -470 0 0 {name=pl3 sig_type=std_logic lab=LNA_TAIL}
C {lab_pin.sym} -280 -500 0 0 {name=pl4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -120 -530 0 0 {name=pl5 sig_type=std_logic lab=LNA_MIDN}
C {lab_pin.sym} -80 -500 0 0 {name=pl6 sig_type=std_logic lab=RF_INN}
C {lab_pin.sym} -120 -470 0 0 {name=pl7 sig_type=std_logic lab=LNA_TAIL}
C {lab_pin.sym} -120 -500 0 0 {name=pl8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -280 -650 0 0 {name=pl9 sig_type=std_logic lab=RF_P}
C {lab_pin.sym} -320 -620 0 1 {name=pl10 sig_type=std_logic lab=VCB_LNA}
C {lab_pin.sym} -280 -590 0 0 {name=pl11 sig_type=std_logic lab=LNA_MIDP}
C {lab_pin.sym} -280 -620 0 0 {name=pl12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -120 -650 0 0 {name=pl13 sig_type=std_logic lab=RF_N}
C {lab_pin.sym} -80 -620 0 0 {name=pl14 sig_type=std_logic lab=VCB_LNA}
C {lab_pin.sym} -120 -590 0 0 {name=pl15 sig_type=std_logic lab=LNA_MIDN}
C {lab_pin.sym} -120 -620 0 0 {name=pl16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} -280 -750 0 0 {name=pl17 sig_type=std_logic lab=VCC}
C {lab_pin.sym} -280 -690 0 0 {name=pl18 sig_type=std_logic lab=RF_P}
C {lab_pin.sym} -120 -750 0 0 {name=pl19 sig_type=std_logic lab=VCC}
C {lab_pin.sym} -120 -690 0 0 {name=pl20 sig_type=std_logic lab=RF_N}
N -200 -430 -180 -430 {lab=LNA_TAIL}
N -200 -370 -180 -370 {lab=GND}
C {lab_pin.sym} -180 -430 0 0 {name=pl21 sig_type=std_logic lab=LNA_TAIL}
C {lab_pin.sym} -180 -370 0 0 {name=pl22 sig_type=std_logic lab=GND}
N -450 -650 -430 -650 {lab=VCB_LNA}
N -450 -590 -430 -590 {lab=GND}
C {lab_pin.sym} -430 -650 0 0 {name=pl23 sig_type=std_logic lab=VCB_LNA}
C {lab_pin.sym} -430 -590 0 0 {name=pl24 sig_type=std_logic lab=GND}
N -450 -530 -430 -530 {lab=RF_INP}
N -450 -470 -430 -470 {lab=GND}
C {lab_pin.sym} -430 -530 0 0 {name=pl25 sig_type=std_logic lab=RF_INP}
C {lab_pin.sym} -430 -470 0 0 {name=pl26 sig_type=std_logic lab=GND}
N 50 -530 70 -530 {lab=RF_INN}
N 50 -470 70 -470 {lab=GND}
C {lab_pin.sym} 70 -530 0 0 {name=pl27 sig_type=std_logic lab=RF_INN}
C {lab_pin.sym} 70 -470 0 0 {name=pl28 sig_type=std_logic lab=GND}
C {sg13g2_pr/npn13G2l.sym} 180 -300 0 0 {name=Q41
model=npn13G2l
spiceprefix=X
Nx=4}
C {sg13g2_pr/npn13G2l.sym} 480 -300 0 1 {name=Q42
model=npn13G2l
spiceprefix=X
Nx=4}
C {sg13g2_pr/npn13G2l.sym} 150 -420 0 0 {name=Q65
model=npn13G2l
spiceprefix=X
Nx=2}
C {sg13g2_pr/npn13G2l.sym} 250 -420 0 1 {name=Q66
model=npn13G2l
spiceprefix=X
Nx=2}
C {sg13g2_pr/npn13G2l.sym} 380 -420 0 0 {name=Q67
model=npn13G2l
spiceprefix=X
Nx=2}
C {sg13g2_pr/npn13G2l.sym} 480 -420 0 1 {name=Q68
model=npn13G2l
spiceprefix=X
Nx=2}
C {devices/res.sym} 200 -520 0 0 {name=RL_IFP
value=1k}
C {devices/res.sym} 400 -520 0 0 {name=RL_IFN
value=1k}
C {devices/capa.sym} 100 -420 0 0 {name=C_CPLOP
value=100f}
C {devices/capa.sym} 100 -350 0 0 {name=C_CPLON
value=100f}
C {devices/res.sym} 60 -420 0 0 {name=R_BIASLOP
value=10k}
C {devices/res.sym} 60 -350 0 0 {name=R_BIASLON
value=10k}
C {devices/isource.sym} 330 -220 0 0 {name=I_MIX
value="PWL(0 0 0.2n 4m 10n 4m)"}
C {lab_pin.sym} 200 -330 0 0 {name=pm1 sig_type=std_logic lab=MIX_MIDP}
C {lab_pin.sym} 160 -300 0 1 {name=pm2 sig_type=std_logic lab=RF_P}
C {lab_pin.sym} 200 -270 0 0 {name=pm3 sig_type=std_logic lab=MIX_TAIL}
C {lab_pin.sym} 200 -300 0 0 {name=pm4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 460 -330 0 0 {name=pm5 sig_type=std_logic lab=MIX_MIDN}
C {lab_pin.sym} 500 -300 0 0 {name=pm6 sig_type=std_logic lab=RF_N}
C {lab_pin.sym} 460 -270 0 0 {name=pm7 sig_type=std_logic lab=MIX_TAIL}
C {lab_pin.sym} 460 -300 0 0 {name=pm8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 170 -450 0 0 {name=pm9 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 130 -420 0 1 {name=pm10 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 170 -390 0 0 {name=pm11 sig_type=std_logic lab=MIX_MIDP}
C {lab_pin.sym} 170 -420 0 0 {name=pm12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 230 -450 0 0 {name=pm13 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 270 -420 0 0 {name=pm14 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 230 -390 0 0 {name=pm15 sig_type=std_logic lab=MIX_MIDP}
C {lab_pin.sym} 230 -420 0 0 {name=pm16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 400 -450 0 0 {name=pm17 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 360 -420 0 1 {name=pm18 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 400 -390 0 0 {name=pm19 sig_type=std_logic lab=MIX_MIDN}
C {lab_pin.sym} 400 -420 0 0 {name=pm20 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 460 -450 0 0 {name=pm21 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 500 -420 0 0 {name=pm22 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 460 -390 0 0 {name=pm23 sig_type=std_logic lab=MIX_MIDN}
C {lab_pin.sym} 460 -420 0 0 {name=pm24 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 200 -550 0 0 {name=pm25 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 200 -490 0 0 {name=pm26 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 400 -550 0 0 {name=pm27 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 400 -490 0 0 {name=pm28 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 100 -450 0 0 {name=pm29 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 100 -390 0 0 {name=pm30 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 100 -380 0 0 {name=pm31 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 100 -320 0 0 {name=pm32 sig_type=std_logic lab=LO_N}
C {lab_pin.sym} 60 -450 0 0 {name=pm33 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 60 -390 0 0 {name=pm34 sig_type=std_logic lab=LO_P}
C {lab_pin.sym} 60 -380 0 0 {name=pm35 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 60 -320 0 0 {name=pm36 sig_type=std_logic lab=LO_N}
N 330 -250 350 -250 {lab=MIX_TAIL}
N 330 -190 350 -190 {lab=GND}
C {lab_pin.sym} 350 -250 0 0 {name=pm37 sig_type=std_logic lab=MIX_TAIL}
C {lab_pin.sym} 350 -190 0 0 {name=pm38 sig_type=std_logic lab=GND}
C {sg13g2_pr/npn13G2l.sym} 180 -20 0 0 {name=Q21
model=npn13G2l
spiceprefix=X
Nx=4}
C {sg13g2_pr/npn13G2l.sym} 380 -20 0 1 {name=Q22
model=npn13G2l
spiceprefix=X
Nx=4}
C {sg13g2_pr/npn13G2l.sym} 180 -140 0 0 {name=Q11
model=npn13G2l
spiceprefix=X
Nx=2}
C {sg13g2_pr/npn13G2l.sym} 380 -140 0 1 {name=Q12
model=npn13G2l
spiceprefix=X
Nx=2}
C {devices/ind.sym} 200 -260 0 0 {name=L_DIVP
value=120p}
C {devices/ind.sym} 360 -260 0 0 {name=L_DIVN
value=120p}
C {devices/res.sym} 200 -330 0 0 {name=R_DIVP
value=5}
C {devices/res.sym} 360 -330 0 0 {name=R_DIVN
value=5}
C {devices/capa.sym} 140 -60 0 0 {name=C_DIVP
value=20f}
C {devices/capa.sym} 420 -60 0 0 {name=C_DIVN
value=20f}
C {devices/capa.sym} 100 -140 0 0 {name=C_CPINJP
value=100f}
C {devices/capa.sym} 480 -140 0 0 {name=C_CPINJN
value=100f}
C {devices/res.sym} 60 -140 0 0 {name=R_BIASINJP
value=10k}
C {devices/res.sym} 520 -140 0 0 {name=R_BIASINJN
value=10k}
C {devices/isource.sym} 280 60 0 0 {name=I_ILFD
value="PWL(0 0 0.2n 4m 10n 4m)"}
C {lab_pin.sym} 200 -50 0 0 {name=pi1 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 160 -20 0 1 {name=pi2 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 200 10 0 0 {name=pi3 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 200 -20 0 0 {name=pi4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 360 -50 0 0 {name=pi5 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 400 -20 0 0 {name=pi6 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 360 10 0 0 {name=pi7 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 360 -20 0 0 {name=pi8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 200 -170 0 0 {name=pi9 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 160 -140 0 1 {name=pi10 sig_type=std_logic lab=INJ_P}
C {lab_pin.sym} 200 -110 0 0 {name=pi11 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 200 -140 0 0 {name=pi12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 360 -170 0 0 {name=pi13 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 400 -140 0 0 {name=pi14 sig_type=std_logic lab=INJ_N}
C {lab_pin.sym} 360 -110 0 0 {name=pi15 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 360 -140 0 0 {name=pi16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 200 -290 0 0 {name=pi17 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 200 -230 0 0 {name=pi18 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 360 -290 0 0 {name=pi19 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 360 -230 0 0 {name=pi20 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 200 -360 0 0 {name=pi21 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 200 -300 0 0 {name=pi22 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 360 -360 0 0 {name=pi23 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 360 -300 0 0 {name=pi24 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 140 -90 0 0 {name=pi25 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 140 -30 0 0 {name=pi26 sig_type=std_logic lab=GND}
C {lab_pin.sym} 420 -90 0 0 {name=pi27 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 420 -30 0 0 {name=pi28 sig_type=std_logic lab=GND}
C {lab_pin.sym} 100 -170 0 0 {name=pi29 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 100 -110 0 0 {name=pi30 sig_type=std_logic lab=INJ_P}
C {lab_pin.sym} 480 -170 0 0 {name=pi31 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 480 -110 0 0 {name=pi32 sig_type=std_logic lab=INJ_N}
C {lab_pin.sym} 60 -170 0 0 {name=pi33 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 60 -110 0 0 {name=pi34 sig_type=std_logic lab=INJ_P}
C {lab_pin.sym} 520 -170 0 0 {name=pi35 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 520 -110 0 0 {name=pi36 sig_type=std_logic lab=INJ_N}
N 280 30 300 30 {lab=ILFD_TAIL}
N 280 90 300 90 {lab=GND}
C {lab_pin.sym} 300 30 0 0 {name=pi37 sig_type=std_logic lab=ILFD_TAIL}
C {lab_pin.sym} 300 90 0 0 {name=pi38 sig_type=std_logic lab=GND}
C {devices/vsource.sym} -600 -800 0 0 {name=VCC
value="PWL(0 0 0.2n 3.3 10n 3.3)"}
N -600 -830 -580 -830 {lab=VCC}
N -600 -770 -580 -770 {lab=GND}
C {lab_pin.sym} -580 -830 0 0 {name=ps1 sig_type=std_logic lab=VCC}
C {lab_pin.sym} -580 -770 0 0 {name=ps2 sig_type=std_logic lab=GND}
C {simulator_commands_shown.sym} -600 -600 0 0 {name=SIM
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
.tran 0.2p 4n
.meas tran vco_freq trig v(outp) val=3.3 rise=200 targ v(outp) val=3.3 rise=201
.meas tran vco_swing pp v(outp) from=3n to=4n
.meas tran txpa_swing pp v(ant_txp) from=3n to=4n
.meas tran lna_swing pp v(rf_p) from=3n to=4n
.meas tran mixer_ifp pp v(ifp) from=3n to=4n
.meas tran ilfd_freq trig v(divp) val=3.3 rise=100 targ v(divp) val=3.3 rise=101
.meas tran ilfd_swing pp v(divp) from=3n to=4n
)"}
