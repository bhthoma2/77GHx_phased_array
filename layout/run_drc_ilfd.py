import sys
sys.argv = [
    "run_drc.py",
    "--path=/home/bthomas3/Videos/77GHz_phased_array/layout/ILFD_77G_XTOR.gds",
    "--run_dir=/home/bthomas3/Videos/77GHz_phased_array/layout/drc_ilfd_out",
    "--topcell=ILFD_77GD",
    "--drc_json=/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/sg13g2_tech_default.json",
    "--no_density",
]
exec(open("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc/run_drc.py").read())
