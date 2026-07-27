v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {ILFD Testbench - 77 GHz Injection-Locked Frequency Divider (div-by-2)} -200 -750 0 0 0.5 0.5 {}
T {Injection: 77 GHz 200mV, Expected output: 38.5 GHz, ITAIL=4mA} -200 -710 0 0 0.3 0.3 {layer=7}
T {L=120pH, R_series=5ohm, C=20fF, cross-coupled m=4, injection m=2} -200 -680 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 80 -300 0 0 {name=Q21
model=npn13G2l
spiceprefix=X
Nx=1
m=4
selft=0}
C {sg13g2_pr/npn13G2l.sym} 280 -300 0 1 {name=Q22
model=npn13G2l
spiceprefix=X
Nx=1
m=4
selft=0}
C {sg13g2_pr/npn13G2l.sym} 80 -420 0 0 {name=Q11
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 280 -420 0 1 {name=Q12
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {devices/ind.sym} 100 -540 0 0 {name=L_DIVP
value=120p}
C {devices/ind.sym} 260 -540 0 0 {name=L_DIVN
value=120p}
C {devices/res.sym} 100 -610 0 0 {name=RS_DIVP
value=5}
C {devices/res.sym} 260 -610 0 0 {name=RS_DIVN
value=5}
C {devices/capa.sym} 140 -400 0 0 {name=C_DIVP
value=20f}
C {devices/capa.sym} 220 -400 0 0 {name=C_DIVN
value=20f}
C {devices/vsource.sym} -150 -600 0 0 {name=VCC
value="DC 3.3"}
C {devices/isource.sym} 180 -200 0 0 {name=ITAIL
value="DC 4m"}
C {devices/vsource.sym} -80 -420 0 0 {name=VINJ_P
value="DC 0.9 SIN(0.9 200m 77e9)"}
C {devices/vsource.sym} 420 -420 0 0 {name=VINJ_N
value="DC 0.9 SIN(0.9 -200m 77e9)"}
C {lab_pin.sym} 100 -330 0 0 {name=p1 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 60 -300 0 1 {name=p2 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 100 -270 0 0 {name=p3 sig_type=std_logic lab=DIV_TAIL}
C {lab_pin.sym} 100 -300 0 0 {name=p4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 260 -330 0 0 {name=p5 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 300 -300 0 0 {name=p6 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 260 -270 0 0 {name=p7 sig_type=std_logic lab=DIV_TAIL}
C {lab_pin.sym} 260 -300 0 0 {name=p8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 100 -450 0 0 {name=p9 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 60 -420 0 1 {name=p10 sig_type=std_logic lab=INJ_P}
C {lab_pin.sym} 100 -390 0 0 {name=p11 sig_type=std_logic lab=DIV_TAIL}
C {lab_pin.sym} 100 -420 0 0 {name=p12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 260 -450 0 0 {name=p13 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 300 -420 0 0 {name=p14 sig_type=std_logic lab=INJ_N}
C {lab_pin.sym} 260 -390 0 0 {name=p15 sig_type=std_logic lab=DIV_TAIL}
C {lab_pin.sym} 260 -420 0 0 {name=p16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 100 -510 0 0 {name=p17 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 100 -570 0 0 {name=p18 sig_type=std_logic lab=L_MIDP}
C {lab_pin.sym} 260 -510 0 0 {name=p19 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 260 -570 0 0 {name=p20 sig_type=std_logic lab=L_MIDN}
C {lab_pin.sym} 100 -580 0 0 {name=p21 sig_type=std_logic lab=L_MIDP}
C {lab_pin.sym} 100 -640 0 0 {name=p22 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 260 -580 0 0 {name=p23 sig_type=std_logic lab=L_MIDN}
C {lab_pin.sym} 260 -640 0 0 {name=p24 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 140 -370 0 0 {name=p25 sig_type=std_logic lab=DIVP}
C {lab_pin.sym} 140 -430 0 0 {name=p26 sig_type=std_logic lab=GND}
C {lab_pin.sym} 220 -370 0 0 {name=p27 sig_type=std_logic lab=DIVN}
C {lab_pin.sym} 220 -430 0 0 {name=p28 sig_type=std_logic lab=GND}
N -150 -630 -130 -630 {lab=VCC}
N -150 -570 -130 -570 {lab=GND}
N 180 -230 200 -230 {lab=DIV_TAIL}
N 180 -170 200 -170 {lab=GND}
N -80 -450 -60 -450 {lab=INJ_P}
N -80 -390 -60 -390 {lab=GND}
N 420 -450 440 -450 {lab=INJ_N}
N 420 -390 440 -390 {lab=GND}
C {lab_pin.sym} -130 -630 0 0 {name=p29 sig_type=std_logic lab=VCC}
C {lab_pin.sym} -130 -570 0 0 {name=p30 sig_type=std_logic lab=GND}
C {lab_pin.sym} 200 -230 0 0 {name=p31 sig_type=std_logic lab=DIV_TAIL}
C {lab_pin.sym} 200 -170 0 0 {name=p32 sig_type=std_logic lab=GND}
C {lab_pin.sym} -60 -450 0 0 {name=p33 sig_type=std_logic lab=INJ_P}
C {lab_pin.sym} -60 -390 0 0 {name=p34 sig_type=std_logic lab=GND}
C {lab_pin.sym} 440 -450 0 0 {name=p35 sig_type=std_logic lab=INJ_N}
C {lab_pin.sym} 440 -390 0 0 {name=p36 sig_type=std_logic lab=GND}
C {simulator_commands_shown.sym} -200 -490 0 0 {name=SIM
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
.tran 0.2p 3n
.meas tran vdivp pp v(divp) from=1n to=3n
.meas tran vdivn pp v(divn) from=1n to=3n
.meas tran freq_div trig v(divp) val=3.3 rise=50 targ v(divp) val=3.3 rise=51
)"}
