`timescale 1ns/1ps
module vibrometer_top #(
    parameter DW       = 16,
    parameter AW       = 2*DW,
    parameter N_FFT    = 64,
    parameter N_CH     = 6,
    parameter N_CHIRPS = 128,
    parameter N_BEAMS  = 4,
    parameter SRAM_AW  = 10,
    parameter SRAM_DW  = 32
)(
    input  wire                 clk,
    input  wire                 rst_n,
    input  wire                 chirp_start,
    input  wire signed [DW-1:0] adc_data_0,
    input  wire signed [DW-1:0] adc_data_1,
    input  wire signed [DW-1:0] adc_data_2,
    input  wire signed [DW-1:0] adc_data_3,
    input  wire signed [DW-1:0] adc_data_4,
    input  wire signed [DW-1:0] adc_data_5,
    input  wire                 adc_valid,
    input  wire [3:0]           beam_idx,
    input  wire [5:0]           target_range_bin,
    input  wire [7:0]           excite_doppler_bin,
    input  wire                 process_start,
    output wire                 spi_clk_o,
    output wire                 spi_mosi_o,
    output wire                 spi_cs_n_o,
    output wire                 busy
);

// --- Range FFT (per-chirp processing) ---
wire signed [AW-1:0] range_result_re;
wire signed [AW-1:0] range_result_im;
wire [5:0]           range_result_bin;
wire                 range_result_valid;
wire                 range_busy;

radar_mac_accel #(
    .DW(DW), .N_FFT(N_FFT), .N_CH(N_CH)
) u_range_fft (
    .clk(clk),
    .rst_n(rst_n),
    .start(chirp_start),
    .adc_data_0(adc_data_0),
    .adc_data_1(adc_data_1),
    .adc_data_2(adc_data_2),
    .adc_data_3(adc_data_3),
    .adc_data_4(adc_data_4),
    .adc_data_5(adc_data_5),
    .adc_valid(adc_valid),
    .result_re(range_result_re),
    .result_im(range_result_im),
    .result_bin(range_result_bin),
    .result_valid(range_result_valid),
    .busy(range_busy)
);

// --- Slow-Time FFT (across chirps, per beam) ---
wire                 st_busy;
wire signed [AW-1:0] vib_amplitude;
wire [3:0]           vib_beam;
wire                 vib_valid;

wire                 sram_ce;
wire                 sram_we;
wire [SRAM_AW-1:0]  sram_addr;
wire [SRAM_DW-1:0]  sram_wdata;
wire [SRAM_DW-1:0]  sram_rdata;

slowtime_fft #(
    .DW(DW), .N_CHIRPS(N_CHIRPS),
    .N_BEAMS(N_BEAMS), .SRAM_AW(SRAM_AW), .SRAM_DW(SRAM_DW)
) u_slowtime (
    .clk(clk),
    .rst_n(rst_n),
    .chirp_valid(range_result_valid),
    .range_re($signed(range_result_re[DW-1:0])),
    .range_im($signed(range_result_im[DW-1:0])),
    .range_bin(range_result_bin),
    .beam_idx(beam_idx),
    .process_start(process_start),
    .target_bin(target_range_bin),
    .excite_bin(excite_doppler_bin),
    .vib_amplitude(vib_amplitude),
    .vib_beam(vib_beam),
    .vib_valid(vib_valid),
    .busy(st_busy),
    .sram_ce(sram_ce),
    .sram_we(sram_we),
    .sram_addr(sram_addr),
    .sram_wdata(sram_wdata),
    .sram_rdata(sram_rdata)
);

// --- SRAM (slow-time sample buffer) ---
sram_if #(
    .ADDR_W(SRAM_AW), .DATA_W(SRAM_DW)
) u_sram (
    .clk(clk),
    .ce(sram_ce),
    .we(sram_we),
    .addr(sram_addr),
    .wdata(sram_wdata),
    .rdata(sram_rdata)
);

// --- SPI Output ---
spi_serializer #(
    .DW(AW), .FRAME_BITS(38)
) u_spi (
    .clk(clk),
    .rst_n(rst_n),
    .data_re($unsigned(vib_amplitude)),
    .data_im({28'd0, vib_beam}),
    .data_bin(6'd0),
    .data_valid(vib_valid),
    .spi_clk(spi_clk_o),
    .spi_mosi(spi_mosi_o),
    .spi_cs_n(spi_cs_n_o),
    .ready()
);

assign busy = range_busy | st_busy;

endmodule