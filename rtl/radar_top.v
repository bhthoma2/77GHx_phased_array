module radar_top #(
    parameter DW    = 16,
    parameter N_FFT = 64,
    parameter N_CH  = 6,
    parameter AW    = 2*DW
)(
    input  wire                 clk,
    input  wire                 rst_n,
    input  wire                 start,
    input  wire signed [DW-1:0] adc_data_0,
    input  wire signed [DW-1:0] adc_data_1,
    input  wire signed [DW-1:0] adc_data_2,
    input  wire signed [DW-1:0] adc_data_3,
    input  wire signed [DW-1:0] adc_data_4,
    input  wire signed [DW-1:0] adc_data_5,
    input  wire                 adc_valid,
    output wire                 spi_clk,
    output wire                 spi_mosi,
    output wire                 spi_cs_n,
    output wire                 busy
);

wire signed [AW-1:0] result_re;
wire signed [AW-1:0] result_im;
wire [5:0]           result_bin;
wire                 result_valid;

radar_mac_accel #(
    .DW(DW), .N_FFT(N_FFT), .N_CH(N_CH)
) u_accel (
    .clk(clk),
    .rst_n(rst_n),
    .start(start),
    .adc_data_0(adc_data_0),
    .adc_data_1(adc_data_1),
    .adc_data_2(adc_data_2),
    .adc_data_3(adc_data_3),
    .adc_data_4(adc_data_4),
    .adc_data_5(adc_data_5),
    .adc_valid(adc_valid),
    .result_re(result_re),
    .result_im(result_im),
    .result_bin(result_bin),
    .result_valid(result_valid),
    .busy(busy)
);

spi_serializer #(
    .DW(AW), .FRAME_BITS(38)
) u_spi (
    .clk(clk),
    .rst_n(rst_n),
    .data_re($unsigned(result_re)),
    .data_im($unsigned(result_im)),
    .data_bin(result_bin),
    .data_valid(result_valid),
    .spi_clk(spi_clk),
    .spi_mosi(spi_mosi),
    .spi_cs_n(spi_cs_n),
    .ready()
);

endmodule