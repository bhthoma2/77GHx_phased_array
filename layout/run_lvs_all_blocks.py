import sys, os

os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH", "")
os.chdir("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/lvs")

blocks = [
    ("LNA_77G_XTOR", "LNA_77G_XTOR"),
    ("MIXER_77G_XTOR", "MIXER_77G_XTOR"),
    ("TXPA_77G_XTOR", "TXPA_77G_XTOR"),
    ("ILFD_77G_XTOR", "ILFD_77G_XTOR"),
]

layout_dir = "/home/bthomas3/Videos/77GHz_phased_array/layout"

for gds_name, topcell in blocks:
    run_dir = os.path.join(layout_dir, f"lvs_{topcell.lower()}")
    os.makedirs(run_dir, exist_ok=True)
    gds_path = os.path.join(layout_dir, f"{gds_name}.gds")
    print(f"\n{'='*60}")
    print(f"Running LVS on {topcell}")
    print(f"{'='*60}")
    sys.argv = [
        "run_lvs.py",
        f"--layout={gds_path}",
        f"--run_dir={run_dir}",
        f"--topcell={topcell}",
        "--net_only",
    ]
    try:
        exec(open("run_lvs.py").read())
    except SystemExit:
        pass
