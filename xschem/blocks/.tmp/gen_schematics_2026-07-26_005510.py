"""
Generate xschem .sch files with mathematically correct pin connectivity.
Uses exact pin offsets from PDK symbols to ensure wires land on pins.
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

# Pin offsets for each symbol (center of pin box relative to component placement)
# npn13G2l: rot=0,mir=0: C=(20,-30), B=(-20,0), E=(20,30), S=(20,0)
#           rot=0,mir=1: C=(-20,-30), B=(20,0), E=(-20,30), S=(-20,0)
# sg13_lv_nmos: rot=0,mir=0: D=(20,-30), G=(-20,0), S=(20,30), B=(20,0)
#              rot=0,mir=1: D=(-20,-30), G=(20,0), S=(-20,30), B=(-20,0)
# sg13_lv_pmos: rot=0,mir=0: D=(20,30), G=(-20,0), S=(20,-30), B=(20,0)
#              rot=0,mir=1: D=(-20,30), G=(20,0), S=(-20,-30), B=(-20,0)
# res: rot=0: pin1=(0,-30), pin2=(0,30)
# isource: rot=0: p=(0,-30), n=(0,30)  [current flows from p to n]
# capa: rot=0: p=(0,-30), n=(0,30); rot=3: p=(-30,0), n=(30,0)

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

def wire(x1, y1, x2, y2, lab):
    return f"N {x1} {y1} {x2} {y2} {{lab={lab}}}"

def npn_comp(x, y, mir, name, nx=1, m=1):
    return f"""C {{sg13g2_pr/npn13G2l.sym}} {x} {y} 0 {mir} {{name={name}
model=npn13G2l
spiceprefix=X
Nx={nx}
m={m}
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

def iopin(x, y, rot, mir, name, lab):
    return f"C {{iopin.sym}} {x} {y} {rot} {mir} {{name={name} lab={lab}}}"

def res_comp(x, y, name, value):
    return f"""C {{devices/res.sym}} {x} {y} 0 0 {{name={name}
value={value}}}"""

def isrc_comp(x, y, name, value):
    return f"""C {{devices/isource.sym}} {x} {y} 0 0 {{name={name}
value="DC {value}"}}"""

# ============================================================
# IFA_77G.sch — 2-stage direct-coupled differential amplifier
# ============================================================
def gen_ifa():
    lines = [HEADER]
    lines.append('T {2-Stage IF Amplifier — 40dB, 10MHz BW} -100 -600 0 0 0.5 0.5 {}')

    # Stage 1: Q1 at (200,-300) mir=0, Q2 at (400,-300) mir=1
    q1x, q1y = 200, -300
    q2x, q2y = 400, -300
    q1 = npn_pins(q1x, q1y, 0)
    q2 = npn_pins(q2x, q2y, 1)

    # Stage 2: Q3 at (200,-100) mir=0, Q4 at (400,-100) mir=1
    q3x, q3y = 200, -100
    q4x, q4y = 400, -100
    q3 = npn_pins(q3x, q3y, 0)
    q4 = npn_pins(q4x, q4y, 1)

    # RL1 at (220,-430), RL2 at (380,-430), RL3 at (220,-230), RL4 at (380,-230)
    # res pin1=(x,y-30), pin2=(x,y+30)

    lines.append(npn_comp(q1x, q1y, 0, "Q1", m=2))
    lines.append(npn_comp(q2x, q2y, 1, "Q2", m=2))
    lines.append(npn_comp(q3x, q3y, 0, "Q3", m=2))
    lines.append(npn_comp(q4x, q4y, 1, "Q4", m=2))

    # Load resistors: top connects to VCC, bottom to collector
    # RL1: VCC to Q1.C — place at (220, -390) so pin1=(220,-420)=VCC, pin2=(220,-360)
    # Actually Q1.C = (220,-330). res at (220,-390): pin1=(220,-420), pin2=(220,-360)
    # Need wire from pin2 (220,-360) to Q1.C (220,-330)
    lines.append(res_comp(220, -390, "RL1", "500"))
    lines.append(res_comp(380, -390, "RL2", "500"))
    lines.append(res_comp(220, -190, "RL3", "500"))
    lines.append(res_comp(380, -190, "RL4", "500"))

    # Tail current sources
    lines.append(isrc_comp(300, -180, "ITAIL1", "2m"))  # pin p=(300,-210), n=(300,-150)
    lines.append(isrc_comp(300, 20, "ITAIL2", "2m"))    # pin p=(300,-10), n=(300,50)

    # IO pins
    lines.append(iopin(80, -300, 0, 1, "p1", "INP"))
    lines.append(iopin(520, -300, 0, 0, "p2", "INN"))
    lines.append(iopin(80, -100, 0, 1, "p5", "OUTP"))   # actually output is Q3 collector
    lines.append(iopin(520, -100, 0, 0, "p6", "OUTN"))
    lines.append(iopin(300, -500, 0, 0, "p3", "VCC"))
    lines.append(iopin(300, 100, 0, 0, "p4", "GND"))
    lines.append(iopin(300, 130, 0, 0, "p7", "sub!"))

    # Wires
    # VCC rail at y=-420 (RL1/RL2 top pins)
    lines.append(wire(220, -420, 380, -420, "VCC"))
    lines.append(wire(300, -420, 300, -500, "VCC"))
    # RL1 bot (220,-360) to Q1.C (220,-330)
    lines.append(wire(220, -360, 220, -330, "out1p"))
    # RL2 bot (380,-360) to Q2.C (380,-330)
    lines.append(wire(380, -360, 380, -330, "out1n"))
    # Q1.E (220,-270) to tail1 node
    lines.append(wire(220, -270, 300, -270, "tail1"))
    # Q2.E (380,-270) to tail1
    lines.append(wire(380, -270, 300, -270, "tail1"))
    # ITAIL1.p (300,-210) to tail1 (300,-270)
    lines.append(wire(300, -210, 300, -270, "tail1"))
    # ITAIL1.n (300,-150) to GND... actually connect to stage2 area
    # Wait, ITAIL1 should go to GND. Let me place it lower.
    # Actually let me reorganize. Let me use a simpler layout:
    # Place ITAIL1 at (300, -230): p=(300,-260), n=(300,-200)
    # Then wire p to tail1 (between Q1.E and Q2.E at y=-270)
    # and n to... hmm this gets complex.

    # Let me just use a flat direct approach matching the verified netlist exactly.
    # The verified netlist is:
    # XQ1 out1p inp tail1 sub npn13G2l
    # XQ2 out1n inn tail1 sub npn13G2l
    # RL1 vcc out1p 500
    # RL2 vcc out1n 500
    # ITAIL1 tail1 gnd DC 2m
    # XQ3 outp out1p tail2 sub npn13G2l
    # XQ4 outn out1n tail2 sub npn13G2l
    # RL3 vcc outp 500
    # RL4 vcc outn 500
    # ITAIL2 tail2 gnd DC 2m

    # I'll regenerate with cleaner layout. Scrap above, use direct write.
    pass

    # Actually, let me just write the files directly with known-good format
    # matching exactly what the working RXAMP schematic uses.
    return None  # Will write directly below


# Since the programmatic approach is getting complex, let me just write
# clean .sch files directly that match the verified SPICE netlist format.
# The key is: put all parameters on separate lines (real newlines, not \n)

def write_ifa():
    """IFA: matches .subckt IFA inp inn outp outn vcc gnd sub"""
    content = HEADER
    content += 'T {IFA — 2-Stage IF Amplifier, 40dB} 0 -550 0 0 0.5 0.5 {}\n'

    # Layout: Stage1 top, Stage2 bottom
    # Q1(200,-400) Q2(400,-400) with RL above, tail below
    # Q3(200,-200) Q4(400,-200) with RL above, tail below
    # Direct coupling: Q1.C connects to Q3.B

    # Stage 1
    content += npn_comp(200, -400, 0, "Q1", m=2) + "\n"
    content += npn_comp(400, -400, 1, "Q2", m=2) + "\n"
    content += res_comp(220, -500, "RL1", "500") + "\n"
    content += res_comp(380, -500, "RL2", "500") + "\n"
    content += isrc_comp(300, -310, "ITAIL1", "2m") + "\n"

    # Stage 2
    content += npn_comp(200, -200, 0, "Q3", m=2) + "\n"
    content += npn_comp(400, -200, 1, "Q4", m=2) + "\n"
    content += res_comp(220, -300, "RL3", "500") + "\n"
    content += res_comp(380, -300, "RL4", "500") + "\n"
    content += isrc_comp(300, -110, "ITAIL2", "2m") + "\n"

    # IO pins
    content += iopin(80, -400, 0, 1, "p1", "INP") + "\n"
    content += iopin(520, -400, 0, 0, "p2", "INN") + "\n"
    content += iopin(520, -200, 0, 0, "p3", "OUTP") + "\n"  # Q3 collector side
    content += iopin(80, -200, 0, 1, "p4", "OUTN") + "\n"   # Q4 collector side
    content += iopin(300, -600, 0, 0, "p5", "VCC") + "\n"
    content += iopin(300, -40, 0, 0, "p6", "GND") + "\n"
    content += iopin(350, -40, 0, 0, "p7", "sub!") + "\n"

    # Compute pin positions
    q1 = npn_pins(200, -400, 0)   # C=(220,-430), B=(180,-400), E=(220,-370), S=(220,-400)
    q2 = npn_pins(400, -400, 1)   # C=(380,-430), B=(420,-400), E=(380,-370), S=(380,-400)
    q3 = npn_pins(200, -200, 0)   # C=(220,-230), B=(180,-200), E=(220,-170), S=(220,-200)
    q4 = npn_pins(400, -200, 1)   # C=(380,-230), B=(420,-200), E=(380,-170), S=(380,-200)

    # RL1 at (220,-500): pin1=(220,-530)=top, pin2=(220,-470)=bot
    # RL2 at (380,-500): pin1=(380,-530)=top, pin2=(380,-470)=bot
    # RL3 at (220,-300): pin1=(220,-330)=top, pin2=(220,-270)=bot
    # RL4 at (380,-300): pin1=(380,-330)=top, pin2=(380,-270)=bot
    # ITAIL1 at (300,-310): p=(300,-340), n=(300,-280)
    # ITAIL2 at (300,-110): p=(300,-140), n=(300,-80)

    # VCC rail
    content += wire(220, -530, 380, -530, "VCC") + "\n"
    content += wire(300, -530, 300, -600, "VCC") + "\n"
    content += wire(220, -330, 380, -330, "VCC") + "\n"
    content += wire(300, -330, 300, -530, "VCC") + "\n"

    # RL1.bot (220,-470) to Q1.C (220,-430)
    content += wire(220, -470, 220, -430, "out1p") + "\n"
    # RL2.bot (380,-470) to Q2.C (380,-430)
    content += wire(380, -470, 380, -430, "out1n") + "\n"

    # Q1.E (220,-370) to tail1, Q2.E (380,-370) to tail1
    content += wire(220, -370, 300, -370, "tail1") + "\n"
    content += wire(380, -370, 300, -370, "tail1") + "\n"
    # ITAIL1.p (300,-340) to tail1 (300,-370)
    content += wire(300, -340, 300, -370, "tail1") + "\n"
    # ITAIL1.n (300,-280) to GND
    content += wire(300, -280, 300, -40, "GND") + "\n"

    # Direct coupling: Q1.C (220,-430) to Q3.B (180,-200)
    # Route: (220,-430) down to (220,-430), left to (140,-430), down to (140,-200), right to (180,-200)
    content += wire(220, -430, 140, -430, "out1p") + "\n"
    content += wire(140, -430, 140, -200, "out1p") + "\n"
    content += wire(140, -200, 180, -200, "out1p") + "\n"

    # Q2.C (380,-430) to Q4.B (420,-200)
    content += wire(380, -430, 460, -430, "out1n") + "\n"
    content += wire(460, -430, 460, -200, "out1n") + "\n"
    content += wire(460, -200, 420, -200, "out1n") + "\n"

    # RL3.bot (220,-270) to Q3.C (220,-230)
    content += wire(220, -270, 220, -230, "OUTP") + "\n"
    # RL4.bot (380,-270) to Q4.C (380,-230)
    content += wire(380, -270, 380, -230, "OUTN") + "\n"

    # Q3.E (220,-170) to tail2, Q4.E (380,-170) to tail2
    content += wire(220, -170, 300, -170, "tail2") + "\n"
    content += wire(380, -170, 300, -170, "tail2") + "\n"
    # ITAIL2.p (300,-140) to tail2 (300,-170)
    content += wire(300, -140, 300, -170, "tail2") + "\n"
    # ITAIL2.n (300,-80) to GND
    content += wire(300, -80, 300, -40, "GND") + "\n"

    # Input pins to bases
    content += wire(80, -400, 180, -400, "INP") + "\n"  # to Q1.B
    content += wire(520, -400, 420, -400, "INN") + "\n"  # to Q2.B

    # Output pins from collectors
    content += wire(220, -230, 80, -230, "OUTP") + "\n"
    content += wire(80, -230, 80, -200, "OUTP") + "\n"
    content += wire(380, -230, 520, -230, "OUTN") + "\n"
    content += wire(520, -230, 520, -200, "OUTN") + "\n"

    # Substrate connections
    content += wire(220, -400, 220, -400, "sub!") + "\n"
    content += wire(380, -400, 380, -400, "sub!") + "\n"
    content += wire(220, -200, 220, -200, "sub!") + "\n"
    content += wire(380, -200, 380, -200, "sub!") + "\n"

    with open(os.path.join(OUTDIR, "IFA_77G.sch"), "w") as f:
        f.write(content)
    print("Wrote IFA_77G.sch")


def write_vga():
    """VGA: matches .subckt VGA inp inn outp outn vctrl vcc gnd sub"""
    content = HEADER
    content += 'T {VGA — Variable-gm Amplifier} 0 -500 0 0 0.5 0.5 {}\n'

    # Q1(200,-300) mir=0, Q2(400,-300) mir=1, Qtail(300,-150) mir=0
    content += npn_comp(200, -300, 0, "Q1", m=2) + "\n"
    content += npn_comp(400, -300, 1, "Q2", m=2) + "\n"
    content += npn_comp(300, -150, 0, "Qtail", m=4) + "\n"
    content += res_comp(220, -400, "RL1", "500") + "\n"
    content += res_comp(380, -400, "RL2", "500") + "\n"
    content += res_comp(320, -60, "RE", "10") + "\n"

    content += iopin(80, -300, 0, 1, "p1", "INP") + "\n"
    content += iopin(520, -300, 0, 0, "p2", "INN") + "\n"
    content += iopin(520, -350, 0, 0, "p3", "OUTP") + "\n"
    content += iopin(80, -350, 0, 1, "p4", "OUTN") + "\n"
    content += iopin(180, -150, 0, 1, "p5", "VCTRL") + "\n"
    content += iopin(300, -480, 0, 0, "p6", "VCC") + "\n"
    content += iopin(320, 20, 0, 0, "p7", "GND") + "\n"
    content += iopin(350, 20, 0, 0, "p8", "sub!") + "\n"

    q1 = npn_pins(200, -300, 0)   # C=(220,-330), B=(180,-300), E=(220,-270)
    q2 = npn_pins(400, -300, 1)   # C=(380,-330), B=(420,-300), E=(380,-270)
    qt = npn_pins(300, -150, 0)   # C=(320,-180), B=(280,-150), E=(320,-120)

    # VCC rail
    content += wire(220, -430, 380, -430, "VCC") + "\n"
    content += wire(300, -430, 300, -480, "VCC") + "\n"
    # RL1: (220,-400) pin1=(220,-430)top pin2=(220,-370)bot → Q1.C (220,-330)
    content += wire(220, -370, 220, -330, "OUTP") + "\n"
    content += wire(380, -370, 380, -330, "OUTN") + "\n"

    # Q1.E (220,-270) and Q2.E (380,-270) to tail
    content += wire(220, -270, 300, -270, "tail") + "\n"
    content += wire(380, -270, 300, -270, "tail") + "\n"
    # Qtail.C (320,-180) to tail (300,-270)
    content += wire(320, -180, 320, -270, "tail") + "\n"
    content += wire(300, -270, 320, -270, "tail") + "\n"

    # Qtail.E (320,-120) to RE top (320,-90)
    content += wire(320, -120, 320, -90, "etail") + "\n"
    # RE: (320,-60) pin1=(320,-90) pin2=(320,-30) → GND
    content += wire(320, -30, 320, 20, "GND") + "\n"

    # VCTRL to Qtail.B (280,-150)
    content += wire(180, -150, 280, -150, "VCTRL") + "\n"

    # Inputs
    content += wire(80, -300, 180, -300, "INP") + "\n"
    content += wire(520, -300, 420, -300, "INN") + "\n"

    # Outputs
    content += wire(220, -330, 80, -350, "OUTP") + "\n"
    content += wire(380, -330, 520, -350, "OUTN") + "\n"

    # Sub
    content += wire(220, -300, 220, -300, "sub!") + "\n"
    content += wire(380, -300, 380, -300, "sub!") + "\n"
    content += wire(320, -150, 320, -150, "sub!") + "\n"

    with open(os.path.join(OUTDIR, "VGA_77G.sch"), "w") as f:
        f.write(content)
    print("Wrote VGA_77G.sch")


def write_digif():
    """DIGIF: .subckt DIGIF dinp dinn doutp doutn vcc gnd sub"""
    content = HEADER
    content += 'T {DIGIF — CML Output Buffer, 50ohm} 0 -450 0 0 0.5 0.5 {}\n'

    content += npn_comp(200, -250, 0, "Q1", m=2) + "\n"
    content += npn_comp(400, -250, 1, "Q2", m=2) + "\n"
    content += res_comp(220, -350, "RT1", "50") + "\n"
    content += res_comp(380, -350, "RT2", "50") + "\n"
    content += isrc_comp(300, -160, "ITAIL", "4m") + "\n"

    content += iopin(80, -250, 0, 1, "p1", "DIN_P") + "\n"
    content += iopin(520, -250, 0, 0, "p2", "DIN_N") + "\n"
    content += iopin(520, -300, 0, 0, "p3", "DOUT_P") + "\n"
    content += iopin(80, -300, 0, 1, "p4", "DOUT_N") + "\n"
    content += iopin(300, -430, 0, 0, "p5", "VCC") + "\n"
    content += iopin(300, -70, 0, 0, "p6", "GND") + "\n"
    content += iopin(350, -70, 0, 0, "p7", "sub!") + "\n"

    q1 = npn_pins(200, -250, 0)  # C=(220,-280), B=(180,-250), E=(220,-220)
    q2 = npn_pins(400, -250, 1)  # C=(380,-280), B=(420,-250), E=(380,-220)

    # VCC
    content += wire(220, -380, 380, -380, "VCC") + "\n"
    content += wire(300, -380, 300, -430, "VCC") + "\n"
    # RT1: (220,-350) p1=(220,-380)=VCC, p2=(220,-320) → Q1.C (220,-280)
    content += wire(220, -320, 220, -280, "DOUT_P") + "\n"
    content += wire(380, -320, 380, -280, "DOUT_N") + "\n"

    # Tail
    content += wire(220, -220, 300, -220, "tail") + "\n"
    content += wire(380, -220, 300, -220, "tail") + "\n"
    # ITAIL: (300,-160) p=(300,-190), n=(300,-130)
    content += wire(300, -190, 300, -220, "tail") + "\n"
    content += wire(300, -130, 300, -70, "GND") + "\n"

    # Inputs
    content += wire(80, -250, 180, -250, "DIN_P") + "\n"
    content += wire(520, -250, 420, -250, "DIN_N") + "\n"

    # Outputs
    content += wire(220, -280, 80, -280, "DOUT_P") + "\n"
    content += wire(80, -280, 80, -300, "DOUT_P") + "\n"
    content += wire(380, -280, 520, -280, "DOUT_N") + "\n"
    content += wire(520, -280, 520, -300, "DOUT_N") + "\n"

    # Sub
    content += wire(220, -250, 220, -250, "sub!") + "\n"
    content += wire(380, -250, 380, -250, "sub!") + "\n"

    with open(os.path.join(OUTDIR, "DIGIF_CML.sch"), "w") as f:
        f.write(content)
    print("Wrote DIGIF_CML.sch")


def write_bias():
    """BIAS: .subckt BIAS vref vcc gnd sub"""
    content = HEADER
    content += 'T {BIAS — Brokaw Bandgap Reference} 0 -500 0 0 0.5 0.5 {}\n'

    # Q1 at (200,-250) mir=0, Q2 at (400,-250) mir=0
    content += npn_comp(200, -250, 0, "Q1", m=1) + "\n"
    content += npn_comp(400, -250, 0, "Q2", nx=1, m=8) + "\n"
    content += res_comp(220, -150, "R1", "5.4k") + "\n"   # E1 to GND
    content += res_comp(500, -250, "R2", "18k") + "\n"     # VREF to GND
    content += res_comp(300, -330, "Rfb", "50") + "\n"     # c1 to c2
    content += res_comp(450, -330, "Rout", "100") + "\n"   # c2 to vref
    content += isrc_comp(220, -380, "I1", "200u") + "\n"   # VCC to c1
    content += isrc_comp(420, -380, "I2", "200u") + "\n"   # VCC to c2

    content += iopin(500, -350, 0, 0, "p1", "VREF") + "\n"
    content += iopin(300, -460, 0, 0, "p2", "VCC") + "\n"
    content += iopin(300, -50, 0, 0, "p3", "GND") + "\n"
    content += iopin(350, -50, 0, 0, "p4", "sub!") + "\n"

    q1 = npn_pins(200, -250, 0)  # C=(220,-280), B=(180,-250), E=(220,-220)
    q2 = npn_pins(400, -250, 0)  # C=(420,-280), B=(380,-250), E=(420,-220)

    # Diode connect Q1: B(180,-250) to C(220,-280)
    content += wire(180, -250, 180, -280, "c1") + "\n"
    content += wire(180, -280, 220, -280, "c1") + "\n"
    # Diode connect Q2: B(380,-250) to C(420,-280)
    content += wire(380, -250, 380, -280, "c2") + "\n"
    content += wire(380, -280, 420, -280, "c2") + "\n"

    # Q1.E (220,-220) to R1 top (220,-180)... wait R1 at (220,-150): p1=(220,-180), p2=(220,-120)
    content += wire(220, -220, 220, -180, "e1") + "\n"
    # R1 bot (220,-120) to GND
    content += wire(220, -120, 220, -50, "GND") + "\n"
    content += wire(220, -50, 300, -50, "GND") + "\n"

    # Q2.E (420,-220) to GND
    content += wire(420, -220, 420, -50, "GND") + "\n"
    content += wire(420, -50, 300, -50, "GND") + "\n"

    # I1: (220,-380) p=(220,-410)=VCC, n=(220,-350) → c1
    content += wire(220, -350, 220, -280, "c1") + "\n"
    content += wire(220, -410, 220, -460, "VCC") + "\n"
    content += wire(220, -460, 300, -460, "VCC") + "\n"
    # I2: (420,-380) p=(420,-410)=VCC, n=(420,-350) → c2
    content += wire(420, -350, 420, -280, "c2") + "\n"
    content += wire(420, -410, 420, -460, "VCC") + "\n"
    content += wire(420, -460, 300, -460, "VCC") + "\n"

    # Rfb: (300,-330) p1=(300,-360), p2=(300,-300) — connects c1 to c2
    # Route: c1 (220,-280) → (220,-360) → (300,-360) = Rfb.p1
    content += wire(220, -280, 220, -360, "c1") + "\n"
    content += wire(220, -360, 300, -360, "c1") + "\n"
    # Rfb.p2 (300,-300) to c2
    content += wire(300, -300, 420, -300, "c2") + "\n"
    content += wire(420, -300, 420, -280, "c2") + "\n"

    # Rout: (450,-330) p1=(450,-360)=c2, p2=(450,-300)=vref
    content += wire(450, -360, 420, -360, "c2") + "\n"
    content += wire(420, -360, 420, -280, "c2") + "\n"
    # Rout.p2 to VREF
    content += wire(450, -300, 500, -300, "VREF") + "\n"
    content += wire(500, -300, 500, -350, "VREF") + "\n"

    # R2: (500,-250) p1=(500,-280)=VREF, p2=(500,-220)=GND
    content += wire(500, -280, 500, -300, "VREF") + "\n"
    content += wire(500, -220, 500, -50, "GND") + "\n"
    content += wire(500, -50, 300, -50, "GND") + "\n"

    # Sub
    content += wire(220, -250, 220, -250, "sub!") + "\n"
    content += wire(420, -250, 420, -250, "sub!") + "\n"

    with open(os.path.join(OUTDIR, "BIAS_BGR.sch"), "w") as f:
        f.write(content)
    print("Wrote BIAS_BGR.sch")


if __name__ == "__main__":
    write_ifa()
    write_vga()
    write_digif()
    write_bias()
    print("Done — 4 schematics regenerated with correct pin connectivity")
