import librosa
import numpy as np
from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter

def generate_fingerprints(song_path):

    audio, sr = librosa.load(song_path, sr=None)

    f, t, Sxx = spectrogram(
        audio,
        fs=sr,
        nperseg=1024,
        noverlap=512
    )

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

    fingerprints = []

    for i in range(len(time_idx)):

        for j in range(
            i + 1,
            min(i + 11, len(time_idx))
        ):

            dt = time_idx[j] - time_idx[i]

            fingerprints.append(
                (
                    (
                        int(freq_idx[i]),
                        int(freq_idx[j]),
                        int(dt)
                    ),
                    int(time_idx[i])
                )
            )

    return fingerprints