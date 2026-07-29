# Power grid for IHP SG13G2
add_global_connection -net VDD -pin_pattern {^VDD$} -power
add_global_connection -net VSS -pin_pattern {^VSS$} -ground
add_global_connection -net VSS -pin_pattern {^zero_$} -ground

set_voltage_domain -name Core -power VDD -ground VSS

define_pdn_grid -name core_grid -voltage_domains {Core}
add_pdn_stripe -grid core_grid -layer Metal3 -width 1.0 -pitch 20.0 -offset 5.0 -followpins
add_pdn_stripe -grid core_grid -layer Metal4 -width 2.0 -pitch 40.0 -offset 10.0
add_pdn_connect -grid core_grid -layers {Metal3 Metal4}