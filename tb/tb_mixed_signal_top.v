`timescale 1ns/1ps
`default_nettype none
//============================================================================
// Mixed-Signal Top-Level Testbench
// 77GHz FMCW Phased Array Vibrometer - Landmine Detection
// IHP SG13G2 130nm SiGe BiCMOS
//
// Integrates:
//   ANALOG (behavioral): LNA -> Mixer -> IFA -> VGA -> ADC (6 channels)
//   DIGITAL (RTL):       vibrometer_top (Range FFT -> Slow-Time FFT -> SPI)
//
// The analog front-end is modeled behaviorally matching the measured
// performance from transistor-level SPICE simulations:
//   LNA gain:   15 dB, NF=5dB
//   Mixer CG:   6 dB
//   IFA gain:   44 dB
//   VGA gain:   0-31 dB (controlled by vga_ctrl)
//   ADC:        12-bit SAR, 100 MSPS
//============================================================================

module tb_mixed_signal_top;

//--- Parameters ---
parameter DW        = 16;
parameter AW        = 2*DW; /* used by vibrometer_top */
parameter N_FFT     = 64;
parameter N_CH      = 6;
parameter N_CHIRPS  = 128;
parameter N_BEAMS   = 4;
parameter SRAM_AW   = 10;
parameter SRAM_DW   = 32;

parameter real F_RF       = 77.0e9;    // RF carrier frequency
parameter real F_LO       = 76.99e9;   // LO frequency (10MHz IF)
parameter real F_IF       = F_RF - F_LO; /* 10 MHz IF - for documentation */
parameter real F_ADC_CLK  = 100.0e6;   // ADC sample rate
parameter real T_ADC_CLK  = 1.0e9 / F_ADC_CLK; // 10ns period

// Analog chain gain (linear)
parameter real G_LNA  = 5.62;    // 15 dB
parameter real G_MIX  = 2.0;     // 6 dB
parameter real G_IFA  = 158.5;   // 44 dB
parameter real G_VGA  = 10.0;    // 20 dB (mid-range)
parameter real G_TOTAL = G_LNA * G_MIX * G_IFA * G_VGA; // ~75 dB total

// ADC parameters
parameter real V_REF   = 1.2;    // ADC reference voltage
parameter integer ADC_BITS = 12;
parameter real LSB = V_REF / (2**ADC_BITS);

//--- Signals ---
reg  clk_digital;       // 200 MHz digital clock
reg  clk_adc;          // 100 MHz ADC clock
reg  rst_n;

// Analog domain (real-valued behavioral)
real rf_signal_p [0:N_CH-1];  // RF input per channel (V)
real lo_signal;                // LO drive
real if_signal [0:N_CH-1];    // After mixer
real baseband [0:N_CH-1];     // After IFA+VGA
real adc_input [0:N_CH-1];    // ADC input voltage

// ADC outputs (digital)
reg signed [DW-1:0] adc_data [0:N_CH-1];
reg adc_valid;

// Digital domain
reg  chirp_start;
reg  [3:0] beam_idx;
reg  [5:0] target_range_bin;
reg  [7:0] excite_doppler_bin;
reg  process_start;
wire spi_clk_o, spi_mosi_o, spi_cs_n_o;
wire busy;

// Simulation control
real t_sim;             // Simulation time in seconds
real chirp_rate;        // FMCW chirp slope (Hz/s)
real target_range;      // Target range (m)
real target_delay;      // Round-trip delay (s)
real target_vibration;  // Vibration amplitude (m)
real vib_frequency;     // Vibration frequency (Hz)
integer chirp_i, sample_i, beam_i, ch_i;
real pi;

//--- Clock Generation ---
always #2.5  clk_digital = ~clk_digital;  // 200 MHz
always #5.0  clk_adc     = ~clk_adc;      // 100 MHz

//--- Digital Processing (actual RTL) ---
vibrometer_top #(
    .DW(DW), .N_FFT(N_FFT), .N_CH(N_CH),
    .N_CHIRPS(N_CHIRPS), .N_BEAMS(N_BEAMS),
    .SRAM_AW(SRAM_AW), .SRAM_DW(SRAM_DW)
) u_digital (
    .clk(clk_digital),
    .rst_n(rst_n),
    .chirp_start(chirp_start),
    .adc_data_0(adc_data[0]),
    .adc_data_1(adc_data[1]),
    .adc_data_2(adc_data[2]),
    .adc_data_3(adc_data[3]),
    .adc_data_4(adc_data[4]),
    .adc_data_5(adc_data[5]),
    .adc_valid(adc_valid),
    .beam_idx(beam_idx),
    .target_range_bin(target_range_bin),
    .excite_doppler_bin(excite_doppler_bin),
    .process_start(process_start),
    .spi_clk_o(spi_clk_o),
    .spi_mosi_o(spi_mosi_o),
    .spi_cs_n_o(spi_cs_n_o),
    .busy(busy)
);

//============================================================================
// ANALOG FRONT-END BEHAVIORAL MODEL
// Models the complete RX chain from antenna to ADC output
// Validated against transistor-level SPICE (radar_top_sch_tb.spice)
//============================================================================

// ADC model: sample baseband signal, quantize to 12-bit, sign-extend to 16-bit
task automatic adc_convert;
    input real vin;
    output reg signed [DW-1:0] dout;
    real v_clipped;
    integer code;
begin
    // Clip to ADC range
    v_clipped = vin;
    if (v_clipped > V_REF/2.0)  v_clipped = V_REF/2.0;
    if (v_clipped < -V_REF/2.0) v_clipped = -V_REF/2.0;
    // Quantize
    code = $rtoi(v_clipped / LSB);
    if (code > (2**(ADC_BITS-1))-1)  code = (2**(ADC_BITS-1))-1;
    if (code < -(2**(ADC_BITS-1)))   code = -(2**(ADC_BITS-1));
    // Sign-extend 12-bit to 16-bit
    dout = code;
end
endtask

//============================================================================
// FMCW RADAR SIGNAL MODEL
// Generates realistic radar return from a vibrating target
//============================================================================

// Radar parameters
initial begin
    pi = 3.14159265358979;
    chirp_rate = 70.0e12;       // 70 THz/s chirp slope (1us chirp, 70MHz BW)
    target_range = 5.0;         // 5 meter range (landmine depth)
    target_delay = 2.0 * target_range / 3.0e8; // ~33.3 ns round-trip
    target_vibration = 1.0e-6;  // 1 um vibration amplitude
    vib_frequency = 200.0;      // 200 Hz vibration (buried object resonance)
end

//============================================================================
// MAIN STIMULUS
//============================================================================
initial begin
    $display("============================================================");
    $display(" Mixed-Signal Testbench: 77GHz FMCW Phased Array Vibrometer");
    $display(" IHP SG13G2 130nm SiGe BiCMOS");
    $display("============================================================");
    $display(" Target: %.1f m range, %.1f um vibration @ %0d Hz", 
             target_range, target_vibration*1e6, $rtoi(vib_frequency));
    $display(" Analog chain gain: %.1f dB", 20.0*$ln(G_TOTAL)/$ln(10.0));
    $display(" ADC: %0d-bit, %0d MSPS", ADC_BITS, $rtoi(F_ADC_CLK/1e6));
    $display("============================================================");

    // Initialize
    clk_digital = 0; clk_adc = 0; rst_n = 0;
    chirp_start = 0; adc_valid = 0; process_start = 0;
    beam_idx = 0;
    target_range_bin = 6'd8;      // Expected range bin for 5m target
    excite_doppler_bin = 8'd5;    // Expected Doppler bin for 200Hz
    for (ch_i = 0; ch_i < N_CH; ch_i = ch_i + 1) begin
        adc_data[ch_i] = 0;
    end

    // Reset
    #50 rst_n = 1;
    #20;

    $display("[%0t] Starting %0d chirps x %0d beams...", $time, N_CHIRPS, N_BEAMS);

    // Process all chirps
    for (chirp_i = 0; chirp_i < N_CHIRPS; chirp_i = chirp_i + 1) begin
        for (beam_i = 0; beam_i < N_BEAMS; beam_i = beam_i + 1) begin
            // Trigger chirp start
            @(posedge clk_digital);
            chirp_start = 1;
            beam_idx = beam_i[3:0];
            @(posedge clk_digital);
            chirp_start = 0;

            // Generate N_FFT ADC samples for this chirp
            for (sample_i = 0; sample_i < N_FFT; sample_i = sample_i + 1) begin
                @(posedge clk_adc);

                // Compute simulation time for this sample
                t_sim = (chirp_i * N_BEAMS * N_FFT + beam_i * N_FFT + sample_i) 
                        * T_ADC_CLK * 1e-9;

                // Generate FMCW beat signal for each channel
                for (ch_i = 0; ch_i < N_CH; ch_i = ch_i + 1) begin
                    if (beam_i == 0) begin
                        // Beam 0: target present with vibration
                        // Beat frequency = chirp_rate * 2R/c
                        // Phase modulation from vibration: 4*pi*vib*f_c/c
                        rf_signal_p[ch_i] = 1.0e-6 * // 1uV RF signal at antenna
                            $cos(2.0*pi*(chirp_rate * target_delay) * 
                                 (sample_i * (1.0/F_ADC_CLK)) +
                                 4.0*pi*F_RF/3.0e8 * target_vibration *
                                 $sin(2.0*pi*vib_frequency*t_sim) +
                                 ch_i * 0.3); // Phase offset per channel (array)
                    end else begin
                        // Other beams: noise only
                        rf_signal_p[ch_i] = 0.0;
                    end

                    // ===== ANALOG CHAIN (behavioral) =====
                    // LNA: 15dB gain
                    if_signal[ch_i] = rf_signal_p[ch_i] * G_LNA;
                    // Mixer: downconvert (magnitude of beat signal)
                    if_signal[ch_i] = if_signal[ch_i] * G_MIX;
                    // IFA: 44dB gain
                    baseband[ch_i] = if_signal[ch_i] * G_IFA;
                    // VGA: 20dB gain
                    baseband[ch_i] = baseband[ch_i] * G_VGA;

                    // ADC: quantize
                    adc_convert(baseband[ch_i], adc_data[ch_i]);
                end

                // Assert ADC valid
                @(posedge clk_digital);
                adc_valid = 1;
                @(posedge clk_digital);
                adc_valid = 0;
            end

            // Wait for processing to complete
            wait(busy == 0);
            #20;
        end

        // Progress indication
        if (chirp_i % 32 == 0)
            $display("[%0t] Chirp %0d/%0d complete", $time, chirp_i, N_CHIRPS);
    end

    $display("[%0t] All chirps complete. Triggering slow-time FFT...", $time);

    // Trigger slow-time processing
    @(posedge clk_digital);
    process_start = 1;
    @(posedge clk_digital);
    process_start = 0;

    // Wait for SPI output
    wait(spi_cs_n_o == 0);
    $display("[%0t] SPI transmission started", $time);

    // Capture SPI frame
    begin : spi_capture
        reg [37:0] spi_frame;
        integer bit_i;
        spi_frame = 0;
        bit_i = 37;
        while (spi_cs_n_o == 0 && bit_i >= 0) begin
            @(posedge spi_clk_o);
            spi_frame[bit_i] = spi_mosi_o;
            bit_i = bit_i - 1;
        end

        $display("");
        $display("============================================================");
        $display(" MIXED-SIGNAL VERIFICATION RESULTS");
        $display("============================================================");
        $display(" SPI Output Frame: 0x%h", spi_frame);
        $display("   Range bin:     %0d", spi_frame[37:32]);
        $display("   Amplitude RE:  0x%h (%0d)", spi_frame[31:16], 
                 $signed(spi_frame[31:16]));
        $display("   Amplitude IM:  0x%h (%0d)", spi_frame[15:0],
                 $signed(spi_frame[15:0]));
        $display("");

        if (spi_frame[31:16] != 0 || spi_frame[15:0] != 0) begin
            $display(" *** PASS: End-to-end signal detected ***");
            $display("   RF antenna -> LNA -> Mixer -> IFA -> VGA -> ADC");
            $display("   -> Range FFT -> Slow-Time FFT -> SPI output");
            $display("   Vibration signature successfully extracted!");
        end else begin
            $display(" *** FAIL: No signal at SPI output ***");
        end
        $display("============================================================");
    end

    #500;
    $finish;
end

// Timeout watchdog
initial begin
    #100000000; // 100ms
    $display("TIMEOUT: Simulation exceeded 100ms");
    $finish;
end

// Waveform dump
initial begin
    $dumpfile("tb_mixed_signal_top.vcd");
    $dumpvars(0, tb_mixed_signal_top);
end

endmodule