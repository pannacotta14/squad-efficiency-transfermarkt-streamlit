from __future__ import annotations
from pathlib import Path

import streamlit as st


def kpi_chip(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div style="
            display:inline-block;
            padding:6px 10px;
            border-radius:999px;
            border:1px solid rgba(255,255,255,0.12);
            background: rgba(255,255,255,0.04);
            margin-right:8px;
            margin-bottom:8px;
            font-size:0.9rem;">
            <span style="opacity:0.75;">{label}:</span>
            <span style="font-weight:700; margin-left:6px;">{value}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Club logo utilities
CLUB_LOGO_DIR = Path("assets/clubs")

def render_club_logo_by_id(club_id, width: int = 40):
    if club_id is None:
        st.write("")
        return

    cid = str(club_id).strip()

    # Fix float-like ids from parquet/csv, "123.0" -> "123"
    if cid.endswith(".0") and cid[:-2].isdigit():
        cid = cid[:-2]

    path = CLUB_LOGO_DIR / f"{cid}.png"
    if path.exists():
        st.image(str(path), width=width)
    else:
        st.write("")


def section_header(text: str):
    st.markdown(
        f"""
        <h3 style="
            border-left: 6px solid #FF4B44;
            padding-left: 12px;
            margin-top: 20px;
            margin-bottom: 12px;">
            {text}
        </h3>
        """,
        unsafe_allow_html=True,
    )
