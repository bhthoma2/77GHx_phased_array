import sys
sys.path.insert(0, '/home/bthomas3/Videos/77GHz_phased_array/layout')
import generate_vco_transistor as gvt

# Monkey-patch: remove varactor routing by replacing the section
import pya

orig_main = gvt.main

def patched_main():
    # Just run original - we want to check extracted netlist
    orig_main()

patched_main()
