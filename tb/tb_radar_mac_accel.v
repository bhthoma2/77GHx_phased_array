`timescale 1ns/1ps

module tb_radar_mac_accel;

parameter DW = 16;
parameter N_FFT = 64;
parameter N_CH = 6;
parameter N_MAC = 4;
parameter AW = 32;

reg clk, rst_n, start, adc_valid;
reg signed [DW-1:0] adc_data_0, adc_data_1, adc_data_2;
reg signed [DW-1:0] adc_data_3, adc_data_4, adc_data_5;
wire signed [AW-1:0] result_re, result_im;
wire [5:0] result_bin;
wire result_valid, busy;

radar_mac_accel #(
    .DW(DW), .N_FFT(N_FFT), .N_CH(N_CH), .N_MAC(N_MAC)
) dut (
    .clk(clk), .rst_n(rst_n), .start(start),
    .adc_data_0(adc_data_0), .adc_data_1(adc_data_1),
    .adc_data_2(adc_data_2), .adc_data_3(adc_data_3),
    .adc_data_4(adc_data_4), .adc_data_5(adc_data_5),
    .adc_valid(adc_valid),
    .result_re(result_re), .result_im(result_im),
    .result_bin(result_bin), .result_valid(result_valid),
    .busy(busy)
);

always #2.5 clk = ~clk;

integer errors;
integer sample_i;
real pi;
real freq_norm;
reg signed [DW-1:0] tone;

initial begin
    pi = 3.14159265358979;
    clk = 0; rst_n = 0; start = 0; adc_valid = 0;
    adc_data_0 = 0; adc_data_1 = 0; adc_data_2 = 0;
    adc_data_3 = 0; adc_data_4 = 0; adc_data_5 = 0;
    errors = 0;

    #20 rst_n = 1;
    #10;

    // Test 1: Single tone at bin 8 on all channels
    // For bin k: x[n] = cos(2*pi*k*n/N), expect peak at bin 8
    freq_norm = 8.0 / 64.0;

    @(posedge clk);
    start = 1;
    @(posedge clk);
    start = 0;

    for (sample_i = 0; sample_i < N_FFT; sample_i = sample_i + 1) begin
        @(posedge clk);
        tone = $rtoi($cos(2.0 * pi * freq_norm * sample_i) * 2000.0);
        adc_data_0 = tone;
        adc_data_1 = tone;
        adc_data_2 = tone;
        adc_data_3 = tone;
        adc_data_4 = tone;
        adc_data_5 = tone;
        adc_valid = 1;
        @(posedge clk);
        adc_valid = 0;
        #10;
    end

    // Wait for result
    wait(result_valid == 1);
    @(posedge clk);

    $display("result_bin = %0d", result_bin);
    $display("result_re = %0d", result_re);
    $display("result_im = %0d", result_im);

    // Peak should be at bin 8
    if (result_bin !== 6'd8) begin
        $display("FAIL: expected peak at bin 8, got %0d", result_bin);
        errors = errors + 1;
    end

    // Real part should be large positive (coherent sum of 6 channels)
    if (result_re <= 0) begin
        $display("FAIL: expected positive result_re, got %0d", result_re);
        errors = errors + 1;
    end

    // Test 2: DC input (all constant) -> peak at bin 0
    #100;
    @(posedge clk);
    start = 1;
    @(posedge clk);
    start = 0;

    for (sample_i = 0; sample_i < N_FFT; sample_i = sample_i + 1) begin
        @(posedge clk);
        adc_data_0 = 16'd1000;
        adc_data_1 = 16'd1000;
        adc_data_2 = 16'd1000;
        adc_data_3 = 16'd1000;
        adc_data_4 = 16'd1000;
        adc_data_5 = 16'd1000;
        adc_valid = 1;
        @(posedge clk);
        adc_valid = 0;
        #10;
    end

    wait(result_valid == 1);
    @(posedge clk);

    $display("DC test: result_bin = %0d, result_re = %0d", result_bin, result_re);

    if (result_bin !== 6'd0) begin
        $display("FAIL: DC expected bin 0, got %0d", result_bin);
        errors = errors + 1;
    end

    #100;
    if (errors == 0)
        $display("RADAR_MAC_ACCEL: ALL TESTS PASSED");
    else
        $display("RADAR_MAC_ACCEL: %0d ERRORS", errors);
    $finish;
end

initial begin
    #10000000;
    $display("TIMEOUT: simulation exceeded 10ms");
    $finish;
end

endmodule