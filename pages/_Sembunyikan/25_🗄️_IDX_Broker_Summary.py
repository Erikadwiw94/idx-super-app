import streamlit as st
import os
import json
import pandas as pd
import glob
from datetime import datetime

st.set_page_config(page_title="IDX Broker Summary (Dataset)", page_icon="🗄️", layout="wide")

st.title("🗄️ IDX Broker Summary (Historical Dataset)")
st.write("Menampilkan data transaksi harian per broker dari proyek `idx-transaction-summary`.")

PROJECT_DIR = "/home/server/idx-transaction-summary"
BROKER_DIR = os.path.join(PROJECT_DIR, "broker")

def parse_val(val_str):
    if not val_str: return 0
    val_str = str(val_str).replace(",", "").strip()
    if val_str.endswith("M"):
        return float(val_str[:-1]) * 1_000_000
    elif val_str.endswith("B"):
        return float(val_str[:-1]) * 1_000_000_000
    elif val_str.endswith("T"):
        return float(val_str[:-1]) * 1_000_000_000_000
    try:
        return float(val_str)
    except:
        return 0

st.sidebar.header("🕹️ Filter Data")

sample_broker = "AF"
sample_files = glob.glob(os.path.join(BROKER_DIR, sample_broker, "*.json"))

# PERBAIKAN: Parse tanggal menjadi objek datetime agar sorting-nya benar
def parse_date_filename(filename):
    date_str = os.path.basename(filename).replace(".json", "")
    try:
        # Format file: 31_May_2022
        return datetime.strptime(date_str, "%d_%b_%Y")
    except:
        return datetime(1900, 1, 1)

# Urutkan berdasarkan tanggal asli (terbaru di atas)
available_files = sorted(sample_files, key=parse_date_filename, reverse=True)
available_dates = [os.path.basename(f).replace(".json", "") for f in available_files]

if not available_dates:
    st.error("Data tidak ditemukan.")
    st.stop()

# Tampilkan pilihan tanggal
selected_date = st.sidebar.selectbox("Pilih Tanggal Bursa:", available_dates)
ticker = st.sidebar.text_input("Kode Saham (misal: BBCA):", value="BBCA").upper()

broker_list = sorted(os.listdir(BROKER_DIR))
broker_list = [b for b in broker_list if os.path.isdir(os.path.join(BROKER_DIR, b))]
selected_broker = st.sidebar.selectbox("Pilih Broker:", ["ALL (Gabungan)"] + broker_list)

if st.sidebar.button("🔍 Tampilkan Data", type="primary"):
    with st.spinner(f"Membaca data untuk {ticker} pada {selected_date}..."):
        results = []
        if selected_broker == "ALL (Gabungan)":
            for broker in broker_list:
                file_path = os.path.join(BROKER_DIR, broker, f"{selected_date}.json")
                if os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        for item in data:
                            if item.get("Code") == ticker:
                                results.append(item)
        else:
            file_path = os.path.join(BROKER_DIR, selected_broker, f"{selected_date}.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
                    for item in data:
                        if item.get("Code") == ticker:
                            results.append(item)
                            
        if not results:
            st.warning(f"Tidak ada data untuk {ticker} pada {selected_date} di broker {selected_broker}.")
        else:
            df = pd.DataFrame(results)
            df['BVal_Num'] = df['BVal'].apply(parse_val)
            df['SVal_Num'] = df['SVal'].apply(parse_val)
            df['NVal_Num'] = df['NVal'].apply(parse_val)
            
            st.success(f"✅ Ditemukan {len(df)} transaksi untuk **{ticker}** pada **{selected_date}**")
            
            total_bval = df['BVal_Num'].sum()
            total_sval = df['SVal_Num'].sum()
            net_val = total_bval - total_sval
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Beli", f"Rp {total_bval:,.0f}")
            c2.metric("Total Jual", f"Rp {total_sval:,.0f}")
            c3.metric("Net Value", f"Rp {net_val:,.0f}", "🟢 Akumulasi" if net_val > 0 else "🔴 Distribusi")
            
            st.divider()
            st.subheader("📋 Rincian Transaksi Broker")
            
            display_cols = ['broker_code', 'Code', 'Name', 'BVol', 'BVal', 'BAvg', 'SVol', 'SVal', 'SAvg', 'NVol', 'NVal']
            display_cols = [c for c in display_cols if c in df.columns]
            
            st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
            
            csv = df[display_cols].to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Data (CSV)", csv, file_name=f"{ticker}_{selected_date}.csv", mime="text/csv")
