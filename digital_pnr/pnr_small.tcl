set PDK_ROOT "/pdk/ihp-sg13g2"

read_lef $PDK_ROOT/libs.ref/sg13g2_stdcell/lef/sg13g2_tech.lef
read_lef $PDK_ROOT/libs.ref/sg13g2_stdcell/lef/sg13g2_stdcell.lef
read_lef $PDK_ROOT/libs.ref/sg13g2_sram/lef/RM_IHPSG13_1P_1024x32_c2_bm_bist.lef
read_liberty $PDK_ROOT/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib
read_liberty $PDK_ROOT/libs.ref/sg13g2_sram/lib/RM_IHPSG13_1P_1024x32_c2_bm_bist_typ_1p20V_25C.lib

read_verilog build/slowtime_fft_synth.v
link_design slowtime_fft

read_sdc constraints.sdc

initialize_floorplan -die_area "0 0 500 500" \
    -core_area "10 10 490 490" \
    -site CoreSite

make_tracks

# Power
add_global_connection -net VDD -pin_pattern {^VDD$} -power
add_global_connection -net VSS -pin_pattern {^VSS$} -ground
set_voltage_domain -name Core -power VDD -ground VSS
define_pdn_grid -name core_grid -voltage_domains {Core}
add_pdn_stripe -grid core_grid -layer Metal3 -width 1.0 -pitch 20.0 -offset 5.0 -followpins
add_pdn_stripe -grid core_grid -layer Metal4 -width 2.0 -pitch 40.0 -offset 10.0
add_pdn_connect -grid core_grid -layers {Metal3 Metal4}

# Place IO pins
place_pins -hor_layers Metal3 -ver_layers Metal2

# Placement
global_placement -density 0.60
clock_tree_synthesis -root_buf sg13g2_buf_8 \
    -buf_list {sg13g2_buf_2 sg13g2_buf_4 sg13g2_buf_8}
repair_timing -hold
detailed_placement

# Snap SRAM macro to grid
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
    }
}

# Mark power/ground nets as special
foreach net [$block getNets] {
    if {[$net getSigType] == "GROUND" || [$net getSigType] == "POWER"} {
        $net setSpecial
    }
}

# Routing
global_route -guide_file build/route_small.guide
set_routing_layers -signal Metal1-TopMetal2
detailed_route -output_drc build/route_small_drc.rpt -or_seed 42 -droute_end_iter 5

# Output
write_def build/slowtime_fft_routed.def
report_worst_slack -max
report_worst_slack -min
report_design_area