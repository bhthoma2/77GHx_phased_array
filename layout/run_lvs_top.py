import sys, os
os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH", "")
os.chdir("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/lvs")
sys.argv = [
    "run_lvs.py",
    "--layout=/home/bthomas3/Videos/77GHz_phased_array/layout/PHASED_ARRAY_77G_TOP.gds",
    "--netlist=/home/bthomas3/Videos/77GHz_phased_array/layout/PHASED_ARRAY_77G_TOP.spice",
    "--run_dir=/home/bthomas3/Videos/77GHz_phased_array/layout/lvs_top",
    "--topcell=PHASED_ARRAY_77G_TOP",
    "--ignore_top_ports_mismatch",
]
exec(open("run_lvs.py").read())