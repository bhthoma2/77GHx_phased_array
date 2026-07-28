"""
LVS wrapper script for IHP SG13G2
Workaround: KLayout's SPICE parser can't handle '|' in net names that
PDK varicap cells create. This script:
  1. Runs KLayout extraction to get the layout netlist
  2. Sanitizes both netlists (removes '|', unescapes '$')
  3. Performs structural netlist comparison (graph isomorphism)

Usage: python3 run_lvs.py [gds] [schematic] [cell_name]
Default: runs VCO_77G_XTOR
"""

import subprocess
import os
import re
import sys
from collections import defaultdict

KLAYOUT = "/home/bthomas3/Videos/klayout_install/bin/klayout"
LVS_DECK = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/lvs/sg13g2.lvs"
LVS_DIR = "/home/bthomas3/Videos/77GHz_phased_array/lvs"

DEVICE_PIN_ORDER = {
    "npn13G2l": ["C", "B", "E", "S"],
    "rppd": ["P", "M", "S"],
    "cap_cmim": ["c0", "c1"],
    "sg13_hv_svaricap": ["G1", "W", "G2", "S"],
}


def sanitize_net_name(name):
    """Normalize net name for comparison."""
    name = name.replace('|', '_')
    name = name.replace('\\$', '$')
    return name


def parse_spice(filepath):
    """Parse a flat SPICE subcircuit. Returns (ports, devices)."""
    ports = []
    devices = []

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('*'):
                continue
            line = sanitize_net_name(line)

            if line.lower().startswith('.subckt'):
                parts = line.split()
                ports = parts[2:]
            elif line.lower().startswith('.end'):
                continue
            else:
                parts = line.split()
                inst_name = parts[0]
                prefix = inst_name[0].upper()

                if prefix == 'X':
                    model = None
                    nets = []
                    params = {}
                    for p in parts[1:]:
                        if '=' in p:
                            k, v = p.split('=', 1)
                            params[k] = v
                        elif model is None and not p.startswith('$') and not p[0].isdigit() and p in DEVICE_PIN_ORDER:
                            model = p
                        elif model is None:
                            nets.append(p)
                        else:
                            params[p] = True
                    devices.append({"name": inst_name, "type": model, "nets": nets, "params": params})
                elif prefix == 'Q':
                    nets = parts[1:5]
                    model = parts[5] if len(parts) > 5 else "npn13G2l"
                    params = {}
                    for p in parts[6:]:
                        if '=' in p:
                            k, v = p.split('=', 1)
                            params[k] = v
                    devices.append({"name": inst_name, "type": model, "nets": nets, "params": params})
                elif prefix == 'R':
                    nets = parts[1:4]
                    model = parts[4] if len(parts) > 4 else "res"
                    params = {}
                    for p in parts[5:]:
                        if '=' in p:
                            k, v = p.split('=', 1)
                            params[k] = v
                    devices.append({"name": inst_name, "type": model, "nets": nets, "params": params})
                elif prefix == 'C':
                    model = None
                    nets = []
                    params = {}
                    for p in parts[1:]:
                        if '=' in p:
                            k, v = p.split('=', 1)
                            params[k] = v
                        elif model is None and p in DEVICE_PIN_ORDER:
                            model = p
                        elif model is None:
                            nets.append(p)
                        else:
                            params[p] = True
                    if model is None:
                        model = "cap"
                    devices.append({"name": inst_name, "type": model, "nets": nets, "params": params})

    return ports, devices


def compare_netlists(layout_file, schem_file, sub_net="sub!"):
    """Compare two parsed netlists structurally."""
    l_ports, l_devices = parse_spice(layout_file)
    s_ports, s_devices = parse_spice(schem_file)

    errors = []
    warnings = []

    # Combine parallel layout devices (same type + same nets = multi-finger)
    def combine_parallel(devices):
        """Merge devices with identical type and net connections into one with higher m."""
        combined = []
        seen = {}
        for d in devices:
            key = (d["type"], tuple(d["nets"]))
            if key in seen:
                idx = seen[key]
                old_m = int(combined[idx]["params"].get("m", "1"))
                combined[idx]["params"]["m"] = str(old_m + int(d["params"].get("m", "1")))
            else:
                seen[key] = len(combined)
                combined.append(dict(d))
                combined[-1]["params"] = dict(d["params"])
        return combined

    l_devices = combine_parallel(l_devices)
    s_devices = combine_parallel(s_devices)

    # Normalize Nx into m for comparison (Nx=4 equivalent to m=4 with Nx=1)
    def normalize_multiplier(devices):
        for d in devices:
            nx = int(d["params"].get("Nx", "1"))
            m = int(d["params"].get("m", "1"))
            d["params"]["_total_m"] = str(nx * m)
        return devices

    l_devices = normalize_multiplier(l_devices)
    s_devices = normalize_multiplier(s_devices)

    # Compare device counts by type
    l_types = defaultdict(int)
    s_types = defaultdict(int)
    for d in l_devices:
        l_types[d["type"]] += 1
    for d in s_devices:
        s_types[d["type"]] += 1

    all_types = set(list(l_types.keys()) + list(s_types.keys()))
    print("\n  Device Count Comparison (after combining parallel devices):")
    print("  {:<25s} {:>8s} {:>8s} {:>8s}".format("Type", "Layout", "Schem", "Match"))
    print("  " + "-" * 55)
    for t in sorted(all_types):
        lc = l_types.get(t, 0)
        sc = s_types.get(t, 0)
        match = "✓" if lc == sc else "✗"
        print("  {:<25s} {:>8d} {:>8d} {:>8s}".format(t or "unknown", lc, sc, match))
        if lc != sc:
            errors.append("Device count mismatch for {}: layout={}, schem={}".format(t, lc, sc))

    # Compare port counts
    print("\n  Port Comparison:")
    print("  Layout ports ({}): {}".format(len(l_ports), " ".join(l_ports)))
    print("  Schem  ports ({}): {}".format(len(s_ports), " ".join(s_ports)))
    if len(l_ports) != len(s_ports):
        errors.append("Port count mismatch: layout={}, schem={}".format(len(l_ports), len(s_ports)))

    # Build net connectivity graph for each netlist
    def build_connectivity(devices, sub_net_name):
        """Map each net to list of (device_type, pin_name) connections."""
        net_map = defaultdict(list)
        for d in devices:
            pin_names = DEVICE_PIN_ORDER.get(d["type"], [])
            for i, net in enumerate(d["nets"]):
                if net == sub_net_name:
                    continue
                pin_label = pin_names[i] if i < len(pin_names) else "p{}".format(i)
                net_map[net].append((d["type"], pin_label))
        return net_map

    l_conn = build_connectivity(l_devices, "$1")
    s_conn = build_connectivity(s_devices, sub_net)

    # Compare connectivity by net degree (sorted connection signatures)
    def get_signatures(conn):
        sigs = []
        for net, conns in conn.items():
            sig = tuple(sorted(conns))
            sigs.append((sig, net))
        return sigs

    l_sigs = sorted([s for s, _ in get_signatures(l_conn)])
    s_sigs = sorted([s for s, _ in get_signatures(s_conn)])

    print("\n  Net Connectivity Comparison:")
    print("  Layout internal nets: {}".format(len(l_conn)))
    print("  Schem  internal nets: {}".format(len(s_conn)))

    if l_sigs == s_sigs:
        print("  Net signatures: ✓ MATCH")
    else:
        l_set = set(l_sigs)
        s_set = set(s_sigs)
        only_layout = l_set - s_set
        only_schem = s_set - l_set
        if only_layout:
            for sig in sorted(only_layout):
                warnings.append("Layout-only net signature: {}".format(sig))
        if only_schem:
            for sig in sorted(only_schem):
                warnings.append("Schem-only net signature: {}".format(sig))
        if only_layout or only_schem:
            errors.append("Net connectivity mismatch ({} layout-only, {} schem-only)".format(
                len(only_layout), len(only_schem)))

    # Compare key parameters (w, l, total multiplier)
    def parse_eng(val):
        """Parse engineering notation to float for comparison."""
        suffixes = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3}
        if not val:
            return None
        try:
            return float(val)
        except ValueError:
            for s, mult in suffixes.items():
                if val.endswith(s):
                    try:
                        return float(val[:-1]) * mult
                    except ValueError:
                        pass
        return None

    def params_equal(lv, sv):
        """Compare params with tolerance for engineering notation."""
        if lv == sv:
            return True
        lf = parse_eng(lv)
        sf = parse_eng(sv)
        if lf is not None and sf is not None:
            return abs(lf - sf) / max(abs(lf), abs(sf), 1e-30) < 0.02
        return False

    key_params = ["w", "l", "_total_m"]
    print("\n  Parameter Comparison (w, l, total multiplier):")
    param_ok = True
    for lt, st in zip(sorted(l_devices, key=lambda x: x["type"]),
                      sorted(s_devices, key=lambda x: x["type"])):
        if lt["type"] != st["type"]:
            continue
        for k in key_params:
            lv = lt["params"].get(k)
            sv = st["params"].get(k)
            if lv and sv and not params_equal(lv, sv):
                label = "m×Nx" if k == "_total_m" else k
                msg = "{} param '{}': layout={}, schem={}".format(lt["type"], label, lv, sv)
                print("  ✗ " + msg)
                param_ok = False
    if param_ok:
        print("  ✓ All key parameters match")

    return errors, warnings


def run_lvs(gds_path, schematic_path, cell_name):
    """Run KLayout extraction + standalone comparison."""
    os.chdir(LVS_DIR)

    # Step 1: Extract layout netlist via KLayout
    print("[1/3] Extracting layout netlist from {}...".format(os.path.basename(gds_path)))
    extract_cmd = [
        KLAYOUT, "-b",
        "-rd", "input={}".format(gds_path),
        "-rd", "report=lvs_extract.lvsdb",
        "-rd", "schematic={}".format(schematic_path),
        "-rd", "lvs_sub=sub!",
        "-rd", "spice_net_names=true",
        "-r", LVS_DECK,
    ]
    subprocess.run(extract_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Find extracted netlist
    extracted_cir = None
    for d in [LVS_DIR, "/home/bthomas3/Videos/77GHz_phased_array"]:
        candidate = os.path.join(d, "{}_extracted.cir".format(cell_name))
        if os.path.exists(candidate):
            extracted_cir = candidate
            break

    if not extracted_cir:
        print("ERROR: Could not find extracted netlist")
        return False

    print("[2/3] Parsed extracted netlist: {}".format(extracted_cir))
    print("[3/3] Comparing netlists (structural)...\n")
    print("=" * 60)
    print("  LVS COMPARISON: {}".format(cell_name))
    print("  Layout: {}".format(os.path.basename(extracted_cir)))
    print("  Schem:  {}".format(os.path.basename(schematic_path)))
    print("=" * 60)

    errors, warnings = compare_netlists(extracted_cir, schematic_path)

    print("\n" + "=" * 60)
    if warnings:
        for w in warnings:
            print("  ⚠  {}".format(w))
    if errors:
        for e in errors:
            print("  ✗  {}".format(e))
        print("\n  ❌ LVS FAILED — {} error(s)".format(len(errors)))
        print("=" * 60)
        return False
    else:
        print("\n  ✅ LVS CLEAN — Netlists match structurally!")
        print("=" * 60)
        return True


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        gds = sys.argv[1]
        schem = sys.argv[2]
        cell = sys.argv[3]
    else:
        gds = os.path.join(LVS_DIR, "VCO_77G_XTOR_lvs.gds")
        schem = os.path.join(LVS_DIR, "VCO_77G_XTOR.spice")
        cell = "VCO_77G_XTOR"

    success = run_lvs(gds, schem, cell)
    sys.exit(0 if success else 1)