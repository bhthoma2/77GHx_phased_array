v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VGA Testbench - Gilbert-Cell Variable Gain Amplifier} -300 -600 0 0 0.5 0.5 {}
T {Gain range 0-30dB, VCC=3.3V, ITAIL=2mA} -300 -560 0 0 0.3 0.3 {layer=7}
T {Expected: gain varies monotonically with VCTRL, BW > 10MHz at all settings} -300 -530 0 0 0.3 0.3 {layer=7}
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
C {sg13g2_pr/npn13G2l.sym} 50 -350 0 0 {name=Q3
model=npn13G2l
spiceprefix=X
Nx=1
m=1
selft=0}
C {sg13g2_pr/npn13G2l.sym} 150 -350 0 1 {name=Q4
model=npn13G2l
spiceprefix=X
Nx=1
m=1
selft=0}
C {sg13g2_pr/npn13G2l.sym} 210 -350 0 0 {name=Q5
model=npn13G2l
spiceprefix=X
Nx=1
m=1
selft=0}
C {sg13g2_pr/npn13G2l.sym} 310 -350 0 1 {name=Q6
model=npn13G2l
spiceprefix=X
Nx=1
m=1
selft=0}
C {devices/res.sym} 70 -430 0 0 {name=RLP
value=300}
C {devices/res.sym} 290 -430 0 0 {name=RLN
value=300}
C {devices/vsource.sym} -150 -460 0 0 {name=VCC
value="DC 3.3"}
C {devices/isource.sym} 180 -100 0 0 {name=ITAIL
value="DC 2m"}
C {devices/vsource.sym} -50 -200 0 0 {name=VIN_P
value="DC 0.9 AC 1m"}
C {devices/vsource.sym} 400 -200 0 0 {name=VIN_N
value="DC 0.9 AC -1m"}
C {devices/vsource.sym} -150 -350 0 0 {name=VCTRL
value="DC 0.9"}
N 100 -230 100 -200 {lab=GM_OUTP}
N 260 -230 260 -200 {lab=GM_OUTN}
N 100 -170 260 -170 {lab=TAIL}
N 180 -170 180 -120 {lab=TAIL}
N 70 -320 70 -300 {lab=GM_OUTP}
N 130 -320 130 -300 {lab=GM_OUTP}
N 230 -320 230 -300 {lab=GM_OUTN}
N 290 -320 290 -300 {lab=GM_OUTN}
N 70 -460 70 -430 {lab=VCC}
N 290 -460 290 -430 {lab=VCC}
N 70 -380 70 -350 {lab=OUTP}
N 230 -380 230 -350 {lab=OUTP}
N 130 -380 130 -350 {lab=OUTN}
N 290 -380 290 -350 {lab=OUTN}
C {lab_pin.sym} 60 -200 0 0 {name=p1 sig_type=std_logic lab=INP}
C {lab_pin.sym} 300 -200 0 0 {name=p2 sig_type=std_logic lab=INN}
C {lab_pin.sym} 70 -380 0 0 {name=p3 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 290 -380 0 0 {name=p4 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 30 -350 0 0 {name=p5 sig_type=std_logic lab=VCTRL_P}
C {lab_pin.sym} 330 -350 0 0 {name=p6 sig_type=std_logic lab=VCTRL_N}
C {lab_pin.sym} 170 -350 0 0 {name=p7 sig_type=std_logic lab=VCTRL_N}
C {lab_pin.sym} 190 -350 0 0 {name=p8 sig_type=std_logic lab=VCTRL_P}
C {simulator_commands_shown.sym} -300 -500 0 0 {name=SIM
simulator=ngspice
only_toplevel=false
value="tcleval(
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.options gmin=1e-10 reltol=5e-3
.ac dec 100 1k 1g
.meas ac gain_max max vdb(outp,outn)
.meas ac bw_3db when vdb(outp,outn)=gain_max-3 fall=1
.step param vctrl 0.7 1.1 0.1
)"}