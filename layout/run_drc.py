import sys
sys.argv = [
    "run_drc.py",
    "--path=/home/bthomas3/Videos/77GHz_phased_array/layout/VCO_77G.gds",
    "--run_dir=/home/bthomas3/Videos/77GHz_phased_array/layout/drc_out",
    "--drc_json=/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/sg13g2_tech_default.json",
    "--no_feol",
    "--no_density",
]
exec(open("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc/run_drc.py").read())
