"""
openEMS simulation: CPW transmission line at 77 GHz
IHP SG13G2 metal stack — TM2 signal over TM1 ground plane

Run on Ubuntu machine with openEMS installed:
  python3 em_cpw_77ghz.py

Extracts: Z0, attenuation (dB/mm), effective εr, S-parameters
"""

import os
import numpy as np

try:
    from CSXCAD import ContinuousStructure
    from openEMS import openEMS
    from openEMS.physical_constants import C0, EPS0, MUE0
except ImportError:
    print("ERROR: openEMS not installed. Run this on your Ubuntu machine with:")
    print("  pip install openEMS CSXCAD")
    print("  or use Docker: docker run -v $PWD:/sim hpretl/iic-osic-tools python3 /sim/em_cpw_77ghz.py")
    exit(1)

# === Simulation Parameters ===
f_center = 77e9
f_bw = 40e9
f_start = f_center - f_bw/2
f_stop = f_center + f_bw/2
nf = 401

# === Geometry (IHP SG13G2 CPW on TM2) ===
# Units: µm
unit = 1e-6

# CPW dimensions
sig_w = 5.0       # signal width
gap = 5.0         # signal-to-ground gap
gnd_w = 15.0      # ground strip width
cpw_len = 500.0   # line length for extraction

# Metal stack heights (above substrate)
sub_h = 300.0     # substrate thickness
ox_h = 11.0       # total oxide height to TM2
tm1_h = 8.5       # TM1 height
tm2_h = 11.0      # TM2 height
tm2_t = 3.0       # TM2 thickness
tm1_t = 2.0       # TM1 thickness

# Material properties
eps_ox = 3.9      # SiO2
eps_sub = 11.7    # Si substrate
sigma_al = 3.5e7  # Al conductivity (TM2/TM1)
sigma_sub = 10.0  # Si substrate (10 S/m, moderately doped)

# === Mesh parameters ===
mesh_res = 1.0    # base mesh resolution (µm)
metal_res = 0.5   # mesh near metal edges

# === Build simulation ===
sim_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'em_results')
os.makedirs(sim_path, exist_ok=True)

FDTD = openEMS(NrTS=50000, EndCriteria=1e-5)
FDTD.SetGaussExcite(f_center, f_bw/2)
FDTD.SetBoundaryCond(['PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8', 'PML_8'])

CSX = ContinuousStructure()
FDTD.SetCSX(CSX)

# Domain
x_max = sig_w/2 + gap + gnd_w + 20
x_min = -x_max
y_min = 0
y_max = cpw_len
z_min = -sub_h
z_max = tm2_h + tm2_t + 20

# === Materials ===
# Substrate
sub = CSX.AddMaterial('substrate', epsilon=eps_sub, kappa=sigma_sub)
sub.AddBox([x_min, y_min, z_min], [x_max, y_max, 0])

# Oxide
ox = CSX.AddMaterial('oxide', epsilon=eps_ox)
ox.AddBox([x_min, y_min, 0], [x_max, y_max, tm2_h + tm2_t])

# TM1 ground plane (continuous under signal)
tm1 = CSX.AddConductingSheet('TM1', conductivity=sigma_al, thickness=tm1_t*unit)
tm1.AddBox([x_min, y_min, tm1_h], [x_max, y_max, tm1_h])

# TM2 signal trace
tm2_sig = CSX.AddConductingSheet('TM2_sig', conductivity=sigma_al, thickness=tm2_t*unit)
tm2_sig.AddBox([-sig_w/2, y_min, tm2_h], [sig_w/2, y_max, tm2_h])

# TM2 ground strips
tm2_gndL = CSX.AddConductingSheet('TM2_gndL', conductivity=sigma_al, thickness=tm2_t*unit)
tm2_gndL.AddBox([-(sig_w/2 + gap + gnd_w), y_min, tm2_h], [-(sig_w/2 + gap), y_max, tm2_h])

tm2_gndR = CSX.AddConductingSheet('TM2_gndR', conductivity=sigma_al, thickness=tm2_t*unit)
tm2_gndR.AddBox([(sig_w/2 + gap), y_min, tm2_h], [(sig_w/2 + gap + gnd_w), y_max, tm2_h])

# === Ports ===
port1_x = [-sig_w/2, sig_w/2]
port1_z = [tm1_h, tm2_h]

p1 = FDTD.AddLumpedPort(1, 50, [0, 0.5, tm1_h], [0, 0.5, tm2_h], 'z', excite=1.0)
p2 = FDTD.AddLumpedPort(2, 50, [0, cpw_len-0.5, tm1_h], [0, cpw_len-0.5, tm2_h], 'z')

# === Mesh ===
mesh = CSX.GetGrid()
mesh.SetDeltaUnit(unit)

# X-mesh (fine near signal edges)
mesh.AddLine('x', np.concatenate([
    np.arange(x_min, -(sig_w/2+gap+gnd_w), mesh_res),
    np.arange(-(sig_w/2+gap+gnd_w), -(sig_w/2+gap), metal_res),
    np.arange(-(sig_w/2+gap), -sig_w/2, metal_res),
    np.arange(-sig_w/2, sig_w/2, metal_res),
    np.arange(sig_w/2, sig_w/2+gap, metal_res),
    np.arange(sig_w/2+gap, sig_w/2+gap+gnd_w, metal_res),
    np.arange(sig_w/2+gap+gnd_w, x_max+1, mesh_res),
]))

# Y-mesh
mesh.AddLine('y', np.arange(y_min, y_max+1, 5.0))

# Z-mesh (fine near metals)
mesh.AddLine('z', np.concatenate([
    np.arange(z_min, 0, 20),
    np.arange(0, tm1_h, 1.0),
    [tm1_h - 0.5, tm1_h, tm1_h + 0.5],
    np.arange(tm1_h + 1, tm2_h, 1.0),
    [tm2_h - 0.5, tm2_h, tm2_h + 0.5],
    np.arange(tm2_h + 1, z_max+1, 2.0),
]))

mesh.SmoothMeshLines('all', mesh_res)

# === Run ===
print(f"openEMS CPW simulation: {f_start/1e9:.0f}-{f_stop/1e9:.0f} GHz")
print(f"CPW: w={sig_w}µm, gap={gap}µm, gnd={gnd_w}µm, len={cpw_len}µm")
print(f"Sim path: {sim_path}")

FDTD.Run(sim_path, verbose=3)

# === Post-process ===
freq = np.linspace(f_start, f_stop, nf)
p1.CalcPort(sim_path, freq)
p2.CalcPort(sim_path, freq)

s11 = p1.uf_ref / p1.uf_inc
s21 = p2.uf_ref / p1.uf_inc

# Z0 extraction from S-parameters
Z0 = 50 * np.sqrt((1+s11)*(1-s11) / ((1-s11)*(1+s11) + 1e-30))

# Find 77 GHz index
idx_77 = np.argmin(np.abs(freq - 77e9))

print(f"\n{'='*50}")
print(f"  EM RESULTS at 77 GHz")
print(f"{'='*50}")
print(f"  |S11| = {20*np.log10(np.abs(s11[idx_77])):.1f} dB")
print(f"  |S21| = {20*np.log10(np.abs(s21[idx_77])):.2f} dB")
print(f"  Insertion loss = {-20*np.log10(np.abs(s21[idx_77])):.2f} dB ({cpw_len}µm)")
print(f"  Loss/mm = {-20*np.log10(np.abs(s21[idx_77]))/(cpw_len/1000):.2f} dB/mm")
print(f"  Z0 ≈ {np.abs(Z0[idx_77]):.1f} Ω")
print(f"{'='*50}")

# Save S-parameters
sp_file = os.path.join(sim_path, 'cpw_77ghz.s2p')
with open(sp_file, 'w') as f:
    f.write(f"! CPW S-parameters, IHP SG13G2 TM2\n")
    f.write(f"! w={sig_w}um gap={gap}um gnd={gnd_w}um len={cpw_len}um\n")
    f.write(f"# GHz S RI R 50\n")
    for i in range(nf):
        f.write(f"{freq[i]/1e9:.4f} {s11[i].real:.6f} {s11[i].imag:.6f} "
                f"{s21[i].real:.6f} {s21[i].imag:.6f} "
                f"0 0 0 0\n")
print(f"\nS-parameters saved: {sp_file}")
