"""
Parasitic Extraction (PEX) for 77 GHz Phased Array blocks.
Uses KLayout RC extraction with IHP SG13G2 metal stack parameters.

Metal stack (IHP SG13G2):
  TM2: 3.0µm thick Al, sheet R = 7 mΩ/sq
  TM1: 2.0µm thick Al, sheet R = 10 mΩ/sq
  M5:  0.44µm Cu, sheet R = 50 mΩ/sq
  M4-M1: 0.36µm Cu, sheet R = 70 mΩ/sq
  IMD thickness: ~0.6µm between metals
  SiO2 εr = 3.9
"""
import pya
import os
import math

GDS = "/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G_XTOR.gds"
TOPCELL = "VCO_77G_XTOR"
OUT_DIR = "/home/bthomas3/Videos/77GHz_phased_array/layout/pex_vco"
os.makedirs(OUT_DIR, exist_ok=True)

# IHP SG13G2 metal stack parameters
METALS = {
    'TM2': {'layer': (134, 0), 'rsh': 0.007, 't': 3.0, 'h': 11.0},  # height above substrate
    'TM1': {'layer': (126, 0), 'rsh': 0.010, 't': 2.0, 'h': 8.5},
    'M5':  {'layer': (67, 0),  'rsh': 0.050, 't': 0.44, 'h': 5.5},
    'M4':  {'layer': (50, 0),  'rsh': 0.070, 't': 0.36, 'h': 4.5},
    'M3':  {'layer': (30, 0),  'rsh': 0.070, 't': 0.36, 'h': 3.5},
    'M2':  {'layer': (10, 0),  'rsh': 0.070, 't': 0.36, 'h': 2.5},
    'M1':  {'layer': (8, 0),   'rsh': 0.070, 't': 0.36, 'h': 1.5},
}
EPS_OX = 3.9
EPS0 = 8.854e-12


def extract_wire_parasitics(layout, cell, ly_idx, metal_name, params):
    """Extract R and C for all shapes on a given metal layer."""
    rsh = params['rsh']
    t = params['t'] * 1e-6
    h = params['h'] * 1e-6
    results = []

    region = pya.Region(cell.begin_shapes_rec(ly_idx))
    for poly in region.each():
        bbox = poly.bbox()
        w = bbox.width() * layout.dbu * 1e-6
        l = bbox.height() * layout.dbu * 1e-6
        area = poly.area() * (layout.dbu * 1e-6) ** 2
        perimeter = poly.perimeter() * layout.dbu * 1e-6

        if w == 0 or l == 0:
            continue

        # Resistance: R = Rsh * L/W (for rectangular approximation)
        aspect = max(l/w, w/l) if min(w, l) > 0 else 0
        r_wire = rsh * aspect if aspect > 0 else 0

        # Capacitance to ground: parallel plate + fringing
        c_area = EPS_OX * EPS0 * area / h
        c_fringe = EPS_OX * EPS0 * perimeter * t / (2 * math.pi * h) if h > 0 else 0
        c_total = c_area + c_fringe

        results.append({
            'metal': metal_name,
            'bbox': f"({bbox.left*layout.dbu:.1f},{bbox.bottom*layout.dbu:.1f})-({bbox.right*layout.dbu:.1f},{bbox.top*layout.dbu:.1f})",
            'w_um': w * 1e6,
            'l_um': l * 1e6,
            'R_ohm': r_wire,
            'C_fF': c_total * 1e15,
        })

    return results


def main():
    layout = pya.Layout()
    layout.read(GDS)
    cell = layout.cell(TOPCELL)

    print(f"PEX: Extracting parasitics for {TOPCELL}")
    print(f"{'Metal':<5} {'Shapes':<7} {'Total R(Ω)':<12} {'Total C(fF)':<12}")
    print("-" * 40)

    all_results = []
    total_r = 0
    total_c = 0

    for metal_name, params in METALS.items():
        ln, dt = params['layer']
        ly_idx = layout.layer(ln, dt)
        results = extract_wire_parasitics(layout, cell, ly_idx, metal_name, params)
        r_sum = sum(r['R_ohm'] for r in results)
        c_sum = sum(r['C_fF'] for r in results)
        total_r += r_sum
        total_c += c_sum
        all_results.extend(results)
        print(f"{metal_name:<5} {len(results):<7} {r_sum:<12.3f} {c_sum:<12.2f}")

    print("-" * 40)
    print(f"{'TOTAL':<5} {len(all_results):<7} {total_r:<12.3f} {total_c:<12.2f}")

    # Write SPICE parasitic netlist
    spice_out = os.path.join(OUT_DIR, "VCO_77G_parasitics.spice")
    with open(spice_out, 'w') as f:
        f.write(f"* Parasitic extraction for {TOPCELL}\n")
        f.write(f"* Total wire resistance: {total_r:.3f} Ohm\n")
        f.write(f"* Total wire capacitance: {total_c:.2f} fF\n")
        f.write(f"* Extraction method: 2D parallel-plate + fringing\n\n")
        f.write(f".SUBCKT {TOPCELL}_parasitic\n")
        for i, r in enumerate(all_results):
            if r['R_ohm'] > 0.001:
                f.write(f"Rp{i} n{i}a n{i}b {r['R_ohm']:.4f} $ {r['metal']} {r['bbox']}\n")
            if r['C_fF'] > 0.001:
                f.write(f"Cp{i} n{i}a 0 {r['C_fF']:.4f}f $ {r['metal']} {r['bbox']}\n")
        f.write(f".ENDS\n")

    print(f"\nParasitic netlist: {spice_out}")

    # Critical path analysis (TM2 signal traces)
    print("\n--- Critical Signal Paths (TM2) ---")
    tm2_results = [r for r in all_results if r['metal'] == 'TM2' and r['R_ohm'] > 0.01]
    tm2_results.sort(key=lambda x: x['R_ohm'], reverse=True)
    for r in tm2_results[:5]:
        print(f"  {r['bbox']}: R={r['R_ohm']:.3f}Ω, C={r['C_fF']:.2f}fF")


if __name__ == "__main__":
    main()
