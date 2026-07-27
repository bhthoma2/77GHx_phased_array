# OpenROAD P&R script for IHP SG13G2
# Target: vibrometer_mocomp_top @ 200 MHz (5 ns period)

set PDK_ROOT "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2"
set DESIGN "vibrometer_mocomp_top"
set NETLIST "build/${DESIGN}.v"

# Read LEF
read_lef $PDK_ROOT/libs.ref/sg13g2_stdcell/lef/sg13g2_tech.lef
read_lef $PDK_ROOT/libs.ref/sg13g2_stdcell/lef/sg13g2_stdcell.lef

# Read Liberty
read_liberty $PDK_ROOT/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib

# Read synthesized netlist
read_verilog $NETLIST
link_design $DESIGN

# Read SDC constraints
read_sdc constraints.sdc

# Floorplan: 1000×1000 µm core (digital block area within 2500×2500 die)
initialize_floorplan -utilization 0.50 \
    -aspect_ratio 1.0 \
    -core_space 10 \
    -site sg13g2_std

# Power planning
source power.tcl

# Global placement
global_placement -density 0.60

# Clock tree synthesis
clock_tree_synthesis -root_buf sg13g2_buf_8 \
    -buf_list {sg13g2_buf_2 sg13g2_buf_4 sg13g2_buf_8}

# Repair hold violations
repair_timing -hold

# Detailed placement
detailed_placement

# Global routing
global_route -guide_file build/route.guide

# Detailed routing
detailed_route -output_drc build/route_drc.rpt

# Write outputs
write_def build/${DESIGN}.def
write_verilog build/${DESIGN}_pnr.v

# Report timing
report_timing -path_delay max -max_paths 5
report_design_area