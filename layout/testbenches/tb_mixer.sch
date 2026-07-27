v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Mixer Testbench - 77 GHz Gilbert Cell Downconverter} -300 -600 0 0 0.5 0.5 {}
T {RF=77 GHz, LO=77.01 GHz, IF=10 MHz, ITAIL=4mA} -300 -560 0 0 0.3 0.3 {layer=7}
T {Expected: IF swing at IFP/IFN nodes, fIF~10MHz} -300 -530 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 80 -100 0 0 {name=Q41
model=npn13G2l
spiceprefix=X
Nx=1
m=4
selft=0}
C {sg13g2_pr/npn13G2l.sym} 380 -100 0 1 {name=Q42
model=npn13G2l
spiceprefix=X
Nx=1
m=4
selft=0}
C {sg13g2_pr/npn13G2l.sym} 50 -240 0 0 {name=Q65
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 150 -240 0 1 {name=Q66
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 280 -240 0 0 {name=Q67
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 380 -240 0 1 {name=Q68
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {devices/res.sym} 100 -340 0 0 {name=RL_IFP
value=1k}
C {devices/res.sym} 300 -340 0 0 {name=RL_IFN
value=1k}
C {devices/vsource.sym} -100 -380 0 0 {name=VCC
value="DC 3.3"}
C {devices/isource.sym} 230 -20 0 0 {name=ITAIL
value="DC 4m"}
C {devices/vsource.sym} -50 -100 0 0 {name=VRF_P
value="DC 0.9 SIN(0.9 0.01 77e9)"}
C {devices/vsource.sym} 480 -100 0 0 {name=VRF_N
value="DC 0.9 SIN(0.9 -0.01 77e9)"}
C {devices/vsource.sym} -50 -240 0 0 {name=VLO_P
value="DC 0.9 SIN(0.9 0.5 77.01e9)"}
C {devices/vsource.sym} 480 -240 0 0 {name=VLO_N
value="DC 0.9 SIN(0.9 -0.5 77.01e9)"}
N 70 -210 130 -210 {lab=MIX_MIDP}
N 100 -130 100 -210 {lab=MIX_MIDP}
N 300 -210 360 -210 {lab=MIX_MIDN}
N 360 -130 360 -210 {lab=MIX_MIDN}
N 100 -70 360 -70 {lab=MIX_TAIL}
N 230 -70 230 -40 {lab=MIX_TAIL}
N 100 -370 300 -370 {lab=VCC}
C {lab_pin.sym} 100 -130 0 0 {name=p1 sig_type=std_logic lab=MIX_MIDP}
C {lab_pin.sym} 60 -100 0 0 {name=p2 sig_type=std_logic lab=RF_P}
C {lab_pin.sym} 100 -70 0 0 {name=p3 sig_type=std_logic lab=MIX_TAIL}
C {lab_pin.sym} 100 -100 0 0 {name=p4 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 360 -130 0 0 {name=p5 sig_type=std_logic lab=MIX_MIDN}
C {lab_pin.sym} 400 -100 0 0 {name=p6 sig_type=std_logic lab=RF_N}
C {lab_pin.sym} 360 -70 0 0 {name=p7 sig_type=std_logic lab=MIX_TAIL}
C {lab_pin.sym} 360 -100 0 0 {name=p8 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 70 -270 0 0 {name=p9 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 30 -240 0 0 {name=p10 sig_type=std_logic lab=LOP}
C {lab_pin.sym} 70 -210 0 0 {name=p11 sig_type=std_logic lab=MIX_MIDP}
C {lab_pin.sym} 70 -240 0 0 {name=p12 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 130 -270 0 0 {name=p13 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 170 -240 0 0 {name=p14 sig_type=std_logic lab=LON}
C {lab_pin.sym} 130 -210 0 0 {name=p15 sig_type=std_logic lab=MIX_MIDP}
C {lab_pin.sym} 130 -240 0 0 {name=p16 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 300 -270 0 0 {name=p17 sig_type=std_logic lab=IFN}
C {lab_pin.sym} 260 -240 0 0 {name=p18 sig_type=std_logic lab=LON}
C {lab_pin.sym} 300 -210 0 0 {name=p19 sig_type=std_logic lab=MIX_MIDN}
C {lab_pin.sym} 300 -240 0 0 {name=p20 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 360 -270 0 0 {name=p21 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 400 -240 0 0 {name=p22 sig_type=std_logic lab=LOP}
C {lab_pin.sym} 360 -210 0 0 {name=p23 sig_type=std_logic lab=MIX_MIDN}
C {lab_pin.sym} 360 -240 0 0 {name=p24 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 100 -370 0 0 {name=p25 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 100 -310 0 0 {name=p26 sig_type=std_logic lab=IFP}
C {lab_pin.sym} 300 -370 0 0 {name=p27 sig_type=std_logic lab=VCC}
C {lab_pin.sym} 300 -310 0 0 {name=p28 sig_type=std_logic lab=IFN}
N -100 -410 -80 -410 {lab=VCC}
N -100 -350 -80 -350 {lab=GND}
N 230 -50 250 -50 {lab=MIX_TAIL}
N 230 10 250 10 {lab=GND}
N -50 -130 -30 -130 {lab=RF_P}
N -50 -70 -30 -70 {lab=GND}
N 480 -130 500 -130 {lab=RF_N}
N 480 -70 500 -70 {lab=GND}
N -50 -270 -30 -270 {lab=LOP}
N -50 -210 -30 -210 {lab=GND}
N 480 -270 500 -270 {lab=LON}
N 480 -210 500 -210 {lab=GND}
C {lab_pin.sym} -80 -410 0 0 {name=p29 sig_type=std_logic lab=VCC}
C {lab_pin.sym} -80 -350 0 0 {name=p30 sig_type=std_logic lab=GND}
C {lab_pin.sym} 250 -50 0 0 {name=p31 sig_type=std_logic lab=MIX_TAIL}
C {lab_pin.sym} 250 10 0 0 {name=p32 sig_type=std_logic lab=GND}
C {lab_pin.sym} -30 -130 0 0 {name=p33 sig_type=std_logic lab=RF_P}
C {lab_pin.sym} -30 -70 0 0 {name=p34 sig_type=std_logic lab=GND}
C {lab_pin.sym} 500 -130 0 0 {name=p35 sig_type=std_logic lab=RF_N}
C {lab_pin.sym} 500 -70 0 0 {name=p36 sig_type=std_logic lab=GND}
C {lab_pin.sym} -30 -270 0 0 {name=p37 sig_type=std_logic lab=LOP}
C {lab_pin.sym} -30 -210 0 0 {name=p38 sig_type=std_logic lab=GND}
C {lab_pin.sym} 500 -270 0 0 {name=p39 sig_type=std_logic lab=LON}
C {lab_pin.sym} 500 -210 0 0 {name=p40 sig_type=std_logic lab=GND}
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
.tran 1p 50n
.meas tran vswing_ifp pp v(ifp) from=40n to=50n
.meas tran vswing_ifn pp v(ifn) from=40n to=50n
)"}
