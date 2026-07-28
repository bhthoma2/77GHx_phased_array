"""
Generate xschem .sch files using lab_pin.sym for all connections.
This avoids wire routing conflicts by connecting everything by name.
"""
import os

OUTDIR = "/home/bthomas3/Videos/77GHz_phased_array/xschem/blocks"

HEADER = """v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
"""

def lab_pin(x, y, rot, mir, name, lab):
    """Place a lab_pin at exact coordinates. rot: 0=right,1=down,2=left,3=up"""
    return f'C {{lab_pin.sym}} {x} {y} {rot} {mir} {{name={name} sig_type=std_logic lab={lab}}}'

def iopin(x, y, rot, mir, name, lab):
    return f"C {{iopin.sym}} {x} {y} {rot} {mir} {{name={name} lab={lab}}}"

def npn_comp(x, y, mir, name, nx=1):
    return f"""C {{sg13g2_pr/npn13G2l.sym}} {x} {y} 0 {mir} {{name={name}
model=npn13G2l
spiceprefix=X
Nx={nx}
El=2.5
selft=0}}"""

def nmos_comp(x, y, mir, name, w="8u", l="200n", ng=4, m=4):
    return f"""C {{sg13g2_pr/sg13_lv_nmos.sym}} {x} {y} 0 {mir} {{name={name}
l={l}
w={w}
ng={ng}
m={m}
model=sg13_lv_nmos
spiceprefix=X
}}"""

def pmos_comp(x, y, mir, name, w="4u", l="200n", ng=2, m=2):
    return f"""C {{sg13g2_pr/sg13_lv_pmos.sym}} {x} {y} 0 {mir} {{name={name}
l={l}
w={w}
ng={ng}
m={m}
model=sg13_lv_pmos
spiceprefix=X
}}"""

def res_comp(x, y, name, value):
    return f"""C {{devices/res.sym}} {x} {y} 0 0 {{name={name}
value={value}}}"""

def isrc_comp(x, y, name, value):
    return f"""C {{devices/isource.sym}} {x} {y} 0 0 {{name={name}
value="DC {value}"}}"""

def wire(x1, y1, x2, y2, lab):
    return f"N {x1} {y1} {x2} {y2} {{lab={lab}}}"

# Pin offset functions
def npn_pins(x, y, mir=0):
    if mir == 0:
        return {'C': (x+20, y-30), 'B': (x-20, y), 'E': (x+20, y+30), 'S': (x+20, y)}
    else:
        return {'C': (x-20, y-30), 'B': (x+20, y), 'E': (x-20, y+30), 'S': (x-20, y)}

def nmos_pins(x, y, mir=0):
    if mir == 0:
        return {'D': (x+20, y-30), 'G': (x-20, y), 'S': (x+20, y+30), 'B': (x+20, y)}
    else:
        return {'D': (x-20, y-30), 'G': (x+20, y), 'S': (x-20, y+30), 'B': (x-20, y)}

def pmos_pins(x, y, mir=0):
    if mir == 0:
        return {'D': (x+20, y+30), 'G': (x-20, y), 'S': (x+20, y-30), 'B': (x+20, y)}
    else:
        return {'D': (x-20, y+30), 'G': (x+20, y), 'S': (x-20, y-30), 'B': (x-20, y)}

# res at (x,y): pin1=(x, y-30), pin2=(x, y+30)
# isource at (x,y): p=(x, y-30), n=(x, y+30)  [current: p→n]

pcnt = [0]
def lp(x, y, rot, lab):
    """Shorthand for lab_pin with auto-incrementing name"""
    pcnt[0] += 1
    return lab_pin(x, y, rot, 0, f"l{pcnt[0]}", lab)


# ============================================================
# ADC_SAR_12B.sch — StrongARM Comparator
# ============================================================
def write_adc():
    pcnt[0] = 0
    content = HEADER
    content += 'T {StrongARM Comparator — 9T CMOS} 0 -750 0 0 0.5 0.5 {}\n'

    # Placement
    # M1(200,-200) mir=0, M2(500,-200) mir=1 — input diff pair
    # M9(350,-50) mir=0 — tail current
    # M5(200,-380) mir=0, M6(500,-380) mir=1 — cross-coupled NMOS latch
    # M3(200,-550) mir=0, M4(500,-550) mir=1 — cross-coupled PMOS latch
    # M7(200,-680) mir=0, M8(500,-680) mir=1 — precharge PMOS

    content += nmos_comp(200, -200, 0, "M1", w="8u", l="200n", ng=4, m=4) + "\n"
    content += nmos_comp(500, -200, 1, "M2", w="8u", l="200n", ng=4, m=4) + "\n"
    content += nmos_comp(350, -50, 0, "M9", w="8u", l="200n", ng=4, m=2) + "\n"
    content += nmos_comp(200, -380, 0, "M5", w="4u", l="200n", ng=2, m=2) + "\n"
    content += nmos_comp(500, -380, 1, "M6", w="4u", l="200n", ng=2, m=2) + "\n"
    content += pmos_comp(200, -550, 0, "M3", w="4u", l="200n", ng=2, m=2) + "\n"
    content += pmos_comp(500, -550, 1, "M4", w="4u", l="200n", ng=2, m=2) + "\n"
    content += pmos_comp(200, -680, 0, "M7", w="2u", l="200n", ng=1, m=2) + "\n"
    content += pmos_comp(500, -680, 1, "M8", w="2u", l="200n", ng=1, m=2) + "\n"

    # IO pins
    content += iopin(80, -200, 0, 1, "p1", "ainp") + "\n"
    content += iopin(620, -200, 0, 0, "p2", "ainn") + "\n"
    content += iopin(350, 30, 0, 0, "p3", "clk") + "\n"
    content += iopin(80, -500, 0, 1, "p4", "doutp") + "\n"
    content += iopin(620, -500, 0, 0, "p5", "doutn") + "\n"
    content += iopin(350, -780, 0, 0, "p6", "vdd") + "\n"
    content += iopin(350, 60, 0, 0, "p7", "vss") + "\n"

    # Pin coordinates
    m1 = nmos_pins(200, -200, 0)   # D=(220,-230), G=(180,-200), S=(220,-170), B=(220,-200)
    m2 = nmos_pins(500, -200, 1)   # D=(480,-230), G=(520,-200), S=(480,-170), B=(480,-200)
    m9 = nmos_pins(350, -50, 0)    # D=(370,-80),  G=(330,-50),  S=(370,-20),  B=(370,-50)
    m5 = nmos_pins(200, -380, 0)   # D=(220,-410), G=(180,-380), S=(220,-350), B=(220,-380)
    m6 = nmos_pins(500, -380, 1)   # D=(480,-410), G=(520,-380), S=(480,-350), B=(480,-380)
    m3 = pmos_pins(200, -550, 0)   # D=(220,-520), G=(180,-550), S=(220,-580), B=(220,-550)
    m4 = pmos_pins(500, -550, 1)   # D=(480,-520), G=(520,-550), S=(480,-580), B=(480,-550)
    m7 = pmos_pins(200, -680, 0)   # D=(220,-650), G=(180,-680), S=(220,-710), B=(220,-680)
    m8 = pmos_pins(500, -680, 1)   # D=(480,-650), G=(520,-680), S=(480,-710), B=(480,-680)

    # Place lab_pins at each device pin
    # M1: D=dn1, G=ainp, S=tail, B=vss
    content += lp(*m1['D'], 3, "dn1") + "\n"
    content += lp(*m1['G'], 0, "ainp") + "\n"
    content += lp(*m1['S'], 1, "tail") + "\n"
    content += lp(*m1['B'], 0, "vss") + "\n"

    # M2: D=dn2, G=ainn, S=tail, B=vss
    content += lp(*m2['D'], 3, "dn2") + "\n"
    content += lp(*m2['G'], 2, "ainn") + "\n"
    content += lp(*m2['S'], 1, "tail") + "\n"
    content += lp(*m2['B'], 2, "vss") + "\n"

    # M9: D=tail, G=clk, S=vss, B=vss
    content += lp(*m9['D'], 3, "tail") + "\n"
    content += lp(*m9['G'], 0, "clk") + "\n"
    content += lp(*m9['S'], 1, "vss") + "\n"
    content += lp(*m9['B'], 0, "vss") + "\n"

    # M5: D=doutp, G=doutn, S=dn1, B=vss
    content += lp(*m5['D'], 3, "doutp") + "\n"
    content += lp(*m5['G'], 0, "doutn") + "\n"
    content += lp(*m5['S'], 1, "dn1") + "\n"
    content += lp(*m5['B'], 0, "vss") + "\n"

    # M6: D=doutn, G=doutp, S=dn2, B=vss
    content += lp(*m6['D'], 3, "doutn") + "\n"
    content += lp(*m6['G'], 2, "doutp") + "\n"
    content += lp(*m6['S'], 1, "dn2") + "\n"
    content += lp(*m6['B'], 2, "vss") + "\n"

    # M3: D=doutp, G=doutn, S=vdd, B=vdd
    content += lp(*m3['D'], 1, "doutp") + "\n"
    content += lp(*m3['G'], 0, "doutn") + "\n"
    content += lp(*m3['S'], 3, "vdd") + "\n"
    content += lp(*m3['B'], 0, "vdd") + "\n"

    # M4: D=doutn, G=doutp, S=vdd, B=vdd
    content += lp(*m4['D'], 1, "doutn") + "\n"
    content += lp(*m4['G'], 2, "doutp") + "\n"
    content += lp(*m4['S'], 3, "vdd") + "\n"
    content += lp(*m4['B'], 2, "vdd") + "\n"

    # M7: D=doutp, G=clk, S=vdd, B=vdd
    content += lp(*m7['D'], 1, "doutp") + "\n"
    content += lp(*m7['G'], 0, "clk") + "\n"
    content += lp(*m7['S'], 3, "vdd") + "\n"
    content += lp(*m7['B'], 0, "vdd") + "\n"

    # M8: D=doutn, G=clk, S=vdd, B=vdd
    content += lp(*m8['D'], 1, "doutn") + "\n"
    content += lp(*m8['G'], 2, "clk") + "\n"
    content += lp(*m8['S'], 3, "vdd") + "\n"
    content += lp(*m8['B'], 2, "vdd") + "\n"

    # Connect iopins with short wires to their lab_pin network
    content += wire(80, -200, 80, -200, "ainp") + "\n"
    content += wire(620, -200, 620, -200, "ainn") + "\n"
    content += wire(350, 30, 350, 30, "clk") + "\n"
    content += wire(80, -500, 80, -500, "doutp") + "\n"
    content += wire(620, -500, 620, -500, "doutn") + "\n"
    content += wire(350, -780, 350, -780, "vdd") + "\n"
    content += wire(350, 60, 350, 60, "vss") + "\n"

    with open(os.path.join(OUTDIR, "ADC_SAR_12B.sch"), "w") as f:
        f.write(content)
    print("Wrote ADC_SAR_12B.sch")


# ============================================================
# IFA_77G.sch — 2-stage direct-coupled diff amp
# ============================================================
def write_ifa():
    pcnt[0] = 0
    content = HEADER
    content += 'T {IFA — 2-Stage IF Amplifier, 44dB} 0 -650 0 0 0.5 0.5 {}\n'

    # Stage 1: Q1(200,-400) mir=0, Q2(400,-400) mir=1
    # Stage 2: Q3(200,-200) mir=0, Q4(400,-200) mir=1
    # RL1(220,-500), RL2(380,-500), RL3(220,-300), RL4(380,-300)
    # ITAIL1(300,-310), ITAIL2(300,-110)

    content += npn_comp(200, -400, 0, "Q1", nx=2) + "\n"
    content += npn_comp(400, -400, 1, "Q2", nx=2) + "\n"
    content += npn_comp(200, -200, 0, "Q3", nx=2) + "\n"
    content += npn_comp(400, -200, 1, "Q4", nx=2) + "\n"
    content += res_comp(220, -500, "RL1", "500") + "\n"
    content += res_comp(380, -500, "RL2", "500") + "\n"
    content += res_comp(220, -300, "RL3", "500") + "\n"
    content += res_comp(380, -300, "RL4", "500") + "\n"
    content += isrc_comp(300, -340, "ITAIL1", "2m") + "\n"
    content += isrc_comp(300, -140, "ITAIL2", "2m") + "\n"

    # IO pins
    content += iopin(80, -400, 0, 1, "p1", "INP") + "\n"
    content += iopin(520, -400, 0, 0, "p2", "INN") + "\n"
    content += iopin(80, -260, 0, 1, "p3", "OUTP") + "\n"
    content += iopin(520, -260, 0, 0, "p4", "OUTN") + "\n"
    content += iopin(300, -600, 0, 0, "p5", "VCC") + "\n"
    content += iopin(300, -40, 0, 0, "p6", "GND") + "\n"
    content += iopin(350, -40, 0, 0, "p7", "sub!") + "\n"

    # Q1 pins: C=(220,-430), B=(180,-400), E=(220,-370), S=(220,-400)
    q1 = npn_pins(200, -400, 0)
    q2 = npn_pins(400, -400, 1)  # C=(380,-430), B=(420,-400), E=(380,-370), S=(380,-400)
    q3 = npn_pins(200, -200, 0)  # C=(220,-230), B=(180,-200), E=(220,-170), S=(220,-200)
    q4 = npn_pins(400, -200, 1)  # C=(380,-230), B=(420,-200), E=(380,-170), S=(380,-200)

    # Q1: C=out1p, B=INP, E=tail1, S=sub!
    content += lp(*q1['C'], 3, "out1p") + "\n"
    content += lp(*q1['B'], 0, "INP") + "\n"
    content += lp(*q1['E'], 1, "tail1") + "\n"
    content += lp(*q1['S'], 0, "sub!") + "\n"

    # Q2: C=out1n, B=INN, E=tail1, S=sub!
    content += lp(*q2['C'], 3, "out1n") + "\n"
    content += lp(*q2['B'], 2, "INN") + "\n"
    content += lp(*q2['E'], 1, "tail1") + "\n"
    content += lp(*q2['S'], 2, "sub!") + "\n"

    # Q3: C=OUTP, B=out1p, E=tail2, S=sub!
    content += lp(*q3['C'], 3, "OUTP") + "\n"
    content += lp(*q3['B'], 0, "out1p") + "\n"
    content += lp(*q3['E'], 1, "tail2") + "\n"
    content += lp(*q3['S'], 0, "sub!") + "\n"

    # Q4: C=OUTN, B=out1n, E=tail2, S=sub!
    content += lp(*q4['C'], 3, "OUTN") + "\n"
    content += lp(*q4['B'], 2, "out1n") + "\n"
    content += lp(*q4['E'], 1, "tail2") + "\n"
    content += lp(*q4['S'], 2, "sub!") + "\n"

    # RL1 at (220,-500): pin1=(220,-530)=VCC, pin2=(220,-470)=out1p
    content += lp(220, -530, 3, "VCC") + "\n"
    content += lp(220, -470, 1, "out1p") + "\n"
    # RL2 at (380,-500): pin1=(380,-530)=VCC, pin2=(380,-470)=out1n
    content += lp(380, -530, 3, "VCC") + "\n"
    content += lp(380, -470, 1, "out1n") + "\n"
    # RL3 at (220,-300): pin1=(220,-330)=VCC, pin2=(220,-270)=OUTP
    content += lp(220, -330, 3, "VCC") + "\n"
    content += lp(220, -270, 1, "OUTP") + "\n"
    # RL4 at (380,-300): pin1=(380,-330)=VCC, pin2=(380,-270)=OUTN
    content += lp(380, -330, 3, "VCC") + "\n"
    content += lp(380, -270, 1, "OUTN") + "\n"

    # ITAIL1 at (300,-340): p=(300,-370)=tail1, n=(300,-310)=GND
    content += lp(300, -370, 3, "tail1") + "\n"
    content += lp(300, -310, 1, "GND") + "\n"
    # ITAIL2 at (300,-140): p=(300,-170)=tail2, n=(300,-110)=GND
    content += lp(300, -170, 3, "tail2") + "\n"
    content += lp(300, -110, 1, "GND") + "\n"

    with open(os.path.join(OUTDIR, "IFA_77G.sch"), "w") as f:
        f.write(content)
    print("Wrote IFA_77G.sch")


# ============================================================
# VGA_77G.sch — Variable-gm amplifier
# ============================================================
def write_vga():
    pcnt[0] = 0
    content = HEADER
    content += 'T {VGA — Variable-gm, 0-31dB} 0 -550 0 0 0.5 0.5 {}\n'

    # Q1(200,-300) mir=0, Q2(400,-300) mir=1, Qtail(300,-150) mir=0
    # RL1(220,-400), RL2(380,-400), RE(320,-60)
    content += npn_comp(200, -300, 0, "Q1", nx=2) + "\n"
    content += npn_comp(400, -300, 1, "Q2", nx=2) + "\n"
    content += npn_comp(300, -150, 0, "Qtail", nx=4) + "\n"
    content += res_comp(220, -400, "RL1", "500") + "\n"
    content += res_comp(380, -400, "RL2", "500") + "\n"
    content += res_comp(320, -60, "RE", "10") + "\n"

    content += iopin(80, -300, 0, 1, "p1", "INP") + "\n"
    content += iopin(520, -300, 0, 0, "p2", "INN") + "\n"
    content += iopin(80, -370, 0, 1, "p3", "OUTP") + "\n"
    content += iopin(520, -370, 0, 0, "p4", "OUTN") + "\n"
    content += iopin(180, -150, 0, 1, "p5", "VCTRL") + "\n"
    content += iopin(300, -500, 0, 0, "p6", "VCC") + "\n"
    content += iopin(320, 20, 0, 0, "p7", "GND") + "\n"
    content += iopin(350, 20, 0, 0, "p8", "sub!") + "\n"

    q1 = npn_pins(200, -300, 0)   # C=(220,-330), B=(180,-300), E=(220,-270)
    q2 = npn_pins(400, -300, 1)   # C=(380,-330), B=(420,-300), E=(380,-270)
    qt = npn_pins(300, -150, 0)   # C=(320,-180), B=(280,-150), E=(320,-120)

    # Q1: C=OUTP, B=INP, E=tail, S=sub!
    content += lp(*q1['C'], 3, "OUTP") + "\n"
    content += lp(*q1['B'], 0, "INP") + "\n"
    content += lp(*q1['E'], 1, "tail") + "\n"
    content += lp(*q1['S'], 0, "sub!") + "\n"

    # Q2: C=OUTN, B=INN, E=tail, S=sub!
    content += lp(*q2['C'], 3, "OUTN") + "\n"
    content += lp(*q2['B'], 2, "INN") + "\n"
    content += lp(*q2['E'], 1, "tail") + "\n"
    content += lp(*q2['S'], 2, "sub!") + "\n"

    # Qtail: C=tail, B=VCTRL, E=etail, S=sub!
    content += lp(*qt['C'], 3, "tail") + "\n"
    content += lp(*qt['B'], 0, "VCTRL") + "\n"
    content += lp(*qt['E'], 1, "etail") + "\n"
    content += lp(*qt['S'], 0, "sub!") + "\n"

    # RL1 at (220,-400): p1=(220,-430)=VCC, p2=(220,-370)=OUTP
    content += lp(220, -430, 3, "VCC") + "\n"
    content += lp(220, -370, 1, "OUTP") + "\n"
    # RL2 at (380,-400): p1=(380,-430)=VCC, p2=(380,-370)=OUTN
    content += lp(380, -430, 3, "VCC") + "\n"
    content += lp(380, -370, 1, "OUTN") + "\n"

    # RE at (320,-60): p1=(320,-90)=etail, p2=(320,-30)=GND
    content += lp(320, -90, 3, "etail") + "\n"
    content += lp(320, -30, 1, "GND") + "\n"

    with open(os.path.join(OUTDIR, "VGA_77G.sch"), "w") as f:
        f.write(content)
    print("Wrote VGA_77G.sch")


# ============================================================
# DIGIF_CML.sch — CML output buffer
# ============================================================
def write_digif():
    pcnt[0] = 0
    content = HEADER
    content += 'T {DIGIF — CML Buffer, 50ohm, 4mA} 0 -450 0 0 0.5 0.5 {}\n'

    content += npn_comp(200, -250, 0, "Q1", nx=2) + "\n"
    content += npn_comp(400, -250, 1, "Q2", nx=2) + "\n"
    content += res_comp(220, -350, "RT1", "50") + "\n"
    content += res_comp(380, -350, "RT2", "50") + "\n"
    content += isrc_comp(300, -160, "ITAIL", "4m") + "\n"

    content += iopin(80, -250, 0, 1, "p1", "DIN_P") + "\n"
    content += iopin(520, -250, 0, 0, "p2", "DIN_N") + "\n"
    content += iopin(80, -310, 0, 1, "p3", "DOUT_P") + "\n"
    content += iopin(520, -310, 0, 0, "p4", "DOUT_N") + "\n"
    content += iopin(300, -430, 0, 0, "p5", "VCC") + "\n"
    content += iopin(300, -70, 0, 0, "p6", "GND") + "\n"
    content += iopin(350, -70, 0, 0, "p7", "sub!") + "\n"

    q1 = npn_pins(200, -250, 0)  # C=(220,-280), B=(180,-250), E=(220,-220)
    q2 = npn_pins(400, -250, 1)  # C=(380,-280), B=(420,-250), E=(380,-220)

    # Q1: C=DOUT_P, B=DIN_P, E=tail, S=sub!
    content += lp(*q1['C'], 3, "DOUT_P") + "\n"
    content += lp(*q1['B'], 0, "DIN_P") + "\n"
    content += lp(*q1['E'], 1, "tail") + "\n"
    content += lp(*q1['S'], 0, "sub!") + "\n"

    # Q2: C=DOUT_N, B=DIN_N, E=tail, S=sub!
    content += lp(*q2['C'], 3, "DOUT_N") + "\n"
    content += lp(*q2['B'], 2, "DIN_N") + "\n"
    content += lp(*q2['E'], 1, "tail") + "\n"
    content += lp(*q2['S'], 2, "sub!") + "\n"

    # RT1 at (220,-350): p1=(220,-380)=VCC, p2=(220,-320)=DOUT_P
    content += lp(220, -380, 3, "VCC") + "\n"
    content += lp(220, -320, 1, "DOUT_P") + "\n"
    # RT2 at (380,-350): p1=(380,-380)=VCC, p2=(380,-320)=DOUT_N
    content += lp(380, -380, 3, "VCC") + "\n"
    content += lp(380, -320, 1, "DOUT_N") + "\n"

    # ITAIL at (300,-160): p=(300,-190)=tail, n=(300,-130)=GND
    content += lp(300, -190, 3, "tail") + "\n"
    content += lp(300, -130, 1, "GND") + "\n"

    with open(os.path.join(OUTDIR, "DIGIF_CML.sch"), "w") as f:
        f.write(content)
    print("Wrote DIGIF_CML.sch")


# ============================================================
# BIAS_BGR.sch — Brokaw Bandgap Reference
# ============================================================
def write_bias():
    pcnt[0] = 0
    content = HEADER
    content += 'T {BIAS — Brokaw BGR, 1.17V} 0 -550 0 0 0.5 0.5 {}\n'

    # Q1(200,-300) mir=0 (1x), Q2(400,-300) mir=0 (8x)
    # R1(220,-200) E1→GND, R2(550,-300) VREF→GND
    # Rfb(310,-380), Rout(450,-380)
    # I1(220,-430), I2(420,-430)
    content += npn_comp(200, -300, 0, "Q1", nx=1) + "\n"
    content += npn_comp(400, -300, 0, "Q2", nx=8) + "\n"
    content += res_comp(220, -200, "R1", "5.4k") + "\n"
    content += res_comp(550, -300, "R2", "18k") + "\n"
    content += res_comp(310, -380, "Rfb", "50") + "\n"
    content += res_comp(470, -380, "Rout", "100") + "\n"
    content += isrc_comp(220, -430, "I1", "200u") + "\n"
    content += isrc_comp(420, -430, "I2", "200u") + "\n"

    content += iopin(600, -300, 0, 0, "p1", "VREF") + "\n"
    content += iopin(320, -530, 0, 0, "p2", "VCC") + "\n"
    content += iopin(320, -80, 0, 0, "p3", "GND") + "\n"
    content += iopin(370, -80, 0, 0, "p4", "sub!") + "\n"

    q1 = npn_pins(200, -300, 0)  # C=(220,-330), B=(180,-300), E=(220,-270), S=(220,-300)
    q2 = npn_pins(400, -300, 0)  # C=(420,-330), B=(380,-300), E=(420,-270), S=(420,-300)

    # Q1: C=c1, B=c1(diode), E=e1, S=sub!
    content += lp(*q1['C'], 3, "c1") + "\n"
    content += lp(*q1['B'], 0, "c1") + "\n"
    content += lp(*q1['E'], 1, "e1") + "\n"
    content += lp(*q1['S'], 0, "sub!") + "\n"

    # Q2: C=c2, B=c2(diode), E=GND, S=sub!
    content += lp(*q2['C'], 3, "c2") + "\n"
    content += lp(*q2['B'], 0, "c2") + "\n"
    content += lp(*q2['E'], 1, "GND") + "\n"
    content += lp(*q2['S'], 0, "sub!") + "\n"

    # R1 at (220,-200): p1=(220,-230)=e1, p2=(220,-170)=GND
    content += lp(220, -230, 3, "e1") + "\n"
    content += lp(220, -170, 1, "GND") + "\n"

    # R2 at (550,-300): p1=(550,-330)=VREF, p2=(550,-270)=GND
    content += lp(550, -330, 3, "VREF") + "\n"
    content += lp(550, -270, 1, "GND") + "\n"

    # Rfb at (310,-380): p1=(310,-410)=c1, p2=(310,-350)=c2
    content += lp(310, -410, 3, "c1") + "\n"
    content += lp(310, -350, 1, "c2") + "\n"

    # Rout at (470,-380): p1=(470,-410)=c2, p2=(470,-350)=VREF
    content += lp(470, -410, 3, "c2") + "\n"
    content += lp(470, -350, 1, "VREF") + "\n"

    # I1 at (220,-430): p=(220,-460)=VCC, n=(220,-400)=c1
    content += lp(220, -460, 3, "VCC") + "\n"
    content += lp(220, -400, 1, "c1") + "\n"
    # I2 at (420,-430): p=(420,-460)=VCC, n=(420,-400)=c2
    content += lp(420, -460, 3, "VCC") + "\n"
    content += lp(420, -400, 1, "c2") + "\n"

    with open(os.path.join(OUTDIR, "BIAS_BGR.sch"), "w") as f:
        f.write(content)
    print("Wrote BIAS_BGR.sch")


# ============================================================
# LVLSHIFT_77G.sch — Emitter follower level shifter
# ============================================================
def write_lvlshift():
    pcnt[0] = 0
    content = HEADER
    content += 'T {Level Shifter — Emitter Follower, -0.85V CM shift} 0 -400 0 0 0.4 0.4 {}\n'

    content += npn_comp(200, -250, 0, "Q1", nx=2) + "\n"
    content += npn_comp(400, -250, 1, "Q2", nx=2) + "\n"
    content += isrc_comp(220, -130, "IEE1", "2m") + "\n"
    content += isrc_comp(380, -130, "IEE2", "2m") + "\n"

    content += iopin(80, -250, 0, 1, "p1", "INP") + "\n"
    content += iopin(520, -250, 0, 0, "p2", "INN") + "\n"
    content += iopin(80, -190, 0, 1, "p3", "OUTP") + "\n"
    content += iopin(520, -190, 0, 0, "p4", "OUTN") + "\n"
    content += iopin(300, -340, 0, 0, "p5", "VCC") + "\n"
    content += iopin(300, -30, 0, 0, "p6", "GND") + "\n"
    content += iopin(350, -30, 0, 0, "p7", "sub!") + "\n"

    q1 = npn_pins(200, -250, 0)  # C=(220,-280), B=(180,-250), E=(220,-220)
    q2 = npn_pins(400, -250, 1)  # C=(380,-280), B=(420,-250), E=(380,-220)

    # Q1: C=VCC, B=INP, E=OUTP, S=sub!
    content += lp(*q1['C'], 3, "VCC") + "\n"
    content += lp(*q1['B'], 0, "INP") + "\n"
    content += lp(*q1['E'], 1, "OUTP") + "\n"
    content += lp(*q1['S'], 0, "sub!") + "\n"

    # Q2: C=VCC, B=INN, E=OUTN, S=sub!
    content += lp(*q2['C'], 3, "VCC") + "\n"
    content += lp(*q2['B'], 2, "INN") + "\n"
    content += lp(*q2['E'], 1, "OUTN") + "\n"
    content += lp(*q2['S'], 2, "sub!") + "\n"

    # IEE1 at (220,-130): p=(220,-160)=OUTP, n=(220,-100)=GND
    content += lp(220, -160, 3, "OUTP") + "\n"
    content += lp(220, -100, 1, "GND") + "\n"
    # IEE2 at (380,-130): p=(380,-160)=OUTN, n=(380,-100)=GND
    content += lp(380, -160, 3, "OUTN") + "\n"
    content += lp(380, -100, 1, "GND") + "\n"

    with open(os.path.join(OUTDIR, "LVLSHIFT_77G.sch"), "w") as f:
        f.write(content)
    print("Wrote LVLSHIFT_77G.sch")


if __name__ == "__main__":
    write_adc()
    write_ifa()
    write_vga()
    write_digif()
    write_bias()
    write_lvlshift()
    print("\nDone — 6 schematics generated with lab_pin connectivity")
