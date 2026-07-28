import sys
sys.path.insert(0, "/home/bthomas3/Videos/77GHz_phased_array/layout")
import pya
from pdk_devices import create_rppd

layout = pya.Layout()
layout.dbu = 0.001
top = layout.create_cell("TEST_RPPD")

# Test: w=3.0u l=10.0u (like TXPA R_bias)
pins = create_rppd(top, layout, 0, 0, 3.0, 10.0, m=1)
print(f"Pin P: {pins['P']}")
print(f"Pin M: {pins['M']}")

layout.write("/home/bthomas3/Videos/77GHz_phased_array/.tmp/test_rppd.gds")
print("Wrote test_rppd.gds")
