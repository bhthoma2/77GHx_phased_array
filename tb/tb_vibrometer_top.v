`timescale 1ns/1ps

module tb_vibrometer_top;

parameter DW = 16;
parameter AW = 32;
parameter N_FFT = 64;
parameter N_CH = 6;
parameter N_CHIRPS = 128;
parameter N_BEAMS = 4;
parameter SRAM_AW = 10;
parameter SRAM_DW = 32;

reg clk, rst_n;
reg chirp_start;
reg signed [DW-1:0] adc_data_0, adc_data_1, adc_data_2;
reg signed [DW-1:0] adc_data_3, adc_data_4, adc_data_5;
reg adc_valid;
reg [3:0] beam_idx;
reg [5:0] target_range_bin;
reg [7:0] excite_doppler_bin;
reg process_start;
wire spi_clk_o, spi_mosi_o, spi_cs_n_o, busy;

vibrometer_top #(
    .DW(DW), .N_FFT(N_FFT), .N_CH(N_CH),
    .N_CHIRPS(N_CHIRPS), .N_BEAMS(N_BEAMS),
    .SRAM_AW(SRAM_AW), .SRAM_DW(SRAM_DW)
) dut (
    .clk(clk), .rst_n(rst_n),
    .chirp_start(chirp_start),
    .adc_data_0(adc_data_0), .adc_data_1(adc_data_1),
    .adc_data_2(adc_data_2), .adc_data_3(adc_data_3),
    .adc_data_4(adc_data_4), .adc_data_5(adc_data_5),
    .adc_valid(adc_valid),
    .beam_idx(beam_idx),
    .target_range_bin(target_range_bin),
    .excite_doppler_bin(excite_doppler_bin),
    .process_start(process_start),
    .spi_clk_o(spi_clk_o), .spi_mosi_o(spi_mosi_o),
    .spi_cs_n_o(spi_cs_n_o), .busy(busy)
);

always #2.5 clk = ~clk;

integer errors;
integer chirp_i, sample_i, beam_i;
real pi;
real range_freq, doppler_freq;
reg signed [DW-1:0] tone;

// Capture SPI output
reg [37:0] spi_captured;
integer spi_bit;

initial begin
    pi = 3.14159265358979;
    clk = 0; rst_n = 0;
    chirp_start = 0; adc_valid = 0;
    adc_data_0 = 0; adc_data_1 = 0; adc_data_2 = 0;
    adc_data_3 = 0; adc_data_4 = 0; adc_data_5 = 0;
    beam_idx = 0;
    target_range_bin = 6'd8;
    excite_doppler_bin = 8'd5;
    process_start = 0;
    errors = 0;

    #20 rst_n = 1;
    #10;

    // Feed N_CHIRPS chirps, each with N_FFT ADC samples
    // Range tone at bin 8: cos(2*pi*8*n/64)
    // Doppler modulation at bin 5: amplitude varies as cos(2*pi*5*chirp/128)
    range_freq = 8.0 / 64.0;
    doppler_freq = 5.0 / 128.0;

    for (chirp_i = 0; chirp_i < N_CHIRPS; chirp_i = chirp_i + 1) begin
        for (beam_i = 0; beam_i < N_BEAMS; beam_i = beam_i + 1) begin
            // Start range FFT for this chirp/beam
            @(posedge clk);
            chirp_start = 1;
            beam_idx = beam_i[3:0];
            @(posedge clk);
            chirp_start = 0;

            // Feed 64 ADC samples
            for (sample_i = 0; sample_i < N_FFT; sample_i = sample_i + 1) begin
                @(posedge clk);
                if (beam_i == 0) begin
                    // Beam 0 has signal: range tone modulated by Doppler
                    tone = $rtoi($cos(2.0*pi*range_freq*sample_i) *
                                 $cos(2.0*pi*doppler_freq*chirp_i) * 1500.0);
                end else begin
                    tone = 0;
                end
                adc_data_0 = tone;
                adc_data_1 = tone;
                adc_data_2 = tone;
                adc_data_3 = tone;
                adc_data_4 = tone;
                adc_data_5 = tone;
                adc_valid = 1;
                @(posedge clk);
                adc_valid = 0;
            end

            // Wait for range FFT to finish
            wait(busy == 0);
            #20;
        end
    end

    // Trigger slow-time FFT processing
    @(posedge clk);
    process_start = 1;
    @(posedge clk);
    process_start = 0;

    // Wait for SPI output (cs_n goes low then high)
    wait(spi_cs_n_o == 0);
    spi_bit = 37;
    spi_captured = 0;
    while (spi_cs_n_o == 0) begin
        @(posedge spi_clk_o);
        if (spi_bit >= 0) begin
            spi_captured[spi_bit] = spi_mosi_o;
            spi_bit = spi_bit - 1;
        end
    end

    $display("SPI frame captured: %h", spi_captured);
    $display("  bin  = %0d", spi_captured[37:32]);
    $display("  re   = %0h", spi_captured[31:16]);
    $display("  im   = %0h", spi_captured[15:0]);

    // Verify SPI output is non-zero (signal was present)
    if (spi_captured[31:16] == 16'd0 && spi_captured[15:0] == 16'd0) begin
        $display("FAIL: SPI output is all zeros - no signal detected");
        errors = errors + 1;
    end

    #200;
    if (errors == 0)
        $display("VIBROMETER_TOP: ALL TESTS PASSED (end-to-end)");
    else
        $display("VIBROMETER_TOP: %0d ERRORS", errors);
    $finish;
end

initial begin
    #50000000;
    $display("TIMEOUT: simulation exceeded 50ms");
    $finish;
end

endmodule