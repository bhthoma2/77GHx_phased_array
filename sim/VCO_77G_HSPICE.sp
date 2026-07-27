** 77 GHz VCO — FULL IHP SG13G2 PDK via HSPICE
** Run: module load hspice/adi/V-2023.12-SP2; hspice VCO_77G_HSPICE.sp

.param vbic_cje=1 vbic_cjc=1 vbic_cjcp=1 vbic_is=1
.param vbic_ibei=1 vbic_re=1 vbic_rcx=1 vbic_rbx=1 vbic_tf=1
.param temper=27

** === Real PDK HBT Model ===
.include /home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_hbt_mod.lib

** === Resistors (from Xyce models — simple R, no Verilog-A) ===
.include /home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/xyce/models/resistors_mod.lib

** === MIM Cap ===
.subckt cap_cmim PLUS MINUS w=10e-6 l=10e-6 m=1
.param Ctot='1.5e-3*w*l*m'
C1 PLUS MINUS Ctot
.ends cap_cmim

** === TL Models (Z0=85 Ohm, SG13G2 TM2 layer) ===
** TL 105µm choke
.subckt TL_85_105u IN OUT GND
.param Lsec=11.71e-12 Csec=1.61e-15 Rsec=0.582
C1 IN GND 0.805e-15
R1 IN n1 Rsec
L1 n1 n2 Lsec
C2 n2 GND Csec
R2 n2 n3 Rsec
L2 n3 n4 Lsec
C3 n4 GND Csec
R3 n4 n5 Rsec
L3 n5 n6 Lsec
C4 n6 GND Csec
R4 n6 n7 Rsec
L4 n7 OUT Lsec
C5 OUT GND 0.805e-15
.ends

** TL 135µm resonator stub
.subckt TL_85_135u IN OUT GND
.param Lsec=20.07e-12 Csec=2.77e-15 Rsec=0.997
C1 IN GND 1.385e-15
R1 IN n1 Rsec
L1 n1 n2 Lsec
C2 n2 GND Csec
R2 n2 n3 Rsec
L2 n3 n4 Lsec
C3 n4 GND Csec
R3 n4 n5 Rsec
L3 n5 OUT Lsec
C4 OUT GND 1.385e-15
.ends

** === VCO Core ===
.subckt VCO_77G OUTP OUTN VTUNE VCC VSS

XQ1 OUTP OUTN net_tail VSS npn13G2l Nx=2 le=2.5e-6
XQ2 OUTN OUTP net_tail VSS npn13G2l Nx=2 le=2.5e-6

XTLRES1 OUTP res1_end VSS TL_85_135u
XTLRES2 OUTN res2_end VSS TL_85_135u

Cvar1 OUTP net_var1 3fF
Rvar1 net_var1 VTUNE 500
Cvar2 OUTN net_var2 3fF
Rvar2 net_var2 VTUNE 500

Rtail net_tail VSS 200

XTLCHK1 VCC OUTP VSS TL_85_105u
XTLCHK2 VCC OUTN VSS TL_85_105u

Cdecap VCC VSS 3pF

.ends VCO_77G

** === TESTBENCH ===
VCC VCC 0 PWL(0 0 0.1n 2.4)
VTUNE VTUNE 0 1.2

XVCO OUTP OUTN VTUNE VCC 0 VCO_77G

RL1 OUTP 0 500
RL2 OUTN 0 500
Ikick OUTP 0 PWL(0 0 1p 100u 10p 100u 11p 0)

** === Analysis ===
.tran 0.1p 5n

.measure tran vosc_pp pp V(OUTP,OUTN) from=4n to=5n
.measure tran t1 when V(OUTP,OUTN)=0 rise=10
.measure tran t2 when V(OUTP,OUTN)=0 rise=11
.measure tran fosc param='1/(t2-t1)'
.measure tran icc avg I(VCC) from=4n to=5n

.option post accurate
.end
