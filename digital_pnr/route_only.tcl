set PDK_ROOT "/pdk/ihp-sg13g2"

read_lef $PDK_ROOT/libs.ref/sg13g2_stdcell/lef/sg13g2_tech.lef
read_lef $PDK_ROOT/libs.ref/sg13g2_stdcell/lef/sg13g2_stdcell.lef
read_lef $PDK_ROOT/libs.ref/sg13g2_sram/lef/RM_IHPSG13_1P_1024x32_c2_bm_bist.lef
read_liberty $PDK_ROOT/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib
read_liberty $PDK_ROOT/libs.ref/sg13g2_sram/lib/RM_IHPSG13_1P_1024x32_c2_bm_bist_typ_1p20V_25C.lib

read_def build/vibrometer_top.def

# Snap SRAM macro to manufacturing grid
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
        puts "Snapped SRAM to ($new_x, $new_y)"
    }
}

# Global route
global_route -guide_file build/route.guide

# Detailed route
set_routing_layers -signal Metal1-TopMetal2
detailed_route -output_drc build/route_drc.rpt -or_seed 42 -droute_end_iter 3

# Write outputs
write_def build/vibrometer_top_routed.def
report_design_area