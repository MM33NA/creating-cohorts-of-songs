from pathlib import Path

# Project root = the folder above src/
ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "reports" / "figures"

RAW_CSV = RAW_DIR / "rolling_stones_spotify.csv"
CLEAN_CSV = PROCESSED_DIR / "cleaned.csv"

RANDOM_STATE = 42  # makes clustering/PCA results reproducible

# The 9 audio descriptors we cluster on (from the data dictionary).
# popularity, track_number and release date are NOT used to form clusters:
# popularity is something we want to *explain*, not build the groups from.
AUDIO_FEATURES = [
    "acousticness", "danceability", "energy", "instrumentalness",
    "liveness", "loudness", "speechiness", "tempo", "valence",
]
# Two rows with identical values on all of these are the same recording
# (e.g. one track on both the standard and the deluxe edition of an album).
DUPLICATE_KEY = AUDIO_FEATURES + ["duration_ms"]