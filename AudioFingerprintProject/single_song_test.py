import librosa
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter

audio, sr = librosa.load(
    "songs/A Day In The Life.mp3",
    sr=None
)
audio = audio[:30*sr]

print("Sampling Rate =", sr)
print("Number of Samples =", len(audio))

plt.figure(figsize=(12,4))

plt.plot(audio)

plt.title("Audio Signal")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")

plt.savefig(
    "outputs/audiosignal.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()

## now answering first question 
## Converts:
##x[n] to x[k]



import numpy as np

N = len(audio)

fft_values = np.fft.fft(audio)

freq = np.fft.fftfreq(
    N,
    d=1/sr
)

## now plot
plt.figure(figsize=(12,5))

plt.plot(
    freq[:N//2],
    np.abs(
        fft_values[:N//2]
    )
)

plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.title("FFT of Entire Song")
plt.savefig(
    "outputs/fft.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()

## now we fix fft
f,t,Sxx = spectrogram(
    audio,
    fs=sr,
    nperseg=1024,
    noverlap=512
)
plt.figure(figsize=(12,6))

plt.pcolormesh(
    t,
    f,
    10*np.log10(Sxx + 1e-10)
)

plt.xlabel("Time")
plt.ylabel("Frequency")

plt.colorbar()

plt.title("Spectrogram")

plt.savefig(
    "outputs/spectrogram.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()

f_short,t_short,Sxx_short = spectrogram(
    audio,
    fs=sr,
    nperseg=256,
    noverlap=128
)
print("Spectrogram Shape =", Sxx.shape)
print("Min Value =", np.min(Sxx))
print("Max Value =", np.max(Sxx))

plt.figure(figsize=(12,6))

plt.pcolormesh(
    t_short,
    f_short,
    10*np.log10(Sxx_short+1e-10)
)

plt.title("Short Window Spectrogram")
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.colorbar()


plt.savefig(
    "outputs/short_window.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()

f_long,t_long,Sxx_long = spectrogram(
    audio,
    fs=sr,
    nperseg=4096,
    noverlap=2048
)

plt.figure(figsize=(12,6))

plt.pcolormesh(
    t_long,
    f_long,
    10*np.log10(Sxx_long+1e-10)
)

plt.title("Long Window Spectrogram")
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.colorbar()

plt.savefig(
    "outputs/long_window.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()
print("Short shape =", Sxx_short.shape)
print("Long shape =", Sxx_long.shape)
# =====================================
# NOISE EXPERIMENT
# =====================================

noise = np.random.normal(
    0,
    0.05,
    len(audio)
)

audio_noisy = audio + noise

f_noise, t_noise, Sxx_noise = spectrogram(
    audio_noisy,
    fs=sr,
    nperseg=1024,
    noverlap=512
)

plt.figure(figsize=(12,6))

plt.pcolormesh(
    t_noise,
    f_noise,
    10*np.log10(Sxx_noise + 1e-10)
)

plt.title("Spectrogram with Added Noise")
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.colorbar()

plt.savefig(
    "outputs/noisy_spectrogram.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()
# =====================================
# PITCH SHIFT EXPERIMENT
# =====================================

audio_pitch = librosa.effects.pitch_shift(
    y=audio,
    sr=sr,
    n_steps=2
)

f_pitch, t_pitch, Sxx_pitch = spectrogram(
    audio_pitch,
    fs=sr,
    nperseg=1024,
    noverlap=512
)

plt.figure(figsize=(12,6))

plt.pcolormesh(
    t_pitch,
    f_pitch,
    10*np.log10(Sxx_pitch + 1e-10)
)

plt.title("Pitch Shifted Spectrogram (+2 Semitones)")
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.colorbar()

plt.savefig(
    "outputs/pitch_shift.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()
# =====================================
# TIME STRETCH EXPERIMENT
# =====================================

audio_stretch = librosa.effects.time_stretch(
    y=audio,
    rate=1.1
)

f_stretch, t_stretch, Sxx_stretch = spectrogram(
    audio_stretch,
    fs=sr,
    nperseg=1024,
    noverlap=512
)

plt.figure(figsize=(12,6))

plt.pcolormesh(
    t_stretch,
    f_stretch,
    10*np.log10(Sxx_stretch + 1e-10)
)

plt.title("Time Stretched Spectrogram (1.1x)")
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.colorbar()

plt.savefig(
    "outputs/time_stretch.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()

##peak detection 

S_peak = np.log10(Sxx + 1e-10)
local_max = maximum_filter(
    S_peak,
    size=20
)

peaks = (S_peak == local_max)
threshold = np.percentile(
    S_peak,
    95
)

peaks = peaks & (S_peak > threshold)
freq_idx, time_idx = np.where(peaks)
indices = np.argsort(time_idx)

time_idx = time_idx[indices]
freq_idx = freq_idx[indices]
print("Number of Peaks =", len(freq_idx))
plt.figure(figsize=(12,6))

plt.scatter(
    time_idx,
    freq_idx,
    s=1 ## pehle it was 5
    
)
for i in range(
    min(
        200,
        len(time_idx)-1
    )
):

    plt.figure(figsize=(12,6))

plt.scatter(
    time_idx,
    freq_idx,
    s=1
)

plt.title("Constellation Map")
plt.xlabel("Time Bin")
plt.ylabel("Frequency Bin")

plt.savefig(
    "outputs/constellation_map.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()
plt.figure(figsize=(12,6))

plt.scatter(
    time_idx,
    freq_idx,
    s=1
)

for i in range(
    min(
        200,
        len(time_idx)-1
    )
):
    plt.plot(
        [time_idx[i], time_idx[i+1]],
        [freq_idx[i], freq_idx[i+1]],
        alpha=0.3
    )

plt.title("Paired Hash Relationships")
plt.xlabel("Time Bin")
plt.ylabel("Frequency Bin")

plt.savefig(
    "outputs/paired_hashes.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()

## proceeding with the fingerprints techniques 
fingerprints = []

for i in range(len(time_idx)):

    anchor_freq = freq_idx[i]
    anchor_time = time_idx[i]

    for j in range(
        i + 1,
        min(i + 11, len(time_idx))
    ):

        target_freq = freq_idx[j]
        target_time = time_idx[j]

        dt = target_time - anchor_time

        fingerprints.append(
            (
                anchor_freq,
                target_freq,
                dt
            )
        )
    # print("\nNumber of Fingerprints =", len(fingerprints))

    # print("\nFirst 20 Fingerprints")

    # for fp in fingerprints[:20]:
    #     print(fp)
        
hashes = []
for fp in fingerprints:
         hashes.append(fp)
        
    # print("\nNumber of Hashes =", len(hashes))

    # print("\nFirst 10 Hashes:\n")

    # for h in hashes[:10]:
    #     print(h)       
        
import pickle
with open(
    "outputs/song1_fingerprints.pkl",
    "wb"
    ) as f:
        pickle.dump(
        fingerprints,
        f
    )
with open(
    "outputs/song1_hashes.pkl",
    "wb"
    ) as f:
        pickle.dump(
        hashes,
        f
    )
            
print("Number of Peaks =", len(freq_idx))
print("Number of Fingerprints =", len(fingerprints))
print("Number of Hashes =", len(hashes))
print("PROGRAM FINISHED")