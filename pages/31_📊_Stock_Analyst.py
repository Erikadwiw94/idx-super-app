import streamlit as st

st.title("📊 Stock Market Analyst (Embedded)")
st.write("Aplikasi Streamlit dari proyek `Stock-Market-Analyst` yang berjalan di port 8503.")

ANALYST_URL = "http://localhost:8503"

st.iframe(ANALYST_URL, height=1000)

st.sidebar.info("💡 **Tips:** Jika layar ini kosong, pastikan server `Stock-Market-Analyst` sudah menyala di terminal lain (Port 8503).")
