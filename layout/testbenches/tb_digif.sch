v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Digital Interface Testbench - CML Output Buffers} -300 -600 0 0 0.5 0.5 {}
T {18-ch CML driver, 50 ohm termination, VCC=3.3V, ITAIL=4mA/ch} -300 -560 0 0 0.3 0.3 {layer=7}
T {Expected: output swing > 400mVpp, rise/fall < 50ps, eye opening > 300mV} -300 -530 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 80 -200 0 0 {name=Q_DRV1
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 220 -200 0 1 {name=Q_DRV2
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {devices/res.sym} 100 -300 0 0 {name=RT_P
value=50}
C {devices/res.sym} 200 -300 0 0 {name=RT_N
value=50}
C {devices/vsource.sym} -150 -400 0 0 {name=VCC
value="DC 3.3"}
C {devices/isource.sym} 150 -100 0 0 {name=ITAIL
value="DC 4m"}
C {devices/vsource.sym} -50 -200 0 0 {name=VDIN
value="DC 0.9 PULSE(0.7 1.1 0 50p 50p 5n 10n)"}
C {devices/res.sym} 100 -380 0 0 {name=RLOAD_P
value=50}
C {devices/res.sym} 200 -380 0 0 {name=RLOAD_N
value=50}
N 100 -230 100 -200 {lab=DOUTP}
N 200 -230 200 -200 {lab=DOUTN}
N 100 -170 200 -170 {lab=DRV_TAIL}
N 150 -170 150 -120 {lab=DRV_TAIL}
N 100 -330 100 -300 {lab=VCC}
N 200 -330 200 -300 {lab=VCC}
N 100 -270 100 -230 {lab=DOUTP}
N 200 -270 200 -230 {lab=DOUTN}
N 100 -410 100 -380 {lab=DOUTP_EXT}
N 200 -410 200 -380 {lab=DOUTN_EXT}
C {lab_pin.sym} 60 -200 0 0 {name=p1 sig_type=std_logic lab=DIN_P}
C {lab_pin.sym} 240 -200 0 0 {name=p2 sig_type=std_logic lab=DIN_N}
C {lab_pin.sym} 100 -230 0 0 {name=p3 sig_type=std_logic lab=DOUTP}
C {lab_pin.sym} 200 -230 0 0 {name=p4 sig_type=std_logic lab=DOUTN}
C {lab_pin.sym} 100 -410 0 0 {name=p5 sig_type=std_logic lab=DOUTP_EXT}
C {lab_pin.sym} 200 -410 0 0 {name=p6 sig_type=std_logic lab=DOUTN_EXT}
C {simulator_commands_shown.sym} -300 -500 0 0 {name=SIM
simulator=ngspice
only_toplevel=false
value="tcleval(
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.options gmin=1e-10 reltol=5e-3 method=gear
.tran 1p 50n
.meas tran vswing pp v(doutp_ext,doutn_ext) from=20n to=50n
.meas tran trise trig v(doutp_ext) val=1.5 rise=2 targ v(doutp_ext) val=1.9 rise=2
.meas tran tfall trig v(doutp_ext) val=1.9 fall=2 targ v(doutp_ext) val=1.5 fall=2
)"}