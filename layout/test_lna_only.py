import pya
import os, sys
os.environ["PATH"] = "/home/bthomas3/Videos/klayout_install/bin:" + os.environ.get("PATH","")
sys.path.insert(0, "/home/bthomas3/Videos/77GHz_phased_array/layout")
import generate_lna_transistor as gen_lna
import generate_ilfd_transistor as gen_ilfd
OUT_DIR = "/home/bthomas3/Videos/77GHz_phased_array/layout/"
PDK_GDS = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_pr/gds/sg13g2_pr.gds"

def um(x):
    return int(round(x / 0.001))

layout = pya.Layout()
layout.dbu = 0.001
layout.read(PDK_GDS)
gen_lna.main(layout)
gen_ilfd.main(layout)
top = layout.create_cell("LNA_ONLY_TEST")
lna_idx = layout.cell_by_name("RXAMP_77GD")
ilfd_idx = layout.cell_by_name("ILFD_77GD")
top.insert(pya.CellInstArray(lna_idx, pya.Trans(um(200), um(1100))))
top.insert(pya.CellInstArray(ilfd_idx, pya.Trans(um(200), um(300))))
layout.write(OUT_DIR + "test_lna_only.gds")
print("Done: LNA + ILFD (no TM1 in ILFD)")