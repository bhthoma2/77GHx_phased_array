import sys
import traceback
sys.path.insert(0, "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/python")
sys.path.insert(0, "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/python/pycell4klayout-api/source/python")
try:
    import sg13g2_pycell_lib
except Exception as e:
    traceback.print_exc()
