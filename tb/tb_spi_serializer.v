`timescale 1ns/1ps

module tb_spi_serializer;

parameter DW = 32;
parameter FRAME_BITS = 38;

reg clk, rst_n;
reg [DW-1:0] data_re, data_im;
reg [5:0] data_bin;
reg data_valid;
wire spi_clk, spi_mosi, spi_cs_n, ready;

spi_serializer #(.DW(DW), .FRAME_BITS(FRAME_BITS)) dut (
    .clk(clk), .rst_n(rst_n),
    .data_re(data_re), .data_im(data_im),
    .data_bin(data_bin), .data_valid(data_valid),
    .spi_clk(spi_clk), .spi_mosi(spi_mosi),
    .spi_cs_n(spi_cs_n), .ready(ready)
);

always #2.5 clk = ~clk;

reg [FRAME_BITS-1:0] captured_frame;
integer bit_idx;
integer errors;

task send_and_capture;
    input [5:0] bin;
    input [DW-1:0] re;
    input [DW-1:0] im;
    begin
        @(posedge clk);
        data_bin = bin;
        data_re = re;
        data_im = im;
        data_valid = 1;
        @(posedge clk);
        data_valid = 0;
        wait(spi_cs_n == 0);
        bit_idx = FRAME_BITS - 1;
        captured_frame = 0;
        while (!ready) begin
            @(posedge spi_clk);
            captured_frame[bit_idx] = spi_mosi;
            bit_idx = bit_idx - 1;
            if (bit_idx < 0) bit_idx = 0;
        end
    end
endtask

initial begin
    clk = 0; rst_n = 0;
    data_re = 0; data_im = 0; data_bin = 0; data_valid = 0;
    errors = 0;

    #20 rst_n = 1;
    #10;

    // Test 1: Known pattern
    send_and_capture(6'h3F, 32'hABCD_0000, 32'h1234_0000);
    // Expected frame: {6'h3F, 16'hABCD, 16'h1234}
    if (captured_frame[37:32] !== 6'h3F) begin
        $display("FAIL: bin mismatch: got %h exp 3F", captured_frame[37:32]);
        errors = errors + 1;
    end
    if (captured_frame[31:16] !== 16'hABCD) begin
        $display("FAIL: re mismatch: got %h exp ABCD", captured_frame[31:16]);
        errors = errors + 1;
    end
    if (captured_frame[15:0] !== 16'h1234) begin
        $display("FAIL: im mismatch: got %h exp 1234", captured_frame[15:0]);
        errors = errors + 1;
    end

    // Test 2: All zeros
    send_and_capture(6'h00, 32'h0000_0000, 32'h0000_0000);
    if (captured_frame !== 38'd0) begin
        $display("FAIL: all-zero frame mismatch: got %h", captured_frame);
        errors = errors + 1;
    end

    // Test 3: All ones
    send_and_capture(6'h3F, 32'hFFFF_0000, 32'hFFFF_0000);
    if (captured_frame !== {6'h3F, 16'hFFFF, 16'hFFFF}) begin
        $display("FAIL: all-ones frame mismatch: got %h", captured_frame);
        errors = errors + 1;
    end

    // Test 4: Back-to-back (ready handshake)
    send_and_capture(6'h15, 32'hDEAD_0000, 32'hBEEF_0000);
    if (captured_frame[37:32] !== 6'h15) begin
        $display("FAIL: back-to-back bin mismatch");
        errors = errors + 1;
    end

    #100;
    if (errors == 0)
        $display("SPI_SERIALIZER: ALL TESTS PASSED");
    else
        $display("SPI_SERIALIZER: %0d ERRORS", errors);
    $finish;
end

endmodule