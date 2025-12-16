from pathlib import Path
import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1] # .../my_app
logo_path = APP_DIR / "assets" / "laliga" / "laliga_logo.png"

st.set_page_config(
    page_title="La Liga Squad Efficiency",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .hero {
        border-radius: 22px;
        padding: 25px 28px;
        border: 1px solid rgba(255,255,255,0.12);
        background: radial-gradient(900px 380px at 20% 10%, rgba(60,70,255,0.35), rgba(0,0,0,0)),
                    radial-gradient(900px 380px at 90% 30%, rgba(225,6,0,0.35), rgba(0,0,0,0)),
                    linear-gradient(135deg, rgba(12,16,44,0.90), rgba(70,10,55,0.85), rgba(85,5,20,0.85));
        box-shadow: 0 20px 70px rgba(0,0,0,0.45);
      }
      .pill {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.88rem;
        font-weight: 700;
        margin-right: 8px;
        border: 1px solid rgba(255,255,255,0.18);
        background: rgba(255,255,255,0.06);
      }
      .hero-title {
        font-size: 2.6rem;
        font-weight: 900;
        margin: 12px 0 8px 0;
        line-height: 1.05;
      }
      .hero-sub {
        font-size: 1.05rem;
        opacity: 0.85;
        margin: 0 0 14px 0;
        max-width: 62ch;
      }
      .hero-tip {
        opacity: 0.78;
        font-size: 0.95rem;
        margin-top: 8px;
      }
      .section-title {
        font-size: 1.6rem;
        font-weight: 900;
        margin-top: 26px;
      }
      .card {
        border-radius: 18px;
        padding: 16px 18px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.03);
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Top row: LaLiga logo on the left, hero card on the right (same layout concept)
left, right = st.columns([1, 3], vertical_alignment="center")

with left:
    st.image(str(logo_path), width=300)

with right:
    st.markdown(
        """
        <div class="hero">
          <div>
            <span class="pill">Season 2025-26</span>
            <span class="pill">Matchday dashboard</span>
            <span class="pill">Transfermarkt-based</span>
          </div>
          <div class="hero-title">La Liga Squad Efficiency</div>
          <div class="hero-sub">
            Explore how market value, availability, age and loan strategy relate to team performance, one matchday at a time.
          </div>
          <div class="hero-tip">Tip: Use the sidebar to navigate pages</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown("## Dashboard overview")

# Intro text
st.markdown(
    """
    This dashboard explores **:red[squad efficiency in La Liga]** at the match level.

    Instead of focusing only on results, we look at:
    - Who was available
    - Who was actually used
    - The age and market value of deployed players
    - How clubs differ in squad depth and utilization

    Use the navigation on the left to:
    - Browse a full matchday
    - Dive into a specific match and compare both teams side by side
    """
)

if st.button("**:rainbow[START EXPLORING]**", use_container_width=True):
  st.switch_page("pages/1_Matchday_overview.py")

st.divider()

# Navigation hints
nav_left, nav_right = st.columns(2)

with nav_left:
    st.markdown("### 🏟️ :yellow[Matchday overview]")
    st.write(
        "Scan all matches of a selected matchday, see fixtures, dates "
        "and quickly jump into match analysis."
    )

with nav_right:
    st.markdown("### ⚽️ :yellow[Match analysis]")
    st.write(
        "Compare two teams in a single match using squad availability, "
        "age profiles and market value deployment."
    )

st.divider()

# Keep existing layout, refine card visuals
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="card"><b>Pick a matchday</b><br><br>Browse fixtures for the selected matchday and jump into match analysis.</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card"><b>Compare two teams</b><br><br>Side by side squad availability, age profile and market value deployment.</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card"><b>What is inside</b><br><br>Gold KPI tables only, no heavy computations inside the UI layer.</div>', unsafe_allow_html=True)

st.divider()

# Footer
st.caption(
    "Data source: Transfermarkt | "
    "Project: Squad efficiency in La Liga 2025–26 | "
    "HEC Lausanne - University of Lausanne"
)
