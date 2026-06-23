import librosa
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

rates = [
    0.95,
    1.05,
    1.10
]

for rate in rates:

    stretched_audio = librosa.effects.time_stretch(
        y=audio,
        rate=rate
    )

    filename = (
        f"test_queries/stretch_{rate}.wav"
    )

    sf.write(
        filename,
        stretched_audio,
        sr
    )

    print(
        "Created:",
        filename
    )