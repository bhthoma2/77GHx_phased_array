import sys, os
os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH", "")
os.chdir("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/lvs")
sys.argv = [
    "run_lvs.py",
    "--layout=/home/bthomas3/Videos/77GHz_phased_array/layout/MIXER_77G_XTOR.gds",
    "--run_dir=/home/bthomas3/Videos/77GHz_phased_array/layout/lvs_mixer",
    "--topcell=MIXER_77GD",
    "--net_only",
]
exec(open("run_lvs.py").read())