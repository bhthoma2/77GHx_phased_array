v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Bandgap + Bias Generator Testbench} -300 -600 0 0 0.5 0.5 {}
T {VREF=1.2V (typ), TC < 50ppm/C, PSRR > 40dB} -300 -560 0 0 0.3 0.3 {layer=7}
T {Expected: VREF stable across -40 to 125C, bias mirrors track reference} -300 -530 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 80 -250 0 0 {name=Q_BG1
model=npn13G2l
spiceprefix=X
Nx=1
m=1
selft=0}
C {sg13g2_pr/npn13G2l.sym} 220 -250 0 0 {name=Q_BG2
model=npn13G2l
spiceprefix=X
Nx=1
m=8
selft=0}
C {sg13g2_pr/npn13G2l.sym} 80 -400 0 0 {name=Q_MIR1
model=npn13G2l
spiceprefix=X
Nx=1
m=4
selft=0}
C {sg13g2_pr/npn13G2l.sym} 220 -400 0 0 {name=Q_MIR2
model=npn13G2l
spiceprefix=X
Nx=1
m=4
selft=0}
C {devices/res.sym} 100 -170 0 0 {name=R1
value=10k}
C {devices/res.sym} 240 -170 0 0 {name=R2
value=1.25k}
C {devices/res.sym} 160 -320 0 0 {name=RPTAT
value=5k}
C {devices/vsource.sym} -100 -400 0 0 {name=VCC
value="DC 3.3"}
C {devices/res.sym} 100 -470 0 0 {name=RLOAD1
value=10k}
C {devices/res.sym} 240 -470 0 0 {name=RLOAD2
value=10k}
N 100 -280 100 -250 {lab=BG_C1}
N 240 -280 240 -250 {lab=BG_C2}
N 100 -220 100 -200 {lab=GND}
N 240 -220 240 -200 {lab=GND}
N 100 -140 100 -120 {lab=GND}
N 240 -140 240 -120 {lab=GND}
N 60 -250 60 -220 {lab=VREF}
N 200 -250 200 -220 {lab=VREF}
N 160 -350 160 -320 {lab=VREF}
N 160 -290 160 -270 {lab=VPTAT}
N 100 -430 100 -400 {lab=IBIAS1}
N 240 -430 240 -400 {lab=IBIAS2}
N 60 -400 60 -370 {lab=VREF}
N 200 -400 200 -370 {lab=VREF}
N 100 -500 100 -470 {lab=VCC}
N 240 -500 240 -470 {lab=VCC}
C {lab_pin.sym} 100 -280 0 0 {name=p1 sig_type=std_logic lab=BG_C1}
C {lab_pin.sym} 240 -280 0 0 {name=p2 sig_type=std_logic lab=BG_C2}
C {lab_pin.sym} 60 -250 0 0 {name=p3 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 100 -430 0 0 {name=p4 sig_type=std_logic lab=IBIAS1}
C {lab_pin.sym} 240 -430 0 0 {name=p5 sig_type=std_logic lab=IBIAS2}
C {lab_pin.sym} 100 -500 0 0 {name=p6 sig_type=std_logic lab=VCC}
C {simulator_commands_shown.sym} -300 -500 0 0 {name=SIM
simulator=ngspice
only_toplevel=false
value="tcleval(
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.options gmin=1e-10 reltol=1e-4
.op
.dc temp -40 125 5
.meas dc vref_nom find v(vref) at=27
.meas dc vref_min min v(vref)
.meas dc vref_max max v(vref)
.meas dc tc param='1e6*(vref_max-vref_min)/vref_nom/165'
)"}