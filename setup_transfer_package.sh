#!/bin/bash
# =============================================================================
# Run this on your PERSONAL machine (with Docker)
# Creates a tarball with ngspice + OSDI plugins for the ADI machine
# Usage: bash setup_transfer_package.sh
# Output: ~/ngspice_pdk_transfer.tar.gz
# =============================================================================

set -e

OUTDIR=~/ngspice_pdk_transfer
rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"/{osdi,libs}

echo "=== Pulling Docker image (this takes a while first time) ==="
docker pull hpretl/iic-osic-tools:latest

echo "=== Extracting files from container ==="
docker run --rm -v "$OUTDIR":/out hpretl/iic-osic-tools:latest bash -c '
set -e

# ngspice binary - known locations in iic-osic-tools
NGSPICE=$(which ngspice 2>/dev/null || echo /foss/tools/ngspice/bin/ngspice)
echo "ngspice: $NGSPICE"
cp "$NGSPICE" /out/ngspice
ngspice --version 2>&1 | head -3 > /out/version.txt
cat /out/version.txt

# OSDI plugins - known PDK location
PDK_OSDI=/foss/pdks/ihp-sg13g2/libs.tech/ngspice/openvaf
if [ -d "$PDK_OSDI" ]; then
    cp "$PDK_OSDI"/*.osdi /out/osdi/
    echo "OSDI from: $PDK_OSDI"
    ls /out/osdi/
else
    # Fallback: search only in /foss (not entire filesystem)
    find /foss -name "*.osdi" -exec cp {} /out/osdi/ \; 2>/dev/null
    echo "OSDI found:"
    ls /out/osdi/ 2>/dev/null || echo "  NONE - see troubleshooting below"
fi

# OpenVAF binary
OPENVAF=$(which openvaf 2>/dev/null || echo "")
if [ -n "$OPENVAF" ]; then
    cp "$OPENVAF" /out/openvaf
    echo "openvaf: $OPENVAF"
fi

# Shared libs needed by ngspice
ldd "$NGSPICE" > /out/ldd_info.txt
ldd "$NGSPICE" | grep "=> /" | awk "{print \$3}" | while read lib; do
    cp -L "$lib" /out/libs/ 2>/dev/null || true
done

# spinit config
SPINIT=$(dirname "$NGSPICE")/../share/ngspice/scripts/spinit
if [ -f "$SPINIT" ]; then
    cp "$SPINIT" /out/spinit
    echo "spinit: $SPINIT"
fi

echo "=== Extraction complete ==="
'

echo "=== Creating install script ==="
cat > "$OUTDIR/install_on_adi.csh" << 'EOF'
#!/bin/tcsh
# Source this on the ADI machine after extracting the tarball

set INSTALL_DIR = ~/ngspice_pdk
mkdir -p $INSTALL_DIR/bin
mkdir -p $INSTALL_DIR/lib/ngspice

cp ngspice $INSTALL_DIR/bin/
chmod +x $INSTALL_DIR/bin/ngspice
cp osdi/*.osdi $INSTALL_DIR/lib/ngspice/
cp libs/* $INSTALL_DIR/lib/ >& /dev/null

# Tell ngspice where OSDI plugins live
echo 'unset ngbehavior' > ~/.spiceinit
foreach f ($INSTALL_DIR/lib/ngspice/*.osdi)
  echo "osdi $f" >> ~/.spiceinit
end

echo ""
echo "Installed to: $INSTALL_DIR"
echo "Test: $INSTALL_DIR/bin/ngspice -b test_pdk.spice"
echo "If lib errors: setenv LD_LIBRARY_PATH ${INSTALL_DIR}/lib"
EOF

echo "=== Creating test netlist ==="
cat > "$OUTDIR/test_pdk.spice" << 'EOF'
** Quick PDK load test
.lib /home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/cornerHBT.lib hbt_typ
.lib /home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/cornerRES.lib res_typ
.lib /home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/cornerCAP.lib cap_typ

VCC vcc 0 2.4
XQ1 vcc base 0 0 npn13G2l Nx=4 le=2.5e-6
Rbase vcc base 10k

.op
.control
run
echo "=== PDK LOAD SUCCESSFUL ==="
echo "Ic ="
print @xq1.xnpn13g2l.qnpn13g2l[ic]
.endc
.end
EOF

echo "=== Packaging tarball ==="
cd ~
tar czf ngspice_pdk_transfer.tar.gz ngspice_pdk_transfer/
ls -lh ~/ngspice_pdk_transfer.tar.gz

echo ""
echo "DONE! Email ~/ngspice_pdk_transfer.tar.gz to your ADI machine."
echo "Then: tar xzf ngspice_pdk_transfer.tar.gz && cd ngspice_pdk_transfer && source install_on_adi.csh"
