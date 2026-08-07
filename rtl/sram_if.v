`timescale 1ns/1ps
module sram_if #(
    parameter ADDR_W = 10,
    parameter DATA_W = 32
)(
    input  wire              clk,
    input  wire              ce,
    input  wire              we,
    input  wire [ADDR_W-1:0] addr,
    input  wire [DATA_W-1:0] wdata,
    output wire [DATA_W-1:0] rdata
);

`ifdef SYNTHESIS

RM_IHPSG13_1P_1024x32_c2_bm_bist u_sram (
    .A_CLK(clk),
    .A_MEN(ce),
    .A_WEN(we),
    .A_REN(ce & ~we),
    .A_ADDR(addr),
    .A_DIN(wdata),
    .A_DLY(1'b0),
    .A_DOUT(rdata),
    .A_BM({DATA_W{1'b1}}),
    .A_BIST_CLK(1'b0),
    .A_BIST_EN(1'b0),
    .A_BIST_MEN(1'b0),
    .A_BIST_WEN(1'b0),
    .A_BIST_REN(1'b0),
    .A_BIST_ADDR(10'd0),
    .A_BIST_DIN(32'd0),
    .A_BIST_BM(32'd0)
);

`else

reg [DATA_W-1:0] mem [0:(1<<ADDR_W)-1];
integer mem_i;
initial for (mem_i = 0; mem_i < (1<<ADDR_W); mem_i = mem_i + 1) mem[mem_i] = 0;

always @(posedge clk) begin
    if (ce && we)
        mem[addr] <= wdata;
end

assign rdata = mem[addr];

`endif

endmodule