import sys, os, subprocess

os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH", "")
base = "/home/bthomas3/Videos/77GHz_phased_array/layout"
lvs_dir = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/lvs"

blocks = [
    ("LNA_77G_XTOR", "ALL_BLOCKS_77G.gds"),
    ("MIXER_77G_XTOR", "ALL_BLOCKS_77G.gds"),
    ("TXPA_77G_XTOR", "ALL_BLOCKS_77G.gds"),
    ("ILFD_77G_XTOR", "ALL_BLOCKS_77G.gds"),
]

results = []
for block, gds in blocks:
    run_dir = f"{base}/lvs_{block}"
    os.makedirs(run_dir, exist_ok=True)
    os.chdir(lvs_dir)
    sys.argv = [
        "run_lvs.py",
        f"--layout={base}/{gds}",
        f"--netlist={base}/testbenches/{block}_lvs.spice",
        f"--run_dir={run_dir}",
        f"--topcell={block}",
        "--run_mode=flat",
        "--ignore_top_ports_mismatch",
    ]
    try:
        exec(open("run_lvs.py").read())
        results.append((block, "DONE"))
    except SystemExit:
        results.append((block, "DONE"))
    except Exception as e:
        results.append((block, str(e)))

print("\n=== Results ===")
for b, r in results:
    print(f"  {b}: {r}")