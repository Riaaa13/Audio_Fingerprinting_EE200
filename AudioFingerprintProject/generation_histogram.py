from matcher import identify_song
import matplotlib.pyplot as plt

song, score, offsets, candidates = identify_song(
    "songs/A Day In The Life.mp3"
)

plt.figure(figsize=(10,5))

plt.hist(
    offsets,
    bins=150
)

plt.title(
    f"Offset Histogram - {song}"
)

plt.xlabel("Offset")
plt.ylabel("Count")

plt.savefig(
    "outputs/offset_histogram.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()