v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {ADC Testbench - 12-bit SAR ADC} -300 -600 0 0 0.5 0.5 {}
T {20 MSPS, ENOB > 10 bits, VCC=3.3V, VREF=1.2V} -300 -560 0 0 0.3 0.3 {layer=7}
T {Expected: DNL < 0.5 LSB, INL < 1 LSB, SFDR > 65dB} -300 -530 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 80 -200 0 0 {name=Q_TH1
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 220 -200 0 1 {name=Q_TH2
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 80 -370 0 0 {name=Q_CMP1
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 220 -370 0 1 {name=Q_CMP2
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {devices/capa.sym} 60 -280 0 0 {name=CSP
value=500f}
C {devices/capa.sym} 240 -280 0 0 {name=CSN
value=500f}
C {devices/res.sym} 100 -450 0 0 {name=RDAC1
value=1k}
C {devices/res.sym} 200 -450 0 0 {name=RDAC2
value=2k}
C {devices/vsource.sym} -150 -460 0 0 {name=VCC
value="DC 3.3"}
C {devices/vsource.sym} -150 -350 0 0 {name=VREF
value="DC 1.2"}
C {devices/isource.sym} 150 -100 0 0 {name=ITAIL_TH
value="DC 1m"}
C {devices/isource.sym} 150 -330 0 0 {name=ITAIL_CMP
value="DC 0.5m"}
C {devices/vsource.sym} -50 -200 0 0 {name=VIN_P
value="DC 0.6 SIN(0.6 0.5 1.234567e6)"}
C {devices/vsource.sym} 350 -200 0 0 {name=VIN_N
value="DC 0.6 SIN(0.6 -0.5 1.234567e6)"}
C {devices/vsource.sym} 350 -370 0 0 {name=VCLK
value="DC 0 PULSE(0 3.3 0 100p 100p 25n 50n)"}
N 100 -230 100 -200 {lab=TH_OUTP}
N 200 -230 200 -200 {lab=TH_OUTN}
N 100 -170 200 -170 {lab=TH_TAIL}
N 150 -170 150 -120 {lab=TH_TAIL}
N 100 -400 100 -370 {lab=CMP_OUTP}
N 200 -400 200 -370 {lab=CMP_OUTN}
N 100 -340 200 -340 {lab=CMP_TAIL}
N 150 -340 150 -330 {lab=CMP_TAIL}
C {lab_pin.sym} 60 -200 0 0 {name=p1 sig_type=std_logic lab=AINP}
C {lab_pin.sym} 240 -200 0 0 {name=p2 sig_type=std_logic lab=AINN}
C {lab_pin.sym} 100 -230 0 0 {name=p3 sig_type=std_logic lab=TH_OUTP}
C {lab_pin.sym} 200 -230 0 0 {name=p4 sig_type=std_logic lab=TH_OUTN}
C {lab_pin.sym} 60 -370 0 0 {name=p5 sig_type=std_logic lab=TH_OUTP}
C {lab_pin.sym} 240 -370 0 0 {name=p6 sig_type=std_logic lab=TH_OUTN}
C {lab_pin.sym} 100 -400 0 0 {name=p7 sig_type=std_logic lab=CMP_OUTP}
C {lab_pin.sym} 200 -400 0 0 {name=p8 sig_type=std_logic lab=CMP_OUTN}
C {simulator_commands_shown.sym} -300 -500 0 0 {name=SIM
simulator=ngspice
only_toplevel=false
value="tcleval(
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ
.options gmin=1e-10 reltol=5e-3 method=gear
.tran 0.5n 10u
.meas tran cmp_delay trig v(th_outp) val=0.6 rise=1 targ v(cmp_outp) val=1.6 rise=1
.meas tran cmp_swing pp v(cmp_outp) from=5u to=10u
)"}