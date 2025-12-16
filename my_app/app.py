import os
from pathlib import Path
import streamlit as st

st.write("CWD:", os.getcwd())
st.write("Exists my_app/assets:", (Path("assets").exists()))
st.write("Exists ../assets:", (Path("..") / "assets").exists())

st.switch_page("pages/0_Homepage.py")