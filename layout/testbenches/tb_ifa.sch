v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {IF Amplifier Testbench - 2-Stage Differential Amp} -300 -600 0 0 0.5 0.5 {}
T {40dB gain, BW=10MHz, VCC=3.3V, ITAIL=2mA/stage} -300 -560 0 0 0.3 0.3 {layer=7}
T {Expected: Av > 38dB, BW > 8MHz, input-referred noise < 5nV/rtHz} -300 -530 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 80 -200 0 0 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 280 -200 0 1 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 80 -380 0 0 {name=Q3
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 280 -380 0 1 {name=Q4
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {devices/res.sym} 100 -280 0 0 {name=RL1P
value=500}
C {devices/res.sym} 260 -280 0 0 {name=RL1N
value=500}
C {devices/res.sym} 100 -460 0 0 {name=RL2P
value=500}
C {devices/res.sym} 260 -460 0 0 {name=RL2N
value=500}
C {devices/capa.sym} 180 -310 0 0 {name=CC1
value=1p}
C {devices/capa.sym} 220 -310 0 0 {name=CC2
value=1p}
C {devices/vsource.sym} -150 -460 0 0 {name=VCC
value="DC 3.3"}
C {devices/isource.sym} 180 -100 0 0 {name=ITAIL1
value="DC 2m"}
C {devices/isource.sym} 180 -340 0 0 {name=ITAIL2
value="DC 2m"}
C {devices/vsource.sym} -50 -200 0 0 {name=VIN_P
value="DC 0.9 AC 1m"}
C {devices/vsource.sym} 400 -200 0 0 {name=VIN_N
value="DC 0.9 AC -1m"}
N 100 -230 100 -200 {lab=S1_OUTP}
N 260 -230 260 -200 {lab=S1_OUTN}
N 100 -170 260 -170 {lab=TAIL1}
N 180 -170 180 -120 {lab=TAIL1}
N 100 -310 100 -280 {lab=VCC}
N 260 -310 260 -280 {lab=VCC}
N 100 -410 100 -380 {lab=S2_OUTP}
N 260 -410 260 -380 {lab=S2_OUTN}
N 100 -490 260 -490 {lab=VCC}
N 100 -350 260 -350 {lab=TAIL2}
N 180 -350 180 -340 {lab=TAIL2}
C {lab_pin.sym} 60 -200 0 0 {name=p1 sig_type=std_logic lab=INP}
C {lab_pin.sym} 300 -200 0 0 {name=p2 sig_type=std_logic lab=INN}
C {lab_pin.sym} 100 -230 0 0 {name=p3 sig_type=std_logic lab=S1_OUTP}
C {lab_pin.sym} 260 -230 0 0 {name=p4 sig_type=std_logic lab=S1_OUTN}
C {lab_pin.sym} 100 -410 0 0 {name=p5 sig_type=std_logic lab=S2_OUTP}
C {lab_pin.sym} 260 -410 0 0 {name=p6 sig_type=std_logic lab=S2_OUTN}
C {lab_pin.sym} 60 -380 0 0 {name=p7 sig_type=std_logic lab=S1_OUTP}
C {lab_pin.sym} 300 -380 0 0 {name=p8 sig_type=std_logic lab=S1_OUTN}
C {simulator_commands_shown.sym} -300 -500 0 0 {name=SIM
simulator=ngspice
only_toplevel=false
value="tcleval(
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ
.options gmin=1e-10 reltol=5e-3
.ac dec 100 1k 1g
.meas ac gain_db max vdb(s2_outp,s2_outn)
.meas ac bw_3db when vdb(s2_outp,s2_outn)=gain_db-3 fall=1
.noise v(s2_outp,s2_outn) VIN_P dec 100 1k 100meg
)"}