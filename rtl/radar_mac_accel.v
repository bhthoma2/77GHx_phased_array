`timescale 1ns/1ps
module radar_mac_accel #(
    parameter DW    = 16,
    parameter N_FFT = 64,
    parameter N_CH  = 6,
    parameter N_MAC = 4,
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
    output reg  signed [AW-1:0] result_re,
    output reg  signed [AW-1:0] result_im,
    output reg  [5:0]           result_bin,
    output reg                  result_valid,
    output wire                 busy
);

localparam [5:0] LOG2_N = 6;
localparam [5:0] N_HALF = N_FFT[5:0] / 2;
localparam [5:0] N_FFT_M1 = N_FFT[5:0] - 6'd1;
localparam [5:0] N_HALF_M1 = N_HALF - 6'd1;
localparam [2:0] N_CH_M1 = N_CH[2:0] - 3'd1;

localparam [2:0] S_IDLE = 3'd0,
                 S_LOAD = 3'd1,
                 S_FFT  = 3'd2,
                 S_BEAM = 3'd3,
                 S_MAG  = 3'd4,
                 S_OUT  = 3'd5;

reg [2:0] state, state_nxt;
reg [5:0] sample_cnt;
reg [2:0] fft_stage;
reg [5:0] bfly_idx;
reg [2:0] ch_idx;
reg [5:0] bin_idx;
reg [1:0] cyc_cnt;

assign busy = (state != S_IDLE);

reg signed [DW-1:0] buf_re [0:N_CH-1][0:N_FFT-1];
reg signed [DW-1:0] buf_im [0:N_CH-1][0:N_FFT-1];

reg signed [DW-1:0] beam_re [0:N_FFT-1];
reg signed [DW-1:0] beam_im [0:N_FFT-1];

reg signed [AW-1:0] mac_acc [0:N_MAC-1];
reg signed [DW-1:0] mac_a   [0:N_MAC-1];
reg signed [DW-1:0] mac_b   [0:N_MAC-1];
reg                 mac_clr [0:N_MAC-1];

reg signed [AW-1:0] mag_max;
reg [5:0]           mag_max_bin;

integer i;

// Butterfly index computation (combinational)
wire [5:0] half_stride = 6'd1 << fft_stage;
wire [5:0] stride      = half_stride << 1;
wire [5:0] bfly_group  = bfly_idx / half_stride;
wire [5:0] bfly_offset = bfly_idx % half_stride;
wire [5:0] p_idx       = bfly_group * stride + bfly_offset;
wire [5:0] q_idx       = p_idx + half_stride;
wire [5:0] tw_idx      = bfly_offset * (N_HALF >> fft_stage);

// Twiddle factor ROM (synthesizable — hardcoded for 64-pt FFT)
// Q14 format: value = cos/sin * 2^14
reg signed [DW-1:0] tw_cos_val;
reg signed [DW-1:0] tw_sin_val;

always @(*) begin
    case (tw_idx)
     6'd0:  begin tw_cos_val =  16'd16384; tw_sin_val =  16'd0;     end
     6'd1:  begin tw_cos_val =  16'd16364; tw_sin_val = -16'd1608;  end
     6'd2:  begin tw_cos_val =  16'd16305; tw_sin_val = -16'd3212;  end
     6'd3:  begin tw_cos_val =  16'd16207; tw_sin_val = -16'd4808;  end
     6'd4:  begin tw_cos_val =  16'd16069; tw_sin_val = -16'd6393;  end
     6'd5:  begin tw_cos_val =  16'd15893; tw_sin_val = -16'd7962;  end
     6'd6:  begin tw_cos_val =  16'd15679; tw_sin_val = -16'd9512;  end
     6'd7:  begin tw_cos_val =  16'd15426; tw_sin_val = -16'd11039; end
     6'd8:  begin tw_cos_val =  16'd15137; tw_sin_val = -16'd12540; end
     6'd9:  begin tw_cos_val =  16'd14811; tw_sin_val = -16'd14010; end
     6'd10: begin tw_cos_val =  16'd14449; tw_sin_val = -16'd15447; end
     6'd11: begin tw_cos_val =  16'd14053; tw_sin_val = -16'd16846; end
     6'd12: begin tw_cos_val =  16'd13623; tw_sin_val = -16'd18204; end
     6'd13: begin tw_cos_val =  16'd13160; tw_sin_val = -16'd19519; end
     6'd14: begin tw_cos_val =  16'd12665; tw_sin_val = -16'd20787; end
     6'd15: begin tw_cos_val =  16'd12140; tw_sin_val = -16'd22005; end
     6'd16: begin tw_cos_val =  16'd11585; tw_sin_val = -16'd11585; end
     6'd17: begin tw_cos_val =  16'd11003; tw_sin_val = -16'd12167; end
     6'd18: begin tw_cos_val =  16'd10394; tw_sin_val = -16'd12721; end
     6'd19: begin tw_cos_val =  16'd9760;  tw_sin_val = -16'd13248; end
     6'd20: begin tw_cos_val =  16'd9102;  tw_sin_val = -16'd13746; end
     6'd21: begin tw_cos_val =  16'd8423;  tw_sin_val = -16'd14214; end
     6'd22: begin tw_cos_val =  16'd7723;  tw_sin_val = -16'd14654; end
     6'd23: begin tw_cos_val =  16'd7005;  tw_sin_val = -16'd15064; end
     6'd24: begin tw_cos_val =  16'd6270;  tw_sin_val = -16'd15446; end
     6'd25: begin tw_cos_val =  16'd5520;  tw_sin_val = -16'd15798; end
     6'd26: begin tw_cos_val =  16'd4756;  tw_sin_val = -16'd16121; end
     6'd27: begin tw_cos_val =  16'd3981;  tw_sin_val = -16'd16414; end
     6'd28: begin tw_cos_val =  16'd3196;  tw_sin_val = -16'd16679; end
     6'd29: begin tw_cos_val =  16'd2404;  tw_sin_val = -16'd16914; end
     6'd30: begin tw_cos_val =  16'd1606;  tw_sin_val = -16'd17121; end
     6'd31: begin tw_cos_val =  16'd804;   tw_sin_val = -16'd17299; end
    default: begin tw_cos_val = 16'd16384; tw_sin_val =  16'd0;     end
    endcase
end

// Magnitude computation (combinational)
wire signed [DW-1:0] mag_re_abs = beam_re[bin_idx] < 0 ? -beam_re[bin_idx] : beam_re[bin_idx];
wire signed [DW-1:0] mag_im_abs = beam_im[bin_idx] < 0 ? -beam_im[bin_idx] : beam_im[bin_idx];
wire signed [AW-1:0] mag_val    = $signed({{AW-DW{1'b0}}, mag_re_abs}) + $signed({{AW-DW{1'b0}}, mag_im_abs});

// Butterfly writeback computation (combinational)
wire signed [AW-1:0] tw_re_prod = mac_acc[0] - mac_acc[1];
wire signed [AW-1:0] tw_im_prod = mac_acc[2] + mac_acc[3];
wire signed [DW-1:0] tr = $signed(tw_re_prod[DW-2+DW-1:DW-2]);
wire signed [DW-1:0] ti = $signed(tw_im_prod[DW-2+DW-1:DW-2]);

// MAC array
genvar g;
generate
    for (g = 0; g < N_MAC; g = g + 1) begin : mac_gen
        always @(posedge clk or negedge rst_n) begin
            if (!rst_n)
                mac_acc[g] <= {AW{1'b0}};
            else if (mac_clr[g])
                mac_acc[g] <= {AW{1'b0}};
            else
                mac_acc[g] <= mac_acc[g] + AW'(mac_a[g]) * AW'(mac_b[g]);
        end
    end
endgenerate

// State register
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        state <= S_IDLE;
    else
        state <= state_nxt;
end

// Next state logic
always @(*) begin
    state_nxt = state;
    case (state)
        S_IDLE: if (start)                                             state_nxt = S_LOAD;
        S_LOAD: if (sample_cnt == N_FFT_M1 && adc_valid)              state_nxt = S_FFT;
        S_FFT:  if (fft_stage == LOG2_N[2:0] && cyc_cnt == 2'd0)      state_nxt = S_BEAM;
        S_BEAM: if (bin_idx == N_FFT_M1 && ch_idx == N_CH_M1 && cyc_cnt == 2'd2) state_nxt = S_MAG;
        S_MAG:  if (bin_idx == N_FFT_M1)                              state_nxt = S_OUT;
        S_OUT:                                                         state_nxt = S_IDLE;
        default:                                                       state_nxt = S_IDLE;
    endcase
end

// Datapath
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        sample_cnt <= 6'd0;
        fft_stage <= 3'd0;
        bfly_idx <= 6'd0;
        ch_idx <= 3'd0;
        bin_idx <= 6'd0;
        cyc_cnt <= 2'd0;
        result_valid <= 1'b0;
        result_re <= {AW{1'b0}};
        result_im <= {AW{1'b0}};
        result_bin <= 6'd0;
        mag_max <= {AW{1'b0}};
        mag_max_bin <= 6'd0;
        for (i = 0; i < N_MAC; i = i + 1) begin
            mac_a[i] <= {DW{1'b0}};
            mac_b[i] <= {DW{1'b0}};
            mac_clr[i] <= 1'b1;
        end
    end else begin
        result_valid <= 1'b0;
        for (i = 0; i < N_MAC; i = i + 1)
            mac_clr[i] <= 1'b0;

        case (state)
        S_IDLE: begin
            sample_cnt <= 6'd0;
            fft_stage <= 3'd0;
            bfly_idx <= 6'd0;
            ch_idx <= 3'd0;
            bin_idx <= 6'd0;
            cyc_cnt <= 2'd0;
            mag_max <= {AW{1'b0}};
            mag_max_bin <= 6'd0;
        end

        S_LOAD: begin
            if (adc_valid) begin
                buf_re[0][sample_cnt] <= adc_data_0;
                buf_re[1][sample_cnt] <= adc_data_1;
                buf_re[2][sample_cnt] <= adc_data_2;
                buf_re[3][sample_cnt] <= adc_data_3;
                buf_re[4][sample_cnt] <= adc_data_4;
                buf_re[5][sample_cnt] <= adc_data_5;
                buf_im[0][sample_cnt] <= {DW{1'b0}};
                buf_im[1][sample_cnt] <= {DW{1'b0}};
                buf_im[2][sample_cnt] <= {DW{1'b0}};
                buf_im[3][sample_cnt] <= {DW{1'b0}};
                buf_im[4][sample_cnt] <= {DW{1'b0}};
                buf_im[5][sample_cnt] <= {DW{1'b0}};
                sample_cnt <= sample_cnt + 6'd1;
            end
        end

        S_FFT: begin
            case (cyc_cnt)
            2'd0: begin
                mac_clr[0] <= 1'b1;
                mac_clr[1] <= 1'b1;
                mac_clr[2] <= 1'b1;
                mac_clr[3] <= 1'b1;
                mac_a[0] <= buf_re[ch_idx][q_idx];
                mac_b[0] <= tw_cos_val;
                mac_a[1] <= buf_im[ch_idx][q_idx];
                mac_b[1] <= tw_sin_val;
                mac_a[2] <= buf_re[ch_idx][q_idx];
                mac_b[2] <= tw_sin_val;
                mac_a[3] <= buf_im[ch_idx][q_idx];
                mac_b[3] <= tw_cos_val;
                cyc_cnt <= 2'd1;
            end
            2'd1: begin
                cyc_cnt <= 2'd2;
            end
            2'd2: begin
                buf_re[ch_idx][p_idx] <= buf_re[ch_idx][p_idx] + tr;
                buf_im[ch_idx][p_idx] <= buf_im[ch_idx][p_idx] + ti;
                buf_re[ch_idx][q_idx] <= buf_re[ch_idx][p_idx] - tr;
                buf_im[ch_idx][q_idx] <= buf_im[ch_idx][p_idx] - ti;
                cyc_cnt <= 2'd0;
                if (bfly_idx == N_HALF_M1) begin
                    bfly_idx <= 6'd0;
                    if (ch_idx == N_CH_M1) begin
                        ch_idx <= 3'd0;
                        fft_stage <= fft_stage + 3'd1;
                    end else begin
                        ch_idx <= ch_idx + 3'd1;
                    end
                end else begin
                    bfly_idx <= bfly_idx + 6'd1;
                end
            end
            default: cyc_cnt <= 2'd0;
            endcase
        end

        S_BEAM: begin
            case (cyc_cnt)
            2'd0: begin
                mac_clr[0] <= (ch_idx == 3'd0);
                mac_clr[1] <= (ch_idx == 3'd0);
                mac_a[0] <= buf_re[ch_idx][bin_idx];
                mac_b[0] <= {{DW-1{1'b0}}, 1'b1};
                mac_a[1] <= buf_im[ch_idx][bin_idx];
                mac_b[1] <= {{DW-1{1'b0}}, 1'b1};
                cyc_cnt <= 2'd1;
            end
            2'd1: begin
                cyc_cnt <= 2'd2;
            end
            2'd2: begin
                if (ch_idx == N_CH_M1) begin
                    beam_re[bin_idx] <= $signed(mac_acc[0][DW-1:0]);
                    beam_im[bin_idx] <= $signed(mac_acc[1][DW-1:0]);
                    ch_idx <= 3'd0;
                    if (bin_idx == N_FFT_M1)
                        bin_idx <= 6'd0;
                    else
                        bin_idx <= bin_idx + 6'd1;
                end else begin
                    ch_idx <= ch_idx + 3'd1;
                end
                cyc_cnt <= 2'd0;
            end
            default: cyc_cnt <= 2'd0;
            endcase
        end

        S_MAG: begin
            if (mag_val > mag_max) begin
                mag_max <= mag_val;
                mag_max_bin <= bin_idx;
            end
            bin_idx <= bin_idx + 6'd1;
        end

        S_OUT: begin
            result_re <= $signed({{AW-DW{beam_re[mag_max_bin][DW-1]}}, beam_re[mag_max_bin]});
            result_im <= $signed({{AW-DW{beam_im[mag_max_bin][DW-1]}}, beam_im[mag_max_bin]});
            result_bin <= mag_max_bin;
            result_valid <= 1'b1;
        end
        default: begin end
        endcase
    end
end

endmodule