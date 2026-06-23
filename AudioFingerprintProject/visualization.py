import librosa
import numpy as np

from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter


def get_visualization_data(song_path):

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

    return (
        S_peak,
        freq_idx,
        time_idx
    )