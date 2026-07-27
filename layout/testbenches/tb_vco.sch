v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VCO Testbench - 77 GHz Cross-Coupled Oscillator} -200 -600 0 0 0.5 0.5 {}
T {L=27pH, CVAR=15fF/12fF, ITAIL=5mA} -200 -560 0 0 0.3 0.3 {layer=7}
T {Expected: f_osc ~ 78 GHz, Vswing ~ 1.2 Vpp} -200 -530 0 0 0.3 0.3 {layer=7}
C {sg13g2_pr/npn13G2l.sym} 80 -300 0 0 {name=Q49
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {sg13g2_pr/npn13G2l.sym} 280 -300 0 1 {name=Q50
model=npn13G2l
spiceprefix=X
Nx=1
m=2
selft=0}
C {devices/ind.sym} 100 -420 0 0 {name=L1
value=27p}
C {devices/ind.sym} 260 -420 0 0 {name=L2
value=27p}
C {devices/capa.sym} 180 -330 3 0 {name=CVAR1
value=15f}
C {devices/capa.sym} 180 -200 0 0 {name=CVAR2
value=12f}
C {devices/capa.sym} 180 -140 0 0 {name=CVAR3
value=12f}
C {devices/isource.sym} 180 -100 0 0 {name=ITAIL
value="DC 5m"}
C {devices/vsource.sym} -100 -350 0 0 {name=VCC
value="DC 3.3"}
C {devices/gnd.sym} -100 -330 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 180 -80 0 0 {name=l2 lab=GND}
N 100 -450 100 -480 {lab=VCC}
N 260 -450 260 -480 {lab=VCC}
N 100 -480 260 -480 {lab=VCC}
N 180 -480 180 -480 {lab=VCC}
N -100 -380 -100 -480 {lab=VCC}
N -100 -480 100 -480 {lab=VCC}
N 100 -390 100 -330 {lab=OUTP}
N 260 -390 260 -330 {lab=OUTN}
N 60 -300 60 -300 {lab=OUTN}
N 300 -300 300 -300 {lab=OUTP}
N 100 -300 100 -300 {lab=sub!}
N 260 -300 260 -300 {lab=sub!}
N 100 -270 100 -230 {lab=VCO_TAIL}
N 260 -270 260 -230 {lab=VCO_TAIL}
N 100 -230 260 -230 {lab=VCO_TAIL}
N 180 -230 180 -200 {lab=VCO_TAIL}
N 100 -330 150 -330 {lab=OUTP}
N 210 -330 260 -330 {lab=OUTN}
N 180 -170 180 -160 {lab=GND}
N 180 -120 180 -100 {lab=VCO_TAIL}
C {lab_pin.sym} 60 -300 0 1 {name=p1 sig_type=std_logic lab=OUTN}
C {lab_pin.sym} 300 -300 0 0 {name=p2 sig_type=std_logic lab=OUTP}
C {lab_pin.sym} 100 -300 0 0 {name=p3 sig_type=std_logic lab=sub!}
C {lab_pin.sym} 260 -300 0 0 {name=p4 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 100 -370 0 0 {name=lw1 sig_type=std_logic lab=OUTP}
C {lab_wire.sym} 260 -370 0 0 {name=lw2 sig_type=std_logic lab=OUTN}
C {lab_wire.sym} 180 -480 0 0 {name=lw3 sig_type=std_logic lab=VCC}
C {lab_wire.sym} 180 -230 0 0 {name=lw4 sig_type=std_logic lab=VCO_TAIL}
C {simulator_commands_shown.sym} -200 -480 0 0 {name=SIM
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
.tran 0.2p 1.5n
.meas tran freq_osc trig v(outp) val=3.3 rise=40 targ v(outp) val=3.3 rise=41
.meas tran vswing pp v(outp) from=0.5n to=1.5n
)"}