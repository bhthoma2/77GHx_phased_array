import sys, os
os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH", "")
os.chdir("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/lvs")
sys.argv = [
    "run_lvs.py",
    "--layout=/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G_XTOR.gds",
    "--netlist=/home/bthomas3/Videos/77GHz_phased_array/layout/testbenches/vco_lvs.spice",
    "--run_dir=/home/bthomas3/Videos/77GHz_phased_array/layout/lvs_vco",
    "--topcell=VCO_77G_XTOR",
    "--ignore_top_ports_mismatch",
]
exec(open("run_lvs.py").read())
