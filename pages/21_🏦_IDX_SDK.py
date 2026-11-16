import streamlit as st
import subprocess
import json
import pandas as pd

st.title("🏦 IDX SDK (Direct from Bursa)")
st.write("Menarik data langsung dari API resmi IDX (menembus Cloudflare menggunakan `curl_cffi`).")

IDX_DIR = "/home/server/idx-indonesia-stock-exchange"
IDX_PYTHON = f"{IDX_DIR}/venv/bin/python"
SCRIPT_PATH = f"{IDX_DIR}/run_query.py"

def fetch_idx_data(method):
    try:
        result = subprocess.run(
            [IDX_PYTHON, SCRIPT_PATH, method],
            cwd=IDX_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.stdout:
            try:
                return json.loads(result.stdout)
            except:
                return {"error": "Gagal parse JSON", "raw": result.stdout}
        return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

# Fungsi untuk mengekstrak list dari dalam dict API IDX
def extract_dataframe(data):
    if isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict):
        if "data" in data and isinstance(data["data"], list):
            return pd.DataFrame(data["data"])
        elif "results" in data and isinstance(data["results"], list):
            return pd.DataFrame(data["results"])
    return None

tab1, tab2, tab3 = st.tabs(["🚀 Top Movers", "📊 Indeks", "🏢 Broker"])

# TAB 1: TOP MOVERS
with tab1:
    st.subheader("Pergerakan Saham Teratas")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🚀 Top Gainers", use_container_width=True, type="primary"):
            st.session_state['movers'] = fetch_idx_data("gainers")
    with col2:
        if st.button("📊 Top Volume", use_container_width=True, type="primary"):
            st.session_state['movers'] = fetch_idx_data("volume")
    with col3:
        if st.button("💰 Top Value", use_container_width=True, type="primary"):
            st.session_state['movers'] = fetch_idx_data("value")
    with col4:
        if st.button("⚡ Top Frequency", use_container_width=True, type="primary"):
            st.session_state['movers'] = fetch_idx_data("frequency")

    if 'movers' in st.session_state:
        df = extract_dataframe(st.session_state['movers'])
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("Data tidak ditemukan atau format tidak dikenali.")
            with st.expander("Lihat Raw Data"):
                st.json(st.session_state['movers'])

# TAB 2: INDEKS
with tab2:
    st.subheader("Daftar Indeks IDX")
    if st.button("📊 Tarik Daftar Indeks", type="primary"):
        with st.spinner("Mengambil data indeks..."):
            data = fetch_idx_data("index")
            df = extract_dataframe(data)
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.json(data)

# TAB 3: BROKER
with tab3:
    st.subheader("Direktori Broker (Anggota Bursa)")
    st.write("Daftar 89 sekuritas yang terdaftar di Bursa Efek Indonesia.")
    
    if st.button("🏢 Tarik Daftar Broker", type="primary"):
        with st.spinner("Mengambil data broker..."):
            data = fetch_idx_data("brokers")
            df = extract_dataframe(data)
            
            if df is not None and not df.empty:
                # Fitur Pencarian (Search)
                search = st.text_input("🔍 Cari Broker (Nama atau Kode):", "")
                if search:
                    df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
                
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.caption(f"Menampilkan {len(df)} broker.")
                
                # Tombol Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Data Broker (CSV)", csv, "idx_brokers.csv", "text/csv")
            else:
                st.json(data)
