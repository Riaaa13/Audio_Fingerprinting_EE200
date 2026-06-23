import pickle

from single_peak_fingerprint import (
    generate_single_peaks
)

query_song = input(
    "Enter query path: "
)

query_peaks = generate_single_peaks(
    query_song
)

with open(
    "single_peak_database.pkl",
    "rb"
) as f:

    database = pickle.load(f)

best_song = None
best_score = 0

for song_name, song_peaks in database.items():

    score = 0

    peak_set = set(song_peaks)

    for peak in query_peaks:

        if peak in peak_set:
            score += 1

    print(
        song_name,
        score
    )

    if score > best_score:

        best_score = score
        best_song = song_name

print("\nMatched Song:")
print(best_song)

print("Score:")
print(best_score)
import csv
import os

csv_file = "single_peak_results.csv"

file_exists = os.path.isfile(csv_file)

with open(csv_file, "a", newline="") as f:

    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(
            [
                "Query File",
                "Matched Song",
                "Match Score"
            ]
        )

    writer.writerow(
        [
            query_song,
            best_song,
            best_score
        ]
    )

print("Result saved to single_peak_results.csv")