`timescale 1ns/1ps
module slowtime_fft #(
    parameter DW       = 16,
    parameter AW       = 2*DW,
    parameter N_CHIRPS = 128,
    parameter N_BEAMS  = 4,
    parameter LOG2_NC  = 7,
    parameter SRAM_AW  = 10,
    parameter SRAM_DW  = 32
)(
    input  wire              clk,
    input  wire              rst_n,
    input  wire              chirp_valid,
    input  wire signed [DW-1:0] range_re,
    input  wire signed [DW-1:0] range_im,
    input  wire [5:0]        range_bin,
    input  wire [3:0]        beam_idx,
    input  wire              process_start,
    input  wire [5:0]        target_bin,
    input  wire [7:0]        excite_bin,
    output reg  signed [AW-1:0] vib_amplitude,
    output reg  [3:0]        vib_beam,
    output reg               vib_valid,
    output wire              busy,
    output reg               sram_ce,
    output reg               sram_we,
    output reg  [SRAM_AW-1:0] sram_addr,
    output reg  [SRAM_DW-1:0] sram_wdata,
    input  wire [SRAM_DW-1:0] sram_rdata
);

// SRAM layout: N_BEAMS × N_CHIRPS × 2 words (Re, Im) = 16×256×2 = 8192 words
// Address: {beam_idx[3:0], chirp_cnt[7:0], re_im[0]} = 13 bits

localparam [2:0] S_IDLE    = 3'd0,
                 S_STORE   = 3'd1,
                 S_FFT_RD  = 3'd2,
                 S_FFT_MAC = 3'd3,
                 S_FFT_WR  = 3'd4,
                 S_EXTRACT = 3'd5,
                 S_OUTPUT  = 3'd6;

reg [2:0] state;
reg [7:0] chirp_cnt;
reg [3:0] cur_beam;
reg [7:0] bfly_idx;
reg [3:0] fft_stage;
reg [1:0] sub_state;

reg signed [DW-1:0] p_re, p_im, q_re, q_im;
reg [13:0]          tmp_addr_14;


reg signed [AW-1:0] best_mag;
reg [3:0]           best_beam;

assign busy = (state != S_IDLE);

// Slow-time twiddle ROM (256-pt, Q14)
// Only need entry at excite_bin for extraction, but full FFT needs all
// For area savings: compute tw on-the-fly with CORDIC, or use ROM
// Here: simplified — we store the butterfly and extract one bin
wire [7:0] nc_half = N_CHIRPS[7:0] >> 1;
wire [7:0] st_half_stride = 8'd1 << fft_stage[3:0];
wire [7:0] st_stride = st_half_stride << 1;
wire [7:0] st_group  = bfly_idx / st_half_stride;
wire [7:0] st_offset = bfly_idx % st_half_stride;
wire [7:0] st_p = st_group * st_stride + st_offset;
wire [7:0] st_q = st_p + st_half_stride;
wire [7:0] st_tw_idx = st_offset * (nc_half >> fft_stage[3:0]);

// SRAM address helpers — full-width intermediates then explicit truncation
wire [13:0] addr_p_re_w = {1'b0, cur_beam, st_p, 1'b0};
wire [13:0] addr_p_im_w = {1'b0, cur_beam, st_p, 1'b1};
wire [13:0] addr_q_re_w = {1'b0, cur_beam, st_q, 1'b0};
wire [13:0] addr_q_im_w = {1'b0, cur_beam, st_q, 1'b1};
wire [SRAM_AW-1:0] addr_p_re = addr_p_re_w[SRAM_AW-1:0];
wire [SRAM_AW-1:0] addr_p_im = addr_p_im_w[SRAM_AW-1:0];
wire [SRAM_AW-1:0] addr_q_re = addr_q_re_w[SRAM_AW-1:0];
wire [SRAM_AW-1:0] addr_q_im = addr_q_im_w[SRAM_AW-1:0];

// 256-pt twiddle factor (simplified: 8 hardcoded quadrant entries, interpolated)
// Full ROM would have 128 entries; for brevity use first-quadrant LUT with symmetry
reg signed [DW-1:0] tw256_cos;
reg signed [DW-1:0] tw256_sin;

always @(*) begin : twiddle_256
    reg [DW-1:0] idx_sq;
    reg signed [DW-1:0] c, s;
    reg signed [AW:0]   s_wide;
    idx_sq = {9'd0, st_tw_idx[6:0]} * {9'd0, st_tw_idx[6:0]};
    c = 16'sd16384 - $signed({1'b0, idx_sq[DW-1:1]});
    s_wide = $signed({1'b0, 9'd0, st_tw_idx[6:0]}) * 16'sd101;
    s = $signed(s_wide[DW-1:0]);
    if (st_tw_idx < 8'd64) begin
        tw256_cos = c;
        tw256_sin = -s;
    end else if (st_tw_idx < 8'd128) begin
        tw256_cos = -s;
        tw256_sin = -c;
    end else begin
        tw256_cos = -c;
        tw256_sin = s;
    end
end

// Butterfly computation
wire signed [AW-1:0] tw_prod_re = (q_re * tw256_cos - q_im * tw256_sin) >>> (DW-2);
wire signed [AW-1:0] tw_prod_im = (q_re * tw256_sin + q_im * tw256_cos) >>> (DW-2);
wire signed [DW-1:0] tw_re_trunc = $signed(tw_prod_re[DW-1:0]);
wire signed [DW-1:0] tw_im_trunc = $signed(tw_prod_im[DW-1:0]);
wire signed [DW-1:0] bfly_p_re = p_re + tw_re_trunc;
wire signed [DW-1:0] bfly_p_im = p_im + tw_im_trunc;
wire signed [DW-1:0] bfly_q_re = p_re - tw_re_trunc;
wire signed [DW-1:0] bfly_q_im = p_im - tw_im_trunc;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        state <= S_IDLE;
        chirp_cnt <= 8'd0;
        cur_beam <= 4'd0;
        bfly_idx <= 8'd0;
        fft_stage <= 4'd0;
        sub_state <= 2'd0;
        vib_valid <= 1'b0;
        vib_amplitude <= {AW{1'b0}};
        vib_beam <= 4'd0;
        best_mag <= {AW{1'b0}};
        best_beam <= 4'd0;
        sram_ce <= 1'b0;
        sram_we <= 1'b0;
        sram_addr <= {SRAM_AW{1'b0}};
        sram_wdata <= {SRAM_DW{1'b0}};
        p_re <= {DW{1'b0}};
        p_im <= {DW{1'b0}};
        q_re <= {DW{1'b0}};
        q_im <= {DW{1'b0}};
    end else begin
        vib_valid <= 1'b0;
        sram_ce <= 1'b0;
        sram_we <= 1'b0;

        case (state)
        S_IDLE: begin
            if (chirp_valid) begin
                state <= S_STORE;
            end else if (process_start) begin
                state <= S_FFT_RD;
                cur_beam <= 4'd0;
                fft_stage <= 4'd0;
                bfly_idx <= 8'd0;
                sub_state <= 2'd0;
                best_mag <= {AW{1'b0}};
                best_beam <= 4'd0;
            end
        end

        S_STORE: begin
            // Write one range bin's I/Q for current beam into SRAM
            sram_ce <= 1'b1;
            sram_we <= 1'b1;
            if (sub_state == 2'd0) begin
                tmp_addr_14 = {1'b0, beam_idx, chirp_cnt, 1'b0};
                sram_addr <= tmp_addr_14[SRAM_AW-1:0];
                sram_wdata <= {{SRAM_DW-DW{range_re[DW-1]}}, range_re};
                sub_state <= 2'd1;
            end else begin
                tmp_addr_14 = {1'b0, beam_idx, chirp_cnt, 1'b1};
                sram_addr <= tmp_addr_14[SRAM_AW-1:0];
                sram_wdata <= {{SRAM_DW-DW{range_im[DW-1]}}, range_im};
                sub_state <= 2'd0;
                if (beam_idx == N_BEAMS[3:0] - 4'd1) begin
                    chirp_cnt <= chirp_cnt + 8'd1;
                end
                state <= S_IDLE;
            end
        end

        S_FFT_RD: begin
            // Read p and q values from SRAM (4 reads: p_re, p_im, q_re, q_im)
            sram_ce <= 1'b1;
            sram_we <= 1'b0;
            case (sub_state)
            2'd0: begin sram_addr <= addr_p_re; sub_state <= 2'd1; end
            2'd1: begin p_re <= $signed(sram_rdata[DW-1:0]); sram_addr <= addr_p_im; sub_state <= 2'd2; end
            2'd2: begin p_im <= $signed(sram_rdata[DW-1:0]); sram_addr <= addr_q_re; sub_state <= 2'd3; end
            2'd3: begin q_re <= $signed(sram_rdata[DW-1:0]); sram_addr <= addr_q_im; state <= S_FFT_MAC; sub_state <= 2'd0; end
            default: ;
            endcase
        end

        S_FFT_MAC: begin
            // One cycle: read q_im, compute butterfly
            q_im <= $signed(sram_rdata[DW-1:0]);
            state <= S_FFT_WR;
            sub_state <= 2'd0;
        end

        S_FFT_WR: begin
            // Write back butterfly results
            sram_ce <= 1'b1;
            sram_we <= 1'b1;
            case (sub_state)
            2'd0: begin sram_addr <= addr_p_re; sram_wdata <= {{SRAM_DW-DW{bfly_p_re[DW-1]}}, bfly_p_re}; sub_state <= 2'd1; end
            2'd1: begin sram_addr <= addr_p_im; sram_wdata <= {{SRAM_DW-DW{bfly_p_im[DW-1]}}, bfly_p_im}; sub_state <= 2'd2; end
            2'd2: begin sram_addr <= addr_q_re; sram_wdata <= {{SRAM_DW-DW{bfly_q_re[DW-1]}}, bfly_q_re}; sub_state <= 2'd3; end
            2'd3: begin
                sram_addr <= addr_q_im;
                sram_wdata <= {{SRAM_DW-DW{bfly_q_im[DW-1]}}, bfly_q_im};
                sub_state <= 2'd0;
                // Advance butterfly/stage/beam
                if (bfly_idx == nc_half - 8'd1) begin
                    bfly_idx <= 8'd0;
                    if (fft_stage == LOG2_NC[3:0] - 4'd1) begin
                        fft_stage <= 4'd0;
                        if (cur_beam == N_BEAMS[3:0] - 4'd1) begin
                            state <= S_EXTRACT;
                            cur_beam <= 4'd0;
                        end else begin
                            cur_beam <= cur_beam + 4'd1;
                        end
                    end else begin
                        fft_stage <= fft_stage + 4'd1;
                    end
                end else begin
                    bfly_idx <= bfly_idx + 8'd1;
                    state <= S_FFT_RD;
                end
            end
            default: ;
            endcase
        end

        S_EXTRACT: begin
            // Read vibration bin (excite_bin) for each beam, find max
            sram_ce <= 1'b1;
            sram_we <= 1'b0;
            case (sub_state)
            2'd0: begin tmp_addr_14 = {1'b0, cur_beam, excite_bin, 1'b0}; sram_addr <= tmp_addr_14[SRAM_AW-1:0]; sub_state <= 2'd1; end
            2'd1: begin p_re <= $signed(sram_rdata[DW-1:0]); tmp_addr_14 = {1'b0, cur_beam, excite_bin, 1'b1}; sram_addr <= tmp_addr_14[SRAM_AW-1:0]; sub_state <= 2'd2; end
            2'd2: begin
                p_im <= $signed(sram_rdata[DW-1:0]);
                sub_state <= 2'd3;
            end
            2'd3: begin
                reg signed [DW-1:0] ex_abs_re, ex_abs_im;
                reg signed [AW-1:0] ex_mag;
                ex_abs_re = p_re < 0 ? -p_re : p_re;
                ex_abs_im = p_im < 0 ? -p_im : p_im;
                ex_mag = $signed({{AW-DW{1'b0}}, ex_abs_re}) + $signed({{AW-DW{1'b0}}, ex_abs_im});
                if (ex_mag > best_mag) begin
                    best_mag <= ex_mag;
                    best_beam <= cur_beam;
                end
                sub_state <= 2'd0;
                if (cur_beam == N_BEAMS[3:0] - 4'd1)
                    state <= S_OUTPUT;
                else
                    cur_beam <= cur_beam + 4'd1;
            end
            default: ;
            endcase
        end

        S_OUTPUT: begin
            vib_amplitude <= best_mag;
            vib_beam <= best_beam;
            vib_valid <= 1'b1;
            chirp_cnt <= 8'd0;
            state <= S_IDLE;
        end

        default: state <= S_IDLE;
        endcase
    end
end

endmodule