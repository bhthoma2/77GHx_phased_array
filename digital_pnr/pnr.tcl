# OpenROAD P&R script for IHP SG13G2
# Target: vibrometer_mocomp_top @ 200 MHz (5 ns period)

set PDK_ROOT "/pdk/ihp-sg13g2"
set DESIGN "vibrometer_top"
set NETLIST "build/vibrometer_top_synth.v"

# Read LEF
read_lef $PDK_ROOT/libs.ref/sg13g2_stdcell/lef/sg13g2_tech.lef
read_lef $PDK_ROOT/libs.ref/sg13g2_stdcell/lef/sg13g2_stdcell.lef
read_lef $PDK_ROOT/libs.ref/sg13g2_sram/lef/RM_IHPSG13_1P_1024x32_c2_bm_bist.lef

# Read Liberty
read_liberty $PDK_ROOT/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib
read_liberty $PDK_ROOT/libs.ref/sg13g2_sram/lib/RM_IHPSG13_1P_1024x32_c2_bm_bist_typ_1p20V_25C.lib

# Read synthesized netlist
read_verilog $NETLIST
link_design $DESIGN

# Read SDC constraints
read_sdc constraints.sdc

# Floorplan: 1000×1000 µm core (digital block area within 2500×2500 die)
initialize_floorplan -die_area "0 0 2000 2000" \
    -core_area "20 20 1980 1980" \
    -site CoreSite

# Make routing tracks
make_tracks

# Power planning
source power.tcl

# Place IO pins
place_pins -hor_layers Metal3 -ver_layers Metal2

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

# Mark ground-type nets as special before detailed routing
set block [ord::get_db_block]
foreach net [$block getNets] {
    if {[$net getSigType] == "GROUND" || [$net getSigType] == "POWER"} {
        $net setSpecial
    }
}

# Snap SRAM macro to manufacturing grid (5nm)
set block [ord::get_db_block]
foreach inst [$block getInsts] {
    if {[[$inst getMaster] getName] == "RM_IHPSG13_1P_1024x32_c2_bm_bist"} {
        set bbox [$inst getBBox]
        set x [$bbox xMin]
        set y [$bbox yMin]
        set grid 5
        set new_x [expr {(($x + $grid/2) / $grid) * $grid}]
        set new_y [expr {(($y + $grid/2) / $grid) * $grid}]
        $inst setLocation $new_x $new_y
        puts "Snapped SRAM macro to ($new_x, $new_y)"
    }
}

# Detailed routing
set_routing_layers -signal Metal1-TopMetal2
detailed_route -output_drc build/route_drc.rpt -or_seed 42 -droute_end_iter 10

# Write outputs
write_def build/${DESIGN}.def
write_verilog build/${DESIGN}_pnr.v

# Report timing
report_worst_slack -max
report_worst_slack -min
report_design_area