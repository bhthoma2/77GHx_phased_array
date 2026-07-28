import numpy as np

# Load vibrometer raw data
data = np.loadtxt('/home/bthomas3/Videos/77GHz_phased_array/layout/testbenches/simulations/fmcw_vibrometer_raw.dat')
t = data[:, 0]
v_adc = data[:, 1]
v_if_p = data[:, 2]
v_if_n = data[:, 3]

# Parameters
Tchirp = 1e-3
Nchirps = 64
fc = 77e9
c = 3e8
lam = c / fc
BW = 4e9
fb_mine = 2 * BW * 7.0125 / (c * Tchirp)  # 187000 Hz (integer cycles/chirp)
fb_ground = 2 * BW * 3 / (c * Tchirp)  # 80000 Hz

# Use IF signal (differential) for better SNR
v_if = v_if_p - v_if_n

print("=" * 70)
print("  77 GHz FMCW VIBROMETER — Phase Extraction & Vibration Detection")
print("=" * 70)
print(f"  Lambda = {lam*1e3:.3f} mm")
print(f"  Mine beat freq = {fb_mine:.0f} Hz")
print(f"  Ground beat freq = {fb_ground:.0f} Hz")
print()

# For each chirp, extract complex value at mine's range bin via DFT
# This is equivalent to range-FFT then picking the mine bin
phases_mine = []
phases_ground = []
amplitudes_mine = []

for chirp_idx in range(Nchirps):
    t_start = chirp_idx * Tchirp
    t_end = (chirp_idx + 1) * Tchirp
    mask = (t >= t_start) & (t < t_end)
    t_chirp = t[mask]
    v_chirp = v_if[mask]

    if len(t_chirp) < 10:
        continue

    # Resample to uniform grid (high N for accuracy)
    N = 4096
    t_uni = np.linspace(t_start, t_end, N, endpoint=False)
    v_uni = np.interp(t_uni, t_chirp, v_chirp)

    # DTFT at exact beat frequencies using GLOBAL time reference
    # This preserves inter-chirp phase coherence
    X_mine = np.sum(v_uni * np.exp(-1j * 2 * np.pi * fb_mine * t_uni))
    X_ground = np.sum(v_uni * np.exp(-1j * 2 * np.pi * fb_ground * t_uni))

    # Coherent demodulation: remove known static phase advance
    # Static phase = 2π*fb*t_center_of_chirp (arbitrary ref, removed by detrend)
    phases_mine.append(np.angle(X_mine))
    phases_ground.append(np.angle(X_ground))
    amplitudes_mine.append(np.abs(X_mine))

phases_mine = np.array(phases_mine)
phases_ground = np.array(phases_ground)
amplitudes_mine = np.array(amplitudes_mine)

# Remove known inter-chirp phase advance BEFORE unwrapping
# Phase advance per chirp = 2π*fb*Tchirp (from static range)
# Demodulate by multiplying by exp(-j*2π*fb*k*Tchirp)
chirp_indices = np.arange(Nchirps)
chirp_times = chirp_indices * Tchirp

# Coherent demodulation using first chirp as reference
# This removes the large static phase ramp
X_mine_complex = amplitudes_mine * np.exp(1j * phases_mine)
X_mine_demod = X_mine_complex * np.conj(X_mine_complex[0]) / np.abs(X_mine_complex[0])
phases_mine_demod = np.angle(X_mine_demod)
phase_detrended = np.unwrap(phases_mine_demod)
# Remove any residual linear drift
p_mine = np.polyfit(chirp_times, phase_detrended, 1)
phase_detrended = phase_detrended - np.polyval(p_mine, chirp_times)

# Same for ground
X_ground_complex = np.ones(Nchirps) * np.exp(1j * phases_ground)
X_ground_demod = X_ground_complex * np.conj(X_ground_complex[0]) / np.abs(X_ground_complex[0])
phases_ground_demod = np.angle(X_ground_demod)
phase_ground_detrended = np.unwrap(phases_ground_demod)
p_ground = np.polyfit(chirp_times, phase_ground_detrended, 1)
phase_ground_detrended = phase_ground_detrended - np.polyval(p_ground, chirp_times)

# Convert phase to displacement: d = phase * lambda / (4*pi)
displacement = phase_detrended * lam / (4 * np.pi)
displacement_ground = phase_ground_detrended * lam / (4 * np.pi)

print(f"  --- Phase Extraction Results ---")
print(f"  Mine phase variation (peak):   {np.max(phase_detrended)-np.min(phase_detrended):.4f} rad")
print(f"  Ground phase variation (peak): {np.max(phase_ground_detrended)-np.min(phase_ground_detrended):.6f} rad")
print(f"  Mine displacement (peak-peak): {(np.max(displacement)-np.min(displacement))*1e6:.3f} um")
print(f"  Ground displacement (p-p):     {(np.max(displacement_ground)-np.min(displacement_ground))*1e9:.1f} nm")
print()

# FFT of displacement across chirps → vibration spectrum
N_vib = Nchirps
window = np.hanning(N_vib)
d_win = displacement * window
fft_vib = np.fft.rfft(d_win)
f_vib_axis = np.fft.rfftfreq(N_vib, Tchirp)  # PRF = 1/Tchirp = 1kHz

mag_vib = np.abs(fft_vib) / (N_vib / 2) * 1e6  # in micrometers

# Also do ground (should show no vibration)
d_ground_win = displacement_ground * window
fft_ground = np.fft.rfft(d_ground_win)
mag_ground = np.abs(fft_ground) / (N_vib / 2) * 1e6

# Find peak vibration frequency in the 50-400 Hz band (skip DC/drift region)
search_mask = (f_vib_axis > 50) & (f_vib_axis < 400)
search_indices = np.where(search_mask)[0]
peak_idx = search_indices[np.argmax(mag_vib[search_indices])]
f_vib_detected = f_vib_axis[peak_idx]
amp_detected = mag_vib[peak_idx]
# Sum adjacent bins for split-bin correction (Hanning leakage)
if peak_idx > 0 and peak_idx < len(mag_vib) - 1:
    amp_corrected = np.sqrt(mag_vib[peak_idx-1]**2 + mag_vib[peak_idx]**2 + mag_vib[peak_idx+1]**2)
else:
    amp_corrected = amp_detected
# Hanning window amplitude correction factor = 2.0
amp_corrected *= 2.0

print(f"  --- Vibration Spectrum (Slow-Time FFT) ---")
print(f"  PRF (chirp rate):         {1/Tchirp:.0f} Hz")
print(f"  Max detectable vibration: {1/(2*Tchirp):.0f} Hz (Nyquist)")
print(f"  Frequency resolution:     {f_vib_axis[1]:.1f} Hz")
print()
print(f"  {'Freq (Hz)':<12} {'Mine (um)':<12} {'Ground (um)':<12} {'Detection'}")
print(f"  {'-'*12} {'-'*12} {'-'*12} {'-'*12}")
for i in range(1, min(20, len(f_vib_axis))):
    det = ""
    if abs(f_vib_axis[i] - 150) < 20:
        det = "<-- VIBRATION"
    print(f"  {f_vib_axis[i]:<12.1f} {mag_vib[i]:<12.4f} {mag_ground[i]:<12.6f} {det}")

print()
print(f"  *** DETECTED VIBRATION ***")
print(f"  Frequency: {f_vib_detected:.1f} Hz (expected: 150 Hz)")
print(f"  Bin amplitude: {amp_detected:.4f} um")
print(f"  Corrected amplitude: {amp_corrected:.4f} um (expected: 1.000 um)")
print(f"  Ground at same freq: {mag_ground[peak_idx]:.6f} um (noise floor)")
print(f"  SNR: {20*np.log10(mag_vib[peak_idx]/(mag_ground[peak_idx]+1e-15)):.1f} dB")
print()
print("=" * 70)

# Save vibration spectrum to CSV for plotting
outpath = '/home/bthomas3/Videos/77GHz_phased_array/layout/testbenches/simulations/vibrometer_spectrum.csv'
np.savetxt(outpath,
           np.column_stack([f_vib_axis, mag_vib, mag_ground]),
           header='freq_Hz,mine_displacement_um,ground_displacement_um',
           delimiter=',', comments='')
print(f"  Spectrum saved to: vibrometer_spectrum.csv")
