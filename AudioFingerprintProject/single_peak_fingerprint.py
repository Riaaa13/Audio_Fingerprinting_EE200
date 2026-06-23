import librosa
import numpy as np

from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter

def generate_single_peaks(song_path):

    audio, sr = librosa.load(
        song_path,
        sr=None
    )

    f, t, Sxx = spectrogram(
        audio,
        fs=sr,
        nperseg=1024,
        noverlap=512
    )

    S_peak = np.log10(
        Sxx + 1e-10
    )

    local_max = maximum_filter(
        S_peak,
        size=20
    )

    peaks = (S_peak == local_max)

    threshold = np.percentile(
        S_peak,
        95
    )

    peaks = peaks & (
        S_peak > threshold
    )

    freq_idx, time_idx = np.where(
        peaks
    )

    single_peaks = []

    for i in range(
        len(freq_idx)
    ):

        single_peaks.append(
            (
                int(freq_idx[i]),
                int(time_idx[i])
            )
        )

    return single_peaks