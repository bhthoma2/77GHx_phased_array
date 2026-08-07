set PDK_ROOT "/pdk/ihp-sg13g2"

read_lef $PDK_ROOT/libs.ref/sg13g2_stdcell/lef/sg13g2_tech.lef
read_lef $PDK_ROOT/libs.ref/sg13g2_stdcell/lef/sg13g2_stdcell.lef
read_liberty $PDK_ROOT/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib

read_verilog build/radar_mac_accel_synth.v
link_design radar_mac_accel

read_sdc constraints.sdc

initialize_floorplan -die_area "0 0 2200 2200" \
    -core_area "10 10 2190 2190" \
    -site CoreSite

make_tracks

add_global_connection -net VDD -pin_pattern {^VDD$} -power
add_global_connection -net VSS -pin_pattern {^VSS$} -ground
set_voltage_domain -name Core -power VDD -ground VSS
define_pdn_grid -name core_grid -voltage_domains {Core}
add_pdn_stripe -grid core_grid -layer Metal5 -width 2.0 -pitch 50.0 -offset 10.0 -followpins
add_pdn_stripe -grid core_grid -layer TopMetal1 -width 4.0 -pitch 100.0 -offset 20.0
add_pdn_connect -grid core_grid -layers {Metal5 TopMetal1}

place_pins -hor_layers Metal3 -ver_layers Metal2
global_placement -density 0.40
clock_tree_synthesis -root_buf sg13g2_buf_8 \
    -buf_list {sg13g2_buf_2 sg13g2_buf_4 sg13g2_buf_8}
repair_timing -hold
detailed_placement

# Repair high-fanout nets with buffer trees
set_max_fanout 100 [current_design]
repair_design

global_route -guide_file build/route_mac.guide -allow_congestion

set block [ord::get_db_block]
foreach net [$block getNets] {
    if {[$net getSigType] == "GROUND" || [$net getSigType] == "POWER"} {
        $net setSpecial
    }
}

set_routing_layers -signal Metal1-TopMetal2
detailed_route -output_drc build/route_mac_drc.rpt -or_seed 42 -droute_end_iter 3

write_def build/radar_mac_accel_routed.def
report_worst_slack -max
report_worst_slack -min
report_design_area