`timescale 1ns/1ps

module tb_slowtime_fft;

parameter DW = 16;
parameter AW = 32;
parameter N_CHIRPS = 128;
parameter N_BINS = 64;
parameter N_BEAMS = 4;
parameter SRAM_AW = 10;
parameter SRAM_DW = 32;

reg clk, rst_n;
reg chirp_valid;
reg signed [DW-1:0] range_re, range_im;
reg [5:0] range_bin;
reg [3:0] beam_idx;
reg process_start;
reg [5:0] target_bin;
reg [7:0] excite_bin;
wire signed [AW-1:0] vib_amplitude;
wire [3:0] vib_beam;
wire vib_valid, busy;

wire sram_ce, sram_we;
wire [SRAM_AW-1:0] sram_addr;
wire [SRAM_DW-1:0] sram_wdata;
reg [SRAM_DW-1:0] sram_rdata;

slowtime_fft #(
    .DW(DW), .N_CHIRPS(N_CHIRPS), .N_BINS(N_BINS),
    .N_BEAMS(N_BEAMS), .SRAM_AW(SRAM_AW), .SRAM_DW(SRAM_DW)
) dut (
    .clk(clk), .rst_n(rst_n),
    .chirp_valid(chirp_valid),
    .range_re(range_re), .range_im(range_im),
    .range_bin(range_bin), .beam_idx(beam_idx),
    .process_start(process_start),
    .target_bin(target_bin), .excite_bin(excite_bin),
    .vib_amplitude(vib_amplitude), .vib_beam(vib_beam),
    .vib_valid(vib_valid), .busy(busy),
    .sram_ce(sram_ce), .sram_we(sram_we),
    .sram_addr(sram_addr), .sram_wdata(sram_wdata),
    .sram_rdata(sram_rdata)
);

// Simple SRAM model
reg [SRAM_DW-1:0] mem [0:(1<<SRAM_AW)-1];

always @(posedge clk) begin
    if (sram_ce && sram_we)
        mem[sram_addr] <= sram_wdata;
    if (sram_ce && !sram_we)
        sram_rdata <= mem[sram_addr];
end

always #2.5 clk = ~clk;

integer errors;
integer chirp_i, beam_i;
real pi;
real freq_norm;
reg signed [DW-1:0] cos_val, sin_val;

initial begin
    pi = 3.14159265358979;
    clk = 0; rst_n = 0;
    chirp_valid = 0; range_re = 0; range_im = 0;
    range_bin = 0; beam_idx = 0;
    process_start = 0; target_bin = 6'd10; excite_bin = 8'd5;
    errors = 0;

    #20 rst_n = 1;
    #10;

    // Feed 128 chirps with a sinusoid at Doppler bin 5
    // For bin k of N-point FFT, input = exp(j*2*pi*k*n/N)
    // We put signal on beam 0, target_bin = 10
    freq_norm = 5.0 / 128.0;

    for (chirp_i = 0; chirp_i < N_CHIRPS; chirp_i = chirp_i + 1) begin
        for (beam_i = 0; beam_i < N_BEAMS; beam_i = beam_i + 1) begin
            @(posedge clk);
            if (beam_i == 0) begin
                // Signal on beam 0: cos + j*sin at Doppler bin 5
                cos_val = $rtoi($cos(2.0 * pi * freq_norm * chirp_i) * 1000.0);
                sin_val = $rtoi($sin(2.0 * pi * freq_norm * chirp_i) * 1000.0);
                range_re = cos_val;
                range_im = sin_val;
            end else begin
                // Other beams: noise-free zero
                range_re = 0;
                range_im = 0;
            end
            range_bin = target_bin;
            beam_idx = beam_i[3:0];
            chirp_valid = 1;
            @(posedge clk);
            chirp_valid = 0;
            #10;
        end
    end

    // Trigger slow-time FFT processing
    @(posedge clk);
    process_start = 1;
    @(posedge clk);
    process_start = 0;

    // Wait for output
    wait(vib_valid == 1);
    @(posedge clk);

    $display("vib_amplitude = %0d", vib_amplitude);
    $display("vib_beam = %0d", vib_beam);

    // Verify: best beam should be 0 (strongest signal)
    if (vib_beam !== 4'd0) begin
        $display("FAIL: expected beam 0, got %0d", vib_beam);
        errors = errors + 1;
    end

    // Amplitude should be significantly nonzero
    if (vib_amplitude == 0) begin
        $display("FAIL: amplitude is zero");
        errors = errors + 1;
    end

    #100;
    if (errors == 0)
        $display("SLOWTIME_FFT: ALL TESTS PASSED");
    else
        $display("SLOWTIME_FFT: %0d ERRORS", errors);
    $finish;
end

initial begin
    #5000000;
    $display("TIMEOUT: simulation exceeded 5ms");
    $finish;
end

endmodule