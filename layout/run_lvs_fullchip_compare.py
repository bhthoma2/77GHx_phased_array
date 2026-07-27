import sys, os
os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH", "")
os.chdir("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/lvs")

base = "/home/bthomas3/Videos/77GHz_phased_array/layout"
sys.argv = [
    "run_lvs.py",
    f"--layout={base}/PHASED_ARRAY_77G_XTOR.gds",
    f"--netlist={base}/testbenches/fullchip_lvs.spice",
    f"--run_dir={base}/lvs_fullchip",
    "--topcell=PHASED_ARRAY_77G_XTOR",
    "--run_mode=flat",
    "--ignore_top_ports_mismatch",
]
exec(open("run_lvs.py").read())