import sys, os
os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH", "")
os.chdir("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/lvs")

block = os.environ.get("LVS_BLOCK", "LNA_77G_XTOR")
base = "/home/bthomas3/Videos/77GHz_phased_array/layout"

sys.argv = [
    "run_lvs.py",
    f"--layout={base}/ALL_BLOCKS_77G.gds",
    f"--run_dir={base}/lvs_{block}",
    f"--topcell={block}",
    "--run_mode=flat",
]
exec(open("run_lvs.py").read())