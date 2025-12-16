from __future__ import annotations

from pathlib import Path
import os
import pandas as pd
import streamlit as st

# Dataset filenames you accept for each key
CANDIDATES = {
    "matchday_overview_gold": ["matchday_overview_gold.parquet", "matchday_overview_gold.csv"],
    "club_match_kpis_gold": ["club_match_kpis_gold.parquet", "club_match_kpis_gold.csv"],
    "clubs_silver": ["clubs_silver.parquet", "clubs_silver.csv"],
}

def _repo_root() -> Path:
    # data.py is in: <repo>/my_app/core/data.py
    # parents[0] = core, parents[1] = my_app, parents[2] = repo
    return Path(__file__).resolve().parents[2]

def _data_dirs() -> list[Path]:
    root = _repo_root()

    # Optional override (useful on Cloud): set DATA_ROOT in Streamlit Secrets or env
    # Example: DATA_ROOT="my_app/data"
    override = os.getenv("DATA_ROOT", "").strip()
    if override:
        base = (root / override).resolve()
        return [base / "processed", base]

    # Default search locations (repo-root first, then inside my_app)
    return [
        root / "data" / "processed",
        root / "data",
        root / "my_app" / "data" / "processed",
        root / "my_app" / "data",
    ]

def _find_dataset_file(dataset_key: str) -> Path:
    if dataset_key not in CANDIDATES:
        raise KeyError(f"Unknown dataset key: {dataset_key}. Known: {list(CANDIDATES)}")

    searched: list[str] = []
    for d in _data_dirs():
        for fname in CANDIDATES[dataset_key]:
            p = d / fname
            searched.append(str(p))
            if p.exists():
                return p

    # Helpful debug: show what actually exists near the searched dirs
    nearby = []
    for d in _data_dirs():
        if d.exists():
            nearby += [str(x) for x in d.glob("*")][:30]

    raise FileNotFoundError(
        f"Could not find {dataset_key}. Searched: {searched}. "
        f"Existing files in those dirs (sample): {nearby}"
    )

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
    if "match_date" in df.columns:
        df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")

    return df
