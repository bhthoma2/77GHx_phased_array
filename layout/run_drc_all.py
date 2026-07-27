import subprocess, sys, os

blocks = [
    ("LNA_77G_XTOR", "ALL_BLOCKS_77G.gds"),
    ("MIXER_77G_XTOR", "ALL_BLOCKS_77G.gds"),
    ("TXPA_77G_XTOR", "ALL_BLOCKS_77G.gds"),
    ("ILFD_77G_XTOR", "ALL_BLOCKS_77G.gds"),
]

base = "/home/bthomas3/Videos/77GHz_phased_array/layout"
drc_json = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/sg13g2_tech_default.json"
drc_script = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc/run_drc.py"

for topcell, gds in blocks:
    run_dir = os.path.join(base, f"drc_{topcell}")
    os.makedirs(run_dir, exist_ok=True)
    gds_path = os.path.join(base, gds)

    sys.argv = [
        "run_drc.py",
        f"--path={gds_path}",
        f"--run_dir={run_dir}",
        f"--topcell={topcell}",
        f"--drc_json={drc_json}",
        "--no_density",
    ]
    try:
        exec(open(drc_script).read())
    except SystemExit:
        pass
    print(f"--- Done: {topcell} ---")
