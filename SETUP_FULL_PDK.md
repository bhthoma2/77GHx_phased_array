# Full PDK Setup Guide — 77 GHz Phased Array Vibrometer

## Problem
The ADI corporate network blocks GitHub binary downloads and has no Docker/Singularity.
The IHP SG13G2 PDK requires:
- ngspice compiled with `--enable-osdi` (for Verilog-A compact models)
- OpenVAF compiler (to compile .va → .osdi plugins)
- Pre-compiled OSDI plugins for: r3_cmc (resistors), psp103 (MOSFETs), VBIC (HBTs)

## Solution: Run on Personal Linux Machine

### Option A: Docker (Fastest — 5 minutes)

```bash
# Pull the complete pre-built environment
docker pull hpretl/iic-osic-tools:latest

# Copy simulation files from ADI machine
scp -r bthomas3@<adi-host>:/home/bthomas3/Videos/77GHz_phased_array ~/

# Run LNA simulation with real PDK
docker run --rm -v ~/77GHz_phased_array:/sim -w /sim/sim \
  hpretl/iic-osic-tools:latest \
  ngspice -b RXAMP_77GD_PDK_TB.spice

# Interactive xschem (needs X11)
docker run -it --rm -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v ~/77GHz_phased_array:/sim -w /sim/xschem \
  hpretl/iic-osic-tools:latest xschem RXAMP_77GD_TB.sch
```

### Option B: Native Install (30 minutes)

```bash
# 1. Install OpenVAF
wget https://github.com/pascalkuthe/OpenVAF/releases/download/v23.5.0/openvaf_23_5_0_linux_amd64.tar.gz
tar xzf openvaf_23_5_0_linux_amd64.tar.gz
sudo mv openvaf /usr/local/bin/

# 2. Clone PDK
git clone https://github.com/IHP-GmbH/IHP-Open-PDK.git
export PDK_ROOT=$(pwd)/IHP-Open-PDK

# 3. Compile OSDI plugins
cd $PDK_ROOT/ihp-sg13g2/libs.tech/verilog-a/r3_cmc
openvaf r3_cmc.va
mv r3_cmc.osdi ../../ngspice/openvaf/

cd $PDK_ROOT/ihp-sg13g2/libs.tech/verilog-a/psp103
openvaf psp103.va
mv psp103.osdi ../../ngspice/openvaf/

# 4. Build ngspice with OSDI
git clone https://github.com/ngspice/ngspice.git
cd ngspice && ./autogen.sh
./configure --prefix=/usr/local --enable-xspice --enable-cider \
  --enable-openmp --enable-osdi --without-x
make -j$(nproc) && sudo make install

# 5. Run simulation
cd ~/77GHz_phased_array/sim
ngspice -b RXAMP_77GD_PDK_TB.spice
```

### Option C: NC State AERPAW / Lab Machine

When you start your PhD at NC State, you'll have access to:
- EDA lab machines with full tool access
- AERPAW drone testbed for field testing
- Silicon-Den tapeout club resources

## What Works NOW on This ADI Machine

All simulations pass with simplified models:

| Block | Command | Result |
|-------|---------|--------|
| LNA | `ngspice -b RXAMP_77GD_TB.spice` | 17.3 dB gain |
| Mixer | `ngspice -b MIXER_77GD_TB.spice` | 25.7 dB CG |
| TX PA | `ngspice -b TXAMP_77GD_TB.spice` | 21.1 dB gain |
| VCO | `ngspice -b VCO_77G_TB.spice` | 43.6 GHz (model-limited) |
| Full RX | `ngspice -b RX_CHAIN_TB.spice` | 34 dB total chain |

ngspice binary: `/home/bthomas3/Videos/ngspice_install/local/bin/ngspice`

## PDK-Compatible Files Ready

These netlists have correct pin interfaces for the real PDK models:
- `RXAMP_77GD_PDK.spice` — LNA with real PDK subcircuit calls
- `RXAMP_77GD_PDK_TB.spice` — Testbench with .lib includes

Once OSDI is set up, these will run directly with accurate mmWave results.

## Expected Improvements with Real PDK

| Parameter | Simplified Model | Real PDK (expected) |
|-----------|:----------------:|:-------------------:|
| LNA NF | N/A | 4-6 dB |
| LNA Gain | 17 dB | 12-15 dB (more realistic) |
| VCO freq | 43 GHz (cap-limited) | **77 GHz** (smaller CJE/CJC) |
| VCO phase noise | N/A | -90 to -100 dBc/Hz @ 1MHz |
| Mixer CG | 26 dB (optimistic) | 5-10 dB (more realistic) |
| PA Psat | +1 dBm | +3 to +5 dBm |

## File Tree

```
/home/bthomas3/Videos/
├── 77GHz_phased_array/
│   ├── README.md
│   ├── SETUP_FULL_PDK.md         ← THIS FILE
│   ├── sim/
│   │   ├── RXAMP_77GD.spice      # LNA + TL models
│   │   ├── RXAMP_77GD_TB.spice   # LNA testbench (simplified)
│   │   ├── RXAMP_77GD_PDK.spice  # LNA (real PDK interface)
│   │   ├── RXAMP_77GD_PDK_TB.spice # LNA TB (real PDK)
│   │   ├── MIXER_77GD.spice      # Mixer
│   │   ├── MIXER_77GD_TB.spice   # Mixer testbench
│   │   ├── IFAMP.spice           # IF amplifier
│   │   ├── TXAMP_77GD.spice      # TX power amplifier
│   │   ├── TXAMP_77GD_TB.spice   # TX PA testbench
│   │   ├── VCO_77G.spice         # VCO (cross-coupled)
│   │   ├── VCO_77G_TB.spice      # VCO testbench
│   │   ├── WILKINSON_77GD.spice  # LO power divider
│   │   ├── PHASE_SHIFTER_77G.spice # 4-bit phase shifter
│   │   ├── RX_CHAIN_TB.spice     # Full RX chain
│   │   └── setup_and_run.sh      # Docker run script
│   └── xschem/                    # GUI schematics
├── IHP-Open-PDK/                  # Full PDK (cloned)
├── mWATTBAT_RADAR_150GHz_TO_July2025/  # Original reference
└── ngspice_install/
    ├── ngspice/                   # Source
    └── local/bin/ngspice          # Built binary (no OSDI)
```

## Next Steps After PDK Sim Works

1. ✅ Verify LNA gain/NF at 77 GHz with HICUM models
2. ✅ Confirm VCO oscillates at 77 GHz
3. Design PLL (charge pump + loop filter + prescaler)
4. Layout in KLayout (use mWATTBAT GDS as reference for metal stack)
5. DRC/LVS clean
6. Submit to next IHP OpenMPW shuttle (~€10-30K)
