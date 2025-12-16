from __future__ import annotations

import streamlit as st
import pandas as pd

from core.data import load_df
from core.ui import kpi_chip, render_club_logo_by_id


st.set_page_config(
    page_title="Matchday, La Liga Squad Efficiency",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Matchday Overview")

# Helper functions
def normalize_match_id(x) -> str:
    if x is None:
        return ""
    s = str(x).strip()
    if s.endswith(".0") and s[:-2].isdigit():
        s = s[:-2]
    return s


def safe_str(x) -> str:
    if x is None:
        return ""
    s = str(x).strip()
    if s.lower() == "nan":
        return ""
    return s


# -----------------------------
# CSS for match cards
# -----------------------------
st.markdown(
    """
    <style>
      .match-card {
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
        padding: 14px 14px;
        margin: 10px 0px;
      }
      .muted {
        opacity: 0.72;
        font-size: 0.92rem;
      }
      .score {
        font-weight: 800;
        font-size: 1.25rem;
        text-align: center;
        letter-spacing: 0.5px;
      }
      .team-name {
        font-weight: 700;
        font-size: 1.05rem;
        line-height: 1.1;
      }
      .right {
        text-align: right;
      }
      .center {
        text-align: center;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Load data
# -----------------------------
df = load_df("matchday_overview_gold").copy()

required_cols = ["match_id", "matchday", "home_club_name", "away_club_name"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error("matchday_overview_gold is missing required columns: " + ", ".join(missing))
    st.stop()

# Optional but recommended for logos on this page
logo_cols_needed = ["home_club_id", "away_club_id"]
has_logo_cols = all(c in df.columns for c in logo_cols_needed)

# Defensive normalize match_id for navigation keys
df["match_id"] = df["match_id"].apply(normalize_match_id)

# Sidebar filters
with st.sidebar:
    st.header("Filters")

    if "season" in df.columns:
        seasons = sorted([s for s in df["season"].dropna().unique().tolist()])
        season = st.selectbox("Season", seasons, index=len(seasons) - 1 if seasons else 0)
        df = df[df["season"] == season]
    else:
        season = None

    if "competition" in df.columns:
        comps = sorted([c for c in df["competition"].dropna().unique().tolist()])
        competition = st.selectbox("Competition", ["All"] + comps, index=0)
        if competition != "All":
            df = df[df["competition"] == competition]
    else:
        competition = None

    matchdays = sorted([int(x) for x in df["matchday"].dropna().unique().tolist()])
    if not matchdays:
        st.warning("No matchdays found after filters.")
        st.stop()

    default_md = matchdays[-1]
    matchday = st.selectbox("Matchday", matchdays, index=matchdays.index(default_md))

# Filter matchday
md = df[df["matchday"] == matchday].copy()

# Sort by date/time when available
sort_cols = []
if "match_date" in md.columns:
    sort_cols.append("match_date")
if "kickoff_time" in md.columns:
    sort_cols.append("kickoff_time")
if sort_cols:
    md = md.sort_values(sort_cols)

# Header summary
left, right = st.columns([3, 2], vertical_alignment="center")
with left:
    title_bits = []
    if season is not None:
        title_bits.append(str(season))
    title_bits.append(f"Matchday {matchday}")
    if competition not in (None, "All"):
        title_bits.append(str(competition))
    st.subheader(" , ".join(title_bits))

with right:
    kpi_chip("Matches", str(len(md)))
    if "match_date" in md.columns:
        dmin = md["match_date"].min()
        dmax = md["match_date"].max()
        if pd.notna(dmin) and pd.notna(dmax):
            if dmin.date() == dmax.date():
                kpi_chip("Date", pd.to_datetime(dmin).strftime("%Y-%m-%d"))
            else:
                kpi_chip("Dates", f"{pd.to_datetime(dmin):%Y-%m-%d} to {pd.to_datetime(dmax):%Y-%m-%d}")

# If logo ids are missing, warn once (still renders)
if not has_logo_cols:
    st.info("Tip: Add home_club_id and away_club_id to matchday_overview_gold to display team logos on this page.")

st.divider()

# -----------------------------
# Match cards
# -----------------------------
for _, r in md.iterrows():
    match_id = normalize_match_id(r.get("match_id"))

    home_name = safe_str(r.get("home_club_name", "Home"))
    away_name = safe_str(r.get("away_club_name", "Away"))

    home_id = r.get("home_club_id") if has_logo_cols else None
    away_id = r.get("away_club_id") if has_logo_cols else None

    date_str = ""
    if "match_date" in md.columns and pd.notna(r.get("match_date")):
        date_str = pd.to_datetime(r["match_date"]).strftime("%a %Y-%m-%d")
    time_str = safe_str(r.get("kickoff_time", ""))

    score = safe_str(r.get("result_string", ""))
    if not score:
        score = "-"

    st.markdown("<div class='match-card'>", unsafe_allow_html=True)

    # Layout: [date/time] [home logo] [home name] [score] [away name] [away logo] [button]
    c0, c1, c2, c3, c4, c5, c6 = st.columns([1.4, 0.6, 2.6, 1.0, 2.6, 0.6, 1.2], vertical_alignment="center")

    with c0:
        if date_str:
            st.markdown(f"<div class='muted'>{date_str}</div>", unsafe_allow_html=True)
        if time_str:
            st.markdown(f"<div class='muted'>{time_str}</div>", unsafe_allow_html=True)

    with c1:
        render_club_logo_by_id(home_id, width=60)

    with c2:
        st.markdown(f"<div class='team-name right'>{home_name}</div>", unsafe_allow_html=True)

    with c3:
        st.markdown(f"<div class='score'>{score}</div>", unsafe_allow_html=True)

    with c4:
        st.markdown(f"<div class='team-name'>{away_name}</div>", unsafe_allow_html=True)

    with c5:
        render_club_logo_by_id(away_id, width=60)

    with c6:
        if st.button("View", key=f"view_{match_id}", use_container_width=True):
            st.session_state["selected_match_id"] = match_id
            st.switch_page("pages/2_Match_analysis.py")

    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
if st.button("**:orange[Return to Homepage]**", use_container_width=True):
  st.switch_page("pages/0_Homepage.py")