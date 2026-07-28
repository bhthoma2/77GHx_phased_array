import numpy as np

data = np.loadtxt('/home/bthomas3/Videos/77GHz_phased_array/layout/testbenches/simulations/fmcw_adc_output.dat')
t = data[:, 0]
v = data[:, 1]

# Use only 2nd chirp period (1ms to 2ms) for clean FFT
mask = (t >= 1e-3) & (t <= 2e-3)
t2 = t[mask]
v2 = v[mask]

# Resample to uniform grid (required for FFT)
N = 8192
t_uniform = np.linspace(t2[0], t2[-1], N)
v_uniform = np.interp(t_uniform, t2, v2)

# Remove DC
v_uniform = v_uniform - np.mean(v_uniform)

# Window + FFT
window = np.hanning(N)
v_win = v_uniform * window
fft_out = np.fft.rfft(v_win)
dt = (t_uniform[-1] - t_uniform[0]) / (N - 1)
freqs = np.fft.rfftfreq(N, dt)

# Power spectrum in dB
mag = np.abs(fft_out) / (N/2)
mag_db = 20 * np.log10(mag + 1e-15)

# Find peaks
peak_indices = []
for i in range(2, len(mag_db)-2):
    if mag_db[i] > mag_db[i-1] and mag_db[i] > mag_db[i+1] and mag_db[i] > -60:
        peak_indices.append(i)

# Sort by magnitude
peak_indices.sort(key=lambda i: -mag_db[i])

print("=" * 65)
print("  FMCW RADAR FFT — RANGE SPECTRUM")
print("=" * 65)
print(f"  FFT points: {N}, Frequency resolution: {freqs[1]:.1f} Hz")
print(f"  Time window: {t2[0]*1e3:.2f} ms to {t2[-1]*1e3:.2f} ms")
print(f"  Sample rate (resampled): {1/dt/1e6:.2f} MHz")
print()
print(f"  {'Peak#':<6} {'Freq (kHz)':<12} {'Range (m)':<10} {'Power (dB)':<12} {'Target'}")
print(f"  {'-'*6} {'-'*12} {'-'*10} {'-'*12} {'-'*10}")

c = 3e8
BW = 4e9
Tchirp = 1e-3

for idx, pi in enumerate(peak_indices[:5]):
    f = freqs[pi]
    r = f * c * Tchirp / (2 * BW)
    label = ""
    if abs(f - 80000) < 2000:
        label = "Ground (3m)"
    elif abs(f - 186667) < 5000:
        label = "Landmine (7m)"
    print(f"  {idx+1:<6} {f/1e3:<12.2f} {r:<10.3f} {mag_db[pi]:<12.1f} {label}")

print()
print("  Range resolution: dr = c/(2*BW) = 3.75 cm")
print("  Freq-to-range:    R = f_beat * c * T / (2*BW)")
print("=" * 65)

# Also save spectrum to CSV
outpath = '/home/bthomas3/Videos/77GHz_phased_array/layout/testbenches/simulations/fmcw_fft_spectrum.csv'
np.savetxt(outpath, np.column_stack([freqs/1e3, mag_db]),
           header='freq_kHz,power_dB', delimiter=',', comments='')
print(f"\n  Spectrum saved to: fmcw_fft_spectrum.csv")
