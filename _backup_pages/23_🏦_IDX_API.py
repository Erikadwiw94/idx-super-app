import streamlit as st
import httpx
import pandas as pd

st.set_page_config(page_title="IDX API (Local)", page_icon="🏦", layout="wide")
st.title("🏦 IDX API (Local Server)")
st.write("Data dari server lokal `IDX-API` (Deno) di Port 52060.")
st.divider()

API_BASE = "http://localhost:52060"

def fetch_api(ep, params=None):
    try:
        with httpx.Client(timeout=30.0) as c:
            r = c.get(f"{API_BASE}{ep}", params=params)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"error": str(e)}

def extract_df(data):
    if isinstance(data, list): return pd.DataFrame(data)
    elif isinstance(data, dict):
        if "data" in data and isinstance(data["data"], list):
            return "empty" if len(data["data"]) == 0 else pd.DataFrame(data["data"])
        elif "error" in data: st.error(data["error"])
    return None

# Status server
try:
    with httpx.Client(timeout=3.0) as c: c.get(f"{API_BASE}/health")
    st.success("🟢 Server IDX-API Online")
except:
    st.error("🔴 Server IDX-API Offline — Jalankan: `cd /home/server/IDX-API && nohup deno task serve > idx_api.log 2>&1 &`")

# Form tengah
col1, col2, col3, col4 = st.columns([1.5, 1.5, 2, 3])
with col1: tahun = st.number_input("Tahun:", 2020, 2030, 2024)
with col2: bulan = st.number_input("Bulan:", 1, 12, 11)
with col3: aksi = st.selectbox("Aksi:", ["Top Gainer", "Top Loser", "Broker Summary", "Indeks", "Stock Screener"])
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🚀 Tampilkan", type="primary", use_container_width=True)

st.divider()

if mulai:
    params_tgl = {"year": tahun, "month": bulan}
    
    with st.spinner(f"Mengambil {aksi}..."):
        if aksi == "Top Gainer": data = fetch_api("/trading/top-gainer", params=params_tgl)
        elif aksi == "Top Loser": data = fetch_api("/trading/top-loser", params=params_tgl)
        elif aksi == "Broker Summary":
            date_str = f"{tahun}{bulan:02d}20"
            data = fetch_api("/trading/broker-summary", params={"date": date_str})
        elif aksi == "Indeks": data = fetch_api("/market/indices")
        else: data = fetch_api("/stock-screener", params=params_tgl)
        
        df = extract_df(data)
        if df == "empty": st.info(f"Tidak ada data untuk {bulan}/{tahun}.")
        elif df is not None and not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
        else: st.warning("Data tidak ditemukan atau server offline.")
