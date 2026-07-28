import sys, os
os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH", "")
os.chdir("/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/lvs")
sys.argv = [
    "run_lvs.py",
    "--layout=/home/bthomas3/Videos/77GHz_phased_array/layout/.tmp/test_no_routes.gds",
    "--run_dir=/home/bthomas3/Videos/77GHz_phased_array/layout/.tmp/lvs_test",
    "--topcell=TEST_TOP",
    "--net_only",
]
exec(open("run_lvs.py").read())
