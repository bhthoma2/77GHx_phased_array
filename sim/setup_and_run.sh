#!/bin/bash
# ============================================================
# 77 GHz Phased Array Vibrometer - Simulation Setup & Run
# ============================================================
# This script sets up the IHP SG13G2 PDK and runs the LNA sim.
# Run on a personal Linux machine (not ADI corporate).
#
# Prerequisites: Docker installed
# ============================================================

set -e

echo "=============================================="
echo " 77 GHz Phased Array - Simulation Setup"
echo "=============================================="

# --- Step 1: Pull IIC-OSIC-TOOLS Docker Image ---
echo ""
echo "[1/5] Pulling IIC-OSIC-TOOLS Docker image..."
echo "       (This includes xschem, ngspice, Xyce, KLayout, IHP PDK)"
docker pull hpretl/iic-osic-tools:latest

# --- Step 2: Clone IHP PDK (if not using Docker's built-in) ---
echo ""
echo "[2/5] Setting up PDK paths..."
export PDK_ROOT="${HOME}/.volare"
export PDK="ihp-sg13g2"

# --- Step 3: Create working directory ---
SIMDIR="$(cd "$(dirname "$0")" && pwd)"
echo ""
echo "[3/5] Simulation directory: ${SIMDIR}"

# --- Step 4: Run simulation in Docker ---
echo ""
echo "[4/5] Running LNA simulation in Docker container..."
echo ""

docker run --rm \
    -v "${SIMDIR}:/sim" \
    -w /sim \
    hpretl/iic-osic-tools:latest \
    bash -c '
        echo "=== Inside Docker container ==="
        echo "ngspice version:"
        ngspice --version | head -3
        echo ""
        echo "PDK_ROOT=$PDK_ROOT"
        echo "PDK=$PDK"
        echo ""
        echo "=== Running RXAMP_77GD_TB simulation ==="
        ngspice -b RXAMP_77GD_TB.spice 2>&1 | tee sim_output.log
        echo ""
        echo "=== Simulation complete ==="
    '

# --- Step 5: Report results ---
echo ""
echo "[5/5] Results:"
echo "  - sim_output.log    : Full simulation log"
echo "  - gain_plot.ps      : S21 gain vs frequency"
echo "  - tran_plot.ps      : Time-domain waveforms"
echo ""
echo "=============================================="
echo " To run with FULL PDK models (accurate mmWave):"
echo "=============================================="
echo ""
echo " 1. Edit RXAMP_77GD_TB.spice"
echo " 2. Comment out the simplified models section"
echo " 3. Uncomment the .lib PDK lines at the top"
echo " 4. Re-run this script"
echo ""
echo " Or open in xschem interactively:"
echo "   docker run -it --rm -e DISPLAY=\$DISPLAY \\"
echo "     -v /tmp/.X11-unix:/tmp/.X11-unix \\"
echo "     -v ${SIMDIR}:/sim -w /sim \\"
echo "     hpretl/iic-osic-tools:latest \\"
echo "     xschem ../xschem/RXAMP_77GD_TB.sch"
echo ""
