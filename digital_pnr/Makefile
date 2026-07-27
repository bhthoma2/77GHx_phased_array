# Digital P&R Flow for Vibrometer DSP — IHP SG13G2
# Uses Yosys (synthesis) + OpenROAD (P&R) + KLayout (GDS merge/DRC/LVS)
#
# Prerequisites:
#   - IHP-Open-PDK installed at $(PDK_ROOT)
#   - Yosys, OpenROAD, KLayout on PATH
#
# Usage:
#   make synth    — Run Yosys synthesis
#   make pnr      — Run OpenROAD place & route
#   make gds      — Export GDS
#   make drc      — Run DRC
#   make all      — Full flow

PDK_ROOT     = /home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2
LIBERTY      = $(PDK_ROOT)/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib
LEF_TECH     = $(PDK_ROOT)/libs.ref/sg13g2_stdcell/lef/sg13g2_tech.lef
LEF_CELLS    = $(PDK_ROOT)/libs.ref/sg13g2_stdcell/lef/sg13g2_stdcell.lef
GDS_CELLS    = $(PDK_ROOT)/libs.ref/sg13g2_stdcell/gds/sg13g2_stdcell.gds

RTL_DIR      = ../rtl
DESIGN       = vibrometer_mocomp_top
CLK_PERIOD   = 5.0
CORE_UTIL    = 0.60

BUILD_DIR    = build
NETLIST      = $(BUILD_DIR)/$(DESIGN).v
DEF_FILE     = $(BUILD_DIR)/$(DESIGN).def
GDS_FILE     = $(BUILD_DIR)/$(DESIGN).gds

RTL_FILES    = $(RTL_DIR)/vibrometer_mocomp_top.v \
               $(RTL_DIR)/radar_mac_accel.v \
               $(RTL_DIR)/slowtime_fft.v \
               $(RTL_DIR)/sram_if.v \
               $(RTL_DIR)/spi_serializer.v \
               $(RTL_DIR)/deconv_kernel_estimator_top_level.v \
               $(RTL_DIR)/iir_notch_filter.v \
               $(RTL_DIR)/cordic_rect_to_polar.v \
               $(RTL_DIR)/cordic_polar_to_rect.v \
               $(RTL_DIR)/fixed_pt_div.v \
               $(RTL_DIR)/deserializer.v \
               $(RTL_DIR)/serializer.v

.PHONY: all synth pnr gds drc clean

all: gds

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

synth: $(NETLIST)

$(NETLIST): $(RTL_FILES) synth.tcl | $(BUILD_DIR)
	yosys -c synth.tcl

pnr: $(DEF_FILE)

$(DEF_FILE): $(NETLIST) pnr.tcl constraints.sdc | $(BUILD_DIR)
	openroad -exit pnr.tcl

gds: $(GDS_FILE)

$(GDS_FILE): $(DEF_FILE)
	klayout -b -r export_gds.py

drc: $(GDS_FILE)
	klayout -b -r run_drc.py

clean:
	rm -rf $(BUILD_DIR)