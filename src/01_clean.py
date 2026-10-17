"""Step 1 - clean the raw data and save data/processed/cleaned.csv

Run from the project root:   python src/01_clean.py
Every rule below was decided after exploring the data in the notebook.
"""
import pandas as pd
from config import RAW_CSV, CLEAN_CSV, PROCESSED_DIR, DUPLICATE_KEY, AUDIO_FEATURES


def clean(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    print(f"Raw rows: {len(df)}")

    # Rule 1: 'Unnamed: 0' is just the old row index saved by mistake.
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")

    # Rule 2: dates should be real dates, not text.
    df["release_date"] = pd.to_datetime(df["release_date"])

    # Rule 3: sanity checks - fail loudly if the data is not what we expect.
    assert df.isna().sum().sum() == 0, "unexpected missing values"
    assert df["id"].is_unique, "duplicate Spotify IDs"
    zero_to_one = ["acousticness", "danceability", "energy", "instrumentalness",
                   "liveness", "speechiness", "valence"]
    assert df[zero_to_one].min().min() >= 0 and df[zero_to_one].max().max() <= 1

    # Rule 4: the same recording often sits on several editions of an album
    # (standard / deluxe / remaster) with a different Spotify ID each time.
    # Keeping all copies would count that song twice when clustering, so we keep
    # one copy - the one with the highest popularity.
    before = len(df)
    df = (df.sort_values("popularity", ascending=False)
            .drop_duplicates(subset=DUPLICATE_KEY, keep="first")
            .sort_index())
    print(f"Removed {before - len(df)} duplicate recordings -> {len(df)} rows")

    # Kept on purpose (documented in the notebook):
    #  - repeated song NAMES (different recordings: live, remaster, ...)
    #  - very long live tracks and very short intros (real, just unusual)
    #  - popularity = 0 (a valid score for 17 obscure tracks, not missing data)
    return df.reset_index(drop=True)


if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    cleaned = clean(pd.read_csv(RAW_CSV))
    cleaned.to_csv(CLEAN_CSV, index=False)
    print(f"Saved {CLEAN_CSV}")