import os
import pickle

from single_peak_fingerprint import (
    generate_single_peaks
)

database = {}

for file in os.listdir("songs"):

    if file.endswith(".mp3"):

        print("Processing:", file)

        peaks = generate_single_peaks(
            os.path.join(
                "songs",
                file
            )
        )

        database[file] = peaks

with open(
    "single_peak_database.pkl",
    "wb"
) as f:

    pickle.dump(
        database,
        f
    )

print("DONE")