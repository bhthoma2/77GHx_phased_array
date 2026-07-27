import sys, os
os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH", "")
os.chdir("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc")
sys.argv = [
    "run_drc.py",
    "--path=/home/bthomas3/Videos/77GHz_phased_array/tapeout/PHASED_ARRAY_77G_XTOR.gds",
    "--run_dir=/home/bthomas3/Videos/77GHz_phased_array/layout/drc_fullchip_xtor",
    "--topcell=PHASED_ARRAY_77G_XTOR",
    "--drc_json=/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/sg13g2_tech_default.json",
    "--no_density",
]
exec(open("run_drc.py").read())
