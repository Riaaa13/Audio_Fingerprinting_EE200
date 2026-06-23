
print("MATCHER VERSION WITH OFFSETS LOADED")
import pickle
from collections import Counter
import os
from pathlib import Path

print("Current Working Directory:", os.getcwd())
print("Matcher File Location:", Path(__file__).resolve())
print("Files in current directory:", os.listdir())

from single_peak_fingerprint import (
    generate_single_peaks
)


def identify_song(query_song):

    query_peaks = generate_single_peaks(
        query_song
    )

    from pathlib import Path
    db_path = Path(__file__).parent / "single_peak_database.pkl"
    with open(db_path, "rb") as f:

        database = pickle.load(f)

    best_song = None
    best_score = 0
    best_offsets = []

    candidate_scores = []

    for song_name, song_peaks in database.items():

        offsets = []

        song_by_freq = {}

        for freq, t in song_peaks:

            if freq not in song_by_freq:
                song_by_freq[freq] = []

            song_by_freq[freq].append(t)

        for freq_q, time_q in query_peaks:

            if freq_q in song_by_freq:

                for time_db in song_by_freq[freq_q]:

                    offsets.append(
                        time_db - time_q
                    )

        if len(offsets) == 0:
            continue

        counter = Counter(offsets)

        score = max(
            counter.values()
        )

        candidate_scores.append(
            (
                song_name,
                score
            )
        )

        if score > best_score:

            best_score = score
            best_song = song_name
            best_offsets = offsets

    candidate_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return (
        best_song,
        best_score,
        best_offsets,
        candidate_scores[:5]
    )