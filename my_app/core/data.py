from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import streamlit as st


DATA_DIRS = [
    Path("data/processed"),
    Path("data"),
]

CANDIDATES = {
    "matchday_overview_gold": ["matchday_overview_gold.parquet", "matchday_overview_gold.csv"],
    "club_match_kpis_gold": ["club_match_kpis_gold.parquet", "club_match_kpis_gold.csv"],
    "clubs_silver": ["clubs_silver.parquet", "clubs_silver.csv"],
}


def _find_dataset_file(dataset_key: str) -> Path:
    if dataset_key not in CANDIDATES:
        raise KeyError(f"Unknown dataset key: {dataset_key}")

    for d in DATA_DIRS:
        for fname in CANDIDATES[dataset_key]:
            p = d / fname
            if p.exists():
                return p

    searched = []
    for d in DATA_DIRS:
        for fname in CANDIDATES[dataset_key]:
            searched.append(str(d / fname))
    raise FileNotFoundError(f"Could not find {dataset_key}. Searched: {searched}")


@st.cache_data(show_spinner=False)
def load_df(dataset_key: str) -> pd.DataFrame:
    path = _find_dataset_file(dataset_key)
    if path.suffix.lower() == ".parquet":
        df = pd.read_parquet(path)
    elif path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    # Basic cleanup for stable UI behavior
    for col in ["match_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df
