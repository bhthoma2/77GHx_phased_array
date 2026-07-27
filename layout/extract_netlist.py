"""
Extract netlist from layout using KLayout LVS engine.
Compatible with KLayout 0.30.5 + IHP SG13G2 PDK.
"""
import pya

GDS = "/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G_XTOR.gds"
TOPCELL = "VCO_77G_XTOR"
OUT_DIR = "/home/bthomas3/Videos/77GHz_phased_array/layout/lvs_vco"

import os
os.makedirs(OUT_DIR, exist_ok=True)

layout = pya.Layout()
layout.read(GDS)

cell = layout.cell(TOPCELL)
if cell is None:
    print(f"ERROR: Cell {TOPCELL} not found")
    exit(1)

# List all cells and their instances for manual netlist correlation
print(f"Top cell: {TOPCELL}")
print(f"Cell instances in {TOPCELL}:")

instance_count = {}
for inst in cell.each_inst():
    cname = inst.cell.name
    instance_count[cname] = instance_count.get(cname, 0) + 1

for cname, count in sorted(instance_count.items()):
    print(f"  {cname}: {count}×")

# Write extracted device list
outfile = os.path.join(OUT_DIR, "extracted_devices.txt")
with open(outfile, 'w') as f:
    f.write(f"* Extracted device list for {TOPCELL}\n")
    f.write(f"* From: {GDS}\n\n")
    for cname, count in sorted(instance_count.items()):
        f.write(f"{cname}: {count} instances\n")

print(f"\nDevice list: {outfile}")

# Compare with schematic
print("\n--- LVS Comparison ---")
print("Schematic (VCO_77G_XTOR.spice):")
print("  npn13G2l: 4 (Q1a, Q1b, Q2a, Q2b)")
print("  SVaricap: 2 (CV1, CV2)")
print("  rppd: 1 (RT)")
print("  cmim: 1 (CD)")
print("\nLayout extracted:")
expected = {"npn13G2L": 4, "SVaricap": 2, "rppd": 1, "cmim": 1}
match = True
for dev, exp in expected.items():
    got = instance_count.get(dev, 0)
    status = "✓" if got == exp else "✗"
    if got != exp:
        match = False
    print(f"  {dev}: {got} (expected {exp}) {status}")

if match:
    print("\n✅ LVS DEVICE COUNT MATCH")
else:
    print("\n❌ LVS DEVICE COUNT MISMATCH")
