module spi_serializer #(
    parameter DW = 32,
    parameter FRAME_BITS = 38
)(
    input  wire             clk,
    input  wire             rst_n,
    input  wire [DW-1:0]    data_re,
    input  wire [DW-1:0]    data_im,
    input  wire [5:0]       data_bin,
    input  wire             data_valid,
    output reg              spi_clk,
    output reg              spi_mosi,
    output reg              spi_cs_n,
    output wire             ready
);

localparam [1:0] S_IDLE = 2'd0,
                 S_DATA = 2'd1;

reg [1:0] state;
reg [5:0] bit_cnt;
reg [FRAME_BITS-1:0] shift_reg;
reg clk_phase;

assign ready = (state == S_IDLE);

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        state <= S_IDLE;
        bit_cnt <= 6'd0;
        shift_reg <= {FRAME_BITS{1'b0}};
        spi_clk <= 1'b0;
        spi_mosi <= 1'b0;
        spi_cs_n <= 1'b1;
        clk_phase <= 1'b0;
    end else begin
        case (state)
        S_IDLE: begin
            spi_cs_n <= 1'b1;
            spi_clk <= 1'b0;
            if (data_valid) begin
                shift_reg <= {data_bin, data_re[DW-1:DW-16], data_im[DW-1:DW-16]};
                bit_cnt <= FRAME_BITS[5:0] - 6'd1;
                state <= S_DATA;
                spi_cs_n <= 1'b0;
                clk_phase <= 1'b0;
            end
        end
        S_DATA: begin
            clk_phase <= ~clk_phase;
            if (clk_phase == 1'b0) begin
                spi_mosi <= shift_reg[FRAME_BITS-1];
                spi_clk <= 1'b0;
            end else begin
                spi_clk <= 1'b1;
                shift_reg <= {shift_reg[FRAME_BITS-2:0], 1'b0};
                if (bit_cnt == 6'd0)
                    state <= S_IDLE;
                else
                    bit_cnt <= bit_cnt - 6'd1;
            end
        end
        default: state <= S_IDLE;
        endcase
    end
end

endmodule