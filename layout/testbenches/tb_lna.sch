v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {LNA Testbench - 77 GHz Differential Cascode Low-Noise Amplifier} -300 -600 0 0 0.5 0.5 {}
T {m=4, ITAIL=6mA, VCC=3.3V, RL=200 ohm} -300 -560 0 0 0.3 0.3 {layer=7}
T {Expected: voltage gain > 15 dB, NF < 5 dB at 77 GHz} -300 -530 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 80 -200 0 0 {name=Q61
model=npn13G2l
spiceprefix=X
Nx=1
m=4
selft=0}
C {sg13g2_pr/npn13G2l.sym} 280 -200 0 1 {name=Q62
model=npn13G2l
spiceprefix=X
Nx=1
m=4
selft=0}
C {sg13g2_pr/npn13G2l.sym} 80 -320 0 0 {name=Q45
model=npn13G2l
spiceprefix=X
Nx=1
m=4
selft=0}
C {sg13g2_pr/npn13G2l.sym} 280 -320 0 1 {name=Q46
model=npn13G2l
spiceprefix=X
Nx=1
m=4
selft=0}
C {devices/res.sym} 100 -420 0 0 {name=RL_P
value=200}
C {devices/res.sym} 260 -420 0 0 {name=RL_N
value=200}
C {devices/vsource.sym} -150 -460 0 0 {name=VCC
value="DC 3.3"}
C {devices/isource.sym} 180 -100 0 0 {name=ITAIL
value="DC 6m"}
C {devices/vsource.sym} -50 -200 0 0 {name=VIN_P
value="DC 0.9 SIN(0.9 0.001 77e9)"}
C {devices/vsource.sym} 400 -200 0 0 {name=VIN_N
value="DC 0.9 SIN(0.9 -0.001 77e9)"}
C {devices/vsource.sym} -150 -320 0 0 {name=VCASC
value="DC 2.0"}
N 100 -290 100 -230 {lab=LNA_MIDP}
N 260 -290 260 -230 {lab=LNA_MIDN}
N 100 -170 260 -170 {lab=LNA_TAIL}
N 180 -170 180 -120 {lab=LNA_TAIL}
N 100 -390 100 -350 {lab=LNA_OUTP}
N 260 -390 260 -350 {lab=LNA_OUTN}
N 100 -450 260 -450 {lab=VCC}
C {lab_pin.sym} 100 -230 0 0 {name=p1 sig_type=std_logic lab=LNA_MIDP}
C {lab_pin.sym} 60 -200 0 0 {name=p2 sig_type=std_logic lab=INP}
C {lab_pin.sym} 100 -170 0 0 {name=p3 sig_type=std_logic lab=LNA_TAIL}
C {lab_pin.sym} 100 -200 0 0 {name=p4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 260 -230 0 0 {name=p5 sig_type=std_logic lab=LNA_MIDN}
C {lab_pin.sym} 300 -200 0 0 {name=p6 sig_type=std_logic lab=INN}
C {lab_pin.sym} 260 -170 0 0 {name=p7 sig_type=std_logic lab=LNA_TAIL}
C {lab_pin.sym} 260 -200 0 0 {name=p8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 100 -350 0 0 {name=p9 sig_type=std_logic lab=LNA_OUTP}
C {lab_pin.sym} 60 -320 0 0 {name=p10 sig_type=std_logic lab=LNA_VCB}
C {lab_pin.sym} 100 -290 0 0 {name=p11 sig_type=std_logic lab=LNA_MIDP}
C {lab_pin.sym} 100 -320 0 0 {name=p12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 260 -350 0 0 {name=p13 sig_type=std_logic lab=LNA_OUTN}
C {lab_pin.sym} 300 -320 0 0 {name=p14 sig_type=std_logic lab=LNA_VCB}
C {lab_pin.sym} 260 -290 0 0 {name=p15 sig_type=std_logic lab=LNA_MIDN}
C {lab_pin.sym} 260 -320 0 0 {name=p16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 100 -450 0 0 {name=p17 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 100 -390 0 0 {name=p18 sig_type=std_logic lab=LNA_OUTP}
C {lab_pin.sym} 260 -450 0 0 {name=p19 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 260 -390 0 0 {name=p20 sig_type=std_logic lab=LNA_OUTN}
N -150 -490 -130 -490 {lab=VCC}
N -150 -430 -130 -430 {lab=GND}
N 180 -130 200 -130 {lab=LNA_TAIL}
N 180 -70 200 -70 {lab=GND}
N -50 -230 -30 -230 {lab=INP}
N -50 -170 -30 -170 {lab=GND}
N 400 -230 420 -230 {lab=INN}
N 400 -170 420 -170 {lab=GND}
N -150 -350 -130 -350 {lab=LNA_VCB}
N -150 -290 -130 -290 {lab=GND}
C {lab_pin.sym} -130 -490 0 0 {name=p21 sig_type=std_logic lab=VCC}
C {lab_pin.sym} -130 -430 0 0 {name=p22 sig_type=std_logic lab=GND}
C {lab_pin.sym} 200 -130 0 0 {name=p23 sig_type=std_logic lab=LNA_TAIL}
C {lab_pin.sym} 200 -70 0 0 {name=p24 sig_type=std_logic lab=GND}
C {lab_pin.sym} -30 -230 0 0 {name=p25 sig_type=std_logic lab=INP}
C {lab_pin.sym} -30 -170 0 0 {name=p26 sig_type=std_logic lab=GND}
C {lab_pin.sym} 420 -230 0 0 {name=p27 sig_type=std_logic lab=INN}
C {lab_pin.sym} 420 -170 0 0 {name=p28 sig_type=std_logic lab=GND}
C {lab_pin.sym} -130 -350 0 0 {name=p29 sig_type=std_logic lab=LNA_VCB}
C {lab_pin.sym} -130 -290 0 0 {name=p30 sig_type=std_logic lab=GND}
C {simulator_commands_shown.sym} -300 -500 0 0 {name=SIM
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
.tran 0.2p 2n
.meas tran vswing_outp pp v(lna_outp) from=1n to=2n
.meas tran vswing_inp pp v(inp) from=1n to=2n
)"}
