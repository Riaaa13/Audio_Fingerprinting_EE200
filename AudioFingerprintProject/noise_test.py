import librosa
import numpy as np
import soundfile as sf
import os

os.makedirs(
    "test_queries",
    exist_ok=True
)

audio, sr = librosa.load(
    "songs/Blackbird.mp3",
    sr=None
)

noise_levels = [
    0.01,
    0.05,
    0.10,
    0.20,
    0.30
]

for level in noise_levels:

    noise = np.random.normal(
        0,
        level,
        len(audio)
    )

    noisy_audio = audio + noise

    filename = (
        f"test_queries/noisy_{level}.wav"
    )

    sf.write(
        filename,
        noisy_audio,
        sr
    )

    print(
        "Created:",
        filename
    )