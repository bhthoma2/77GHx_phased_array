import sys, os
os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH", "")
os.chdir("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc")
sys.argv = [
    "klayout", "-b", "-r", "ihp-sg13g2.drc",
    "-rd", "input=/home/bthomas3/Videos/77GHz_phased_array/layout/PHASED_ARRAY_77G_TOP.gds",
    "-rd", "topcell=PHASED_ARRAY_77G_TOP",
    "-rd", "report=/home/bthomas3/Videos/77GHz_phased_array/layout/drc_top.lyrdb",
]