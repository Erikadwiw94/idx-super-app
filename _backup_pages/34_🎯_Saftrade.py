import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Saftrade Bot", page_icon="🎯", layout="wide")
st.title("🎯 Saftrade (AI Trading Bot)")
st.write("Engine dari proyek `Saftrade` — analisis teknikal + AI + notifikasi Telegram.")
st.divider()

SAFTRADE_DIR = "/home/server/Saftrade"
SAFTRADE_BIN = f"{SAFTRADE_DIR}/venv/bin/python"

col1, col2, col3 = st.columns([2, 2, 1.5])
with col1:
    st.info("💡 **Info:** Bot ini memindai watchlist `config/watchlist.py` dan menjalankan analisis AI untuk semua ticker di dalamnya.")
with col2:
    st.info("⚠️ **Catatan:** Agar notifikasi Telegram & AI (DeepSeek) berfungsi, isi API Key di `.env` folder Saftrade.")
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🚀 Jalankan Bot", type="primary", use_container_width=True)

st.divider()

if mulai:
    with st.spinner("Bot sedang menganalisis watchlist... (1-3 menit)"):
        try:
            r = subprocess.run([SAFTRADE_BIN, "main.py"], cwd=SAFTRADE_DIR, capture_output=True, text=True, timeout=300)
            st.success("✅ Eksekusi Selesai!")
            st.code(r.stdout if r.stdout else "(kosong)", language="text")
            if r.stderr: st.warning(f"STDERR: {r.stderr}")
            
            log_path = os.path.join(SAFTRADE_DIR, "app.log")
            if os.path.exists(log_path):
                with st.expander("📝 Log Terakhir (20 baris)"):
                    with open(log_path) as f:
                        st.code("".join(f.readlines()[-20:]))
        except subprocess.TimeoutExpired:
            st.error("❌ Timeout!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Tampilkan Watchlist
st.divider()
st.subheader("📋 Watchlist Saat Ini")
wl_path = os.path.join(SAFTRADE_DIR, "config", "watchlist.py")
if os.path.exists(wl_path):
    with open(wl_path) as f: st.code(f.read(), language="python")
