# Yosys synthesis script for IHP SG13G2
# Target: vibrometer_mocomp_top

set RTL_DIR "../rtl"
set LIBERTY "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib"
set DESIGN "vibrometer_mocomp_top"

read_verilog $RTL_DIR/vibrometer_mocomp_top.v
read_verilog $RTL_DIR/radar_mac_accel.v
read_verilog $RTL_DIR/slowtime_fft.v
read_verilog $RTL_DIR/sram_if.v
read_verilog $RTL_DIR/spi_serializer.v
read_verilog $RTL_DIR/deconv_kernel_estimator_top_level.v
read_verilog $RTL_DIR/iir_notch_filter.v
read_verilog $RTL_DIR/cordic_rect_to_polar.v
read_verilog $RTL_DIR/cordic_polar_to_rect.v
read_verilog $RTL_DIR/fixed_pt_div.v
read_verilog $RTL_DIR/deserializer.v
read_verilog $RTL_DIR/serializer.v

hierarchy -check -top $DESIGN
proc; opt; fsm; opt; memory; opt
techmap; opt
dfflibmap -liberty $LIBERTY
abc -liberty $LIBERTY
clean
opt_clean -purge

stat -liberty $LIBERTY

write_verilog build/${DESIGN}.v