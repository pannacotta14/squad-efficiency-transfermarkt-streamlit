from __future__ import annotations

import streamlit as st
import pandas as pd

from core.data import load_df
from core.ui import render_club_logo_by_id, section_header


st.set_page_config(
    page_title="Match Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .match-header-card {
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
        padding: 10px 10px;
        margin: 10px 0px 16px 0px;
      }
      .mh-team {
        font-weight: 800;
        font-size: 1.25rem;
        line-height: 1.1;
      }
      .mh-score {
        font-weight: 900;
        font-size: 2.1rem;
        text-align: center;
        letter-spacing: 0.5px;
      }
      .mh-meta {
        opacity: 0.72;
        text-align: center;
        margin-top: 6px;
        font-size: 0.95rem;
      }
      .mh-right { text-align: right; }
      .mh-left { text-align: left; }
      .mh-center { text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
      .score-chip {
        display: inline-block;
        padding: 5px 22px;
        border-radius: 10px;
        font-weight: 900;
        font-size: 2.0rem;
        letter-spacing: 1px;
        border: 1px solid rgba(255,255,255,0.16);
        background: linear-gradient(135deg, rgba(255,65,90,0.95), rgba(255,190,60,0.92));
        box-shadow: 0 5px 55px rgba(0,0,0,0.45);
      }
      .meta-line {
        opacity: 0.75;
        margin-top: 10px;
        font-size: 1.02rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Helpers
def normalize_match_id(x) -> str:
    if isinstance(x, list):
        x = x[0] if len(x) else ""
    if x is None:
        return ""
    s = str(x).strip()

    # Fix float-like ids such as "123.0"
    if s.endswith(".0"):
        s2 = s[:-2]
        if s2.isdigit():
            s = s2

    return s


def comparison_row(label, left_val, right_val, fmt="{:.2f}"):
    c1, c2, c3 = st.columns([3, 2, 2], vertical_alignment="center")

    with c1:
        st.write(label)

    with c2:
        if pd.notna(left_val):
            st.markdown(
                f"<span style='color:#43ce15ff; font-weight:700;'>"
                f"{fmt.format(left_val)}</span>",
                unsafe_allow_html=True,
            )
        else:
            st.write("-")

    with c3:
        if pd.notna(right_val):
            st.markdown(
                f"<span style='color:#ed4920ff; font-weight:700;'>"
                f"{fmt.format(right_val)}</span>",
                unsafe_allow_html=True,
            )
        else:
            st.write("-")


def dual_progress_bar(label, left_pct, right_pct, left_name, right_name):
    st.write(label)

    c1, c2 = st.columns(2)

    with c1:
        st.caption(left_name)
        st.progress(float(left_pct) if pd.notna(left_pct) else 0.0)
        if pd.notna(left_pct):
            st.caption(f"{left_pct:.1%}")

    with c2:
        st.caption(right_name)
        st.progress(float(right_pct) if pd.notna(right_pct) else 0.0)
        if pd.notna(right_pct):
            st.caption(f"{right_pct:.1%}")

def dual_ratio_bar(label: str, left_pct, right_pct, left_name: str, right_name: str):
    # left_pct and right_pct should be in [0, 1]
    def clamp01(x):
        try:
            x = float(x)
        except Exception:
            return 0.0
        if x != x:  # NaN
            return 0.0
        return max(0.0, min(1.0, x))

    l = clamp01(left_pct)
    r = clamp01(right_pct)

    # Widths as percentages of the full track
    lw = l * 100.0
    rw = r * 100.0

    # Display values
    ltxt = f"{l:.0%}"
    rtxt = f"{r:.0%}"

    st.markdown(
        f"""
        <div class="h2h-row">
          <div class="h2h-top">
            <div class="left">{ltxt}</div>
            <div class="h2h-label">{label}</div>
            <div class="right">{rtxt}</div>
          </div>

          <div class="h2h-track">
            <div class="h2h-left" style="width:{lw:.2f}%"></div>
            <div class="h2h-right" style="width:{rw:.2f}%"></div>
          </div>

          <div class="h2h-note">
            <div>{left_name}</div>
            <div class="right">{right_name}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Read match_id from query params
raw_match_id = st.session_state.get("selected_match_id")

if not raw_match_id:
    raw_match_id = st.query_params.get("match_id")

match_id = normalize_match_id(raw_match_id)

if not match_id:
    st.error("No match selected. Please go back to the Matchday page.")
    st.stop()

st.query_params["match_id"] = match_id


# Load data
matches = load_df("matchday_overview_gold").copy()
kpis = load_df("club_match_kpis_gold").copy()

# Normalize match_id everywhere
matches["match_id"] = matches["match_id"].apply(normalize_match_id)
kpis["match_id"] = kpis["match_id"].apply(normalize_match_id)


# Filter to selected match
match_row = matches[matches["match_id"] == match_id]
kpi_rows = kpis[kpis["match_id"] == match_id]

# Defensive checks
if match_row.empty:
    st.error("match_id not found in matchday_overview_gold: " + repr(match_id))
    st.stop()

if kpi_rows.empty:
    st.error("match_id not found in club_match_kpis_gold: " + repr(match_id))
    st.stop()

if "club_side" not in kpi_rows.columns:
    st.error("club_match_kpis_gold missing club_side column.")
    st.stop()

home_rows = kpi_rows[kpi_rows["club_side"] == "home"]
away_rows = kpi_rows[kpi_rows["club_side"] == "away"]

if home_rows.empty or away_rows.empty:
    st.error("Expected one home row and one away row for match_id = " + repr(match_id))
    st.stop()

# Use first row if duplicates exist
home = home_rows.iloc[0]
away = away_rows.iloc[0]
match = match_row.iloc[0]

home_name = str(home.get("club_name", match.get("home_club_name", "Home")))
away_name = str(away.get("club_name", match.get("away_club_name", "Away")))

home_id = match.get("home_club_id")
away_id = match.get("away_club_id")


# ------------------------------------------------
# Page sections
# ------------------------------------------------

# Header
if st.button("← Back to Matchday selection"):
    st.session_state["selected_match_id"] = None
    st.switch_page("pages/1_Matchday_overview.py")

st.title("Match Analysis")

# Prepare header values
home_id = match.get("home_club_id")
away_id = match.get("away_club_id")

score_str = str(match.get("result_string", "")).strip()
if not score_str or score_str.lower() == "nan":
    score_str = "-"

date_str = ""
if pd.notna(match.get("match_date")):
    date_str = pd.to_datetime(match["match_date"]).strftime("%d %b %Y")

time_str = str(match.get("kickoff_time", "")).strip()
if time_str.lower() == "nan":
    time_str = ""

meta_bits = [b for b in [date_str, time_str] if b]
meta_line = " , ".join(meta_bits)

st.markdown("<div class='match-header-card'>", unsafe_allow_html=True)

# Layout: [home logo] [home name] [score + meta] [away name] [away logo]
c1, c2, c3, c4, c5 = st.columns([1.2, 3.2, 2.4, 3.2, 1.2], vertical_alignment="center")

with c1:
    render_club_logo_by_id(home_id, width=100)

with c2:
    st.markdown(f"<div class='mh-team mh-right'>{home_name}</div>", unsafe_allow_html=True)

with c3:
    st.markdown(f"<div class='mh-center'><span class='score-chip'>{score_str}</span></div>", unsafe_allow_html=True)
    if meta_line:
        st.markdown(f"<div class='mh-center meta-line'>{meta_line}</div>", unsafe_allow_html=True)

with c4:
    st.markdown(f"<div class='mh-team mh-left'>{away_name}</div>", unsafe_allow_html=True)

with c5:
    render_club_logo_by_id(away_id, width=100)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# Section: Squad availability
section_header("Squad availability")

comparison_row(
    "Total squad players",
    home.get("players_total_squad"),
    away.get("players_total_squad"),
    fmt="{:.0f}",
)

comparison_row(
    "Players available",
    home.get("players_available"),
    away.get("players_available"),
    fmt="{:.0f}",
)

comparison_row(
    "Players used",
    home.get("players_used"),
    away.get("players_used"),
    fmt="{:.0f}",
)

comparison_row(
    "Usage rate",
    home.get("usage_rate"),
    away.get("usage_rate"),
    fmt="{:.1%}",
)

st.markdown("</div>", unsafe_allow_html=True)

# Section: Squad utilization ratios
st.divider()
section_header("Squad utilization ratios")


dual_progress_bar(
    "Share of squad available",
    home.get("pct_available"),
    away.get("pct_available"),
    home_name,
    away_name,
)

dual_progress_bar(
    "Share of squad in matchday squad",
    home.get("pct_matchday"),
    away.get("pct_matchday"),
    home_name,
    away_name,
)

dual_progress_bar(
    "Share of squad deployed",
    home.get("pct_deployed"),
    away.get("pct_deployed"),
    home_name,
    away_name,
)

st.caption(
    "Ratios are expressed as a share of the registered squad. "
    "Deployed players are those who played at least one minute."
)

# Section: Age profile
st.divider()
section_header("Age profile")

comparison_row(
    "Average age",
    home.get("avg_age_used"),
    away.get("avg_age_used"),
)

comparison_row(
    "Minutes weighted age",
    home.get("weighted_age_used"),
    away.get("weighted_age_used"),
)

# Section: Market value
st.divider()
section_header("Market value")

comparison_row(
    "Average market value",
    home.get("avg_market_value_used"),
    away.get("avg_market_value_used"),
)

comparison_row(
    "Minutes weighted market value",
    home.get("weighted_market_value_used"),
    away.get("weighted_market_value_used"),
)

comparison_row(
    "Deployed squad market value",
    home.get("deployed_squad_market_value"),
    away.get("deployed_squad_market_value"),
    fmt="{:,.0f}",
)
