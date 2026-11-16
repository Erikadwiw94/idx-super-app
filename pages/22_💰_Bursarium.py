import streamlit as st
import httpx
import pandas as pd

st.title("💰 Bursarium (Live IDX API)")
st.write("Data langsung dari `api.sarbeh.com` (Cloudflare Workers).")
st.divider()

API_BASE = "https://api.sarbeh.com"

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

# Form tengah
col1, col2, col3 = st.columns([2, 2, 3])
with col1: tahun = st.number_input("Tahun:", 2020, 2030, 2024)
with col2: bulan = st.number_input("Bulan:", 1, 12, 11)
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    aksi = st.radio("Aksi:", ["Indeks Pasar", "Top Gainer", "Top Loser", "Stock Screener"], horizontal=True)

st.divider()

params = {"year": tahun, "month": bulan}

if aksi == "Indeks Pasar":
    with st.spinner("Mengambil data indeks..."):
        data = fetch_api("/market/indices")
        df = extract_df(data)
        if df == "empty": st.warning("Data kosong.")
        elif df is not None and not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
        else: st.warning("Tidak ada data.")
elif aksi in ["Top Gainer", "Top Loser"]:
    ep = "/trading/top-gainer" if aksi == "Top Gainer" else "/trading/top-loser"
    with st.spinner(f"Mengambil {aksi}..."):
        data = fetch_api(ep, params=params)
        df = extract_df(data)
        if df == "empty": st.info(f"Tidak ada data {aksi} untuk {bulan}/{tahun}.")
        elif df is not None and not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
        else: st.warning("Tidak ada data.")
elif aksi == "Stock Screener":
    with st.spinner("Mengambil screener..."):
        data = fetch_api("/stock-screener")
        df = extract_df(data)
        if df == "empty": st.warning("Data screener kosong.")
        elif df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, "bursarium_screener.csv", "text/csv")
        else: st.warning("Tidak ada data.")
