import os
import pickle

from fingerprint import generate_fingerprints

database = {}

songs_folder = "songs"

for file in os.listdir(songs_folder):

    if file.endswith(".mp3"):

        song_path = os.path.join(
            songs_folder,
            file
        )

        print("Processing:", file)

        fingerprints = generate_fingerprints(
            song_path
        )

        database[file] = fingerprints

        print(
            "Fingerprints:",
            len(fingerprints)
        )

with open(
    "song_database.pkl",
    "wb"
) as f:

    pickle.dump(
        database,
        f
    )

print("DATABASE CREATED")