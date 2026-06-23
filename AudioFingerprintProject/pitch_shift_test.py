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

steps = [
    1,
    2,
    3
]

for step in steps:

    shifted_audio = librosa.effects.pitch_shift(
        y=audio,
        sr=sr,
        n_steps=step
    )

    filename = (
        f"test_queries/pitch_{step}.wav"
    )

    sf.write(
        filename,
        shifted_audio,
        sr
    )

    print(
        "Created:",
        filename
    )