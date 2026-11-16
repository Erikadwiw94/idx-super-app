import streamlit as st

st.title("📊 Fundamental Analysis (Embedded)")
st.write("Aplikasi UI modern dari proyek `idx-fundamental-analysis`.")

# PENTING: Sesuaikan angka 5173 dengan port yang muncul di file ui.log
# Jika log menunjukkan 5174 atau 3000, ubah angka di bawah ini.
FUNDAMENTAL_URL = "http://localhost:5173"

st.iframe(FUNDAMENTAL_URL, height=1000)

st.sidebar.info("💡 **Tips:** Jika layar ini kosong, pastikan server UI (Bun/Vite) sudah menyala di terminal lain.")
