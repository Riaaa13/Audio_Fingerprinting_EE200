import pickle
from fingerprint import generate_fingerprints

query_song = input(
    "Enter query song path: "
)
print("Generating query fingerprints...")
query_fingerprints = generate_fingerprints(
    query_song
)
print("Loading database...")
with open(
    "song_database.pkl",
    "rb"
) as f:

    database = pickle.load(f)

best_song = None
best_score = 0
best_offsets = None
print("Data base loaded")

for song_name, song_fingerprints in database.items():

    print("Matching:", song_name)

    offsets = {}

    # Create fast lookup table
    song_lookup = {}

    for db_fp, db_time in song_fingerprints:

        if db_fp not in song_lookup:
            song_lookup[db_fp] = []

        song_lookup[db_fp].append(db_time)

    # Match query fingerprints
    for query_fp, query_time in query_fingerprints:

        if query_fp in song_lookup:

            for db_time in song_lookup[query_fp]:

                offset = db_time - query_time

                offsets[offset] = (
                    offsets.get(offset, 0) + 1
                )

    score = max(offsets.values()) if offsets else 0

    print(song_name, "Score =", score)

    if score > best_score:
        best_score = score
        best_song = song_name
        best_offsets = offsets.copy()

print("\nMatched Song:")
print(best_song)

print("Match Score:")
print(best_score)
import matplotlib.pyplot as plt


offset_list = []

for offset, count in best_offsets.items():

    offset_list.extend(
        [offset] * count
    )

plt.figure(figsize=(10,5))

plt.hist(
    offset_list,
    bins=100
)

plt.title("Offset Histogram")
plt.xlabel("Offset")
plt.ylabel("Matches")

plt.show()

import csv
import os

csv_file = "results.csv"

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

print("Result saved to results.csv")

