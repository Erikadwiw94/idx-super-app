import streamlit as st
import os, json, glob
import pandas as pd

st.title("🗄️ IDX Broker Summary (Dataset 2022)")
st.write("Data transaksi per broker dari proyek `idx-transaction-summary`.")
st.divider()

BROKER_DIR = "/home/server/idx-transaction-summary/broker"

def parse_val(v):
    if not v: return 0
    v = str(v).replace(",", "").strip()
    for suf, mult in [("T", 1e12), ("B", 1e9), ("M", 1e6)]:
        if v.endswith(suf): 
            try: return float(v[:-1]) * mult
            except: return 0
    try: return float(v)
    except: return 0

sample_files = glob.glob(os.path.join(BROKER_DIR, "AF", "*.json"))
dates = sorted([os.path.basename(f).replace(".json", "") for f in sample_files], reverse=True)

if not dates:
    st.error("Data broker tidak ditemukan."); st.stop()

brokers = sorted([b for b in os.listdir(BROKER_DIR) if os.path.isdir(os.path.join(BROKER_DIR, b))])

col1, col2, col3, col4 = st.columns([2, 2, 2.5, 1.5])
with col1: selected_date = st.selectbox("Tanggal:", dates)
with col2: ticker = st.text_input("Kode Saham:", value="BBCA").upper()
with col3: broker = st.selectbox("Broker:", ["ALL (Gabungan)"] + brokers)
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🔍 Tampilkan", type="primary", use_container_width=True)

st.divider()

if mulai:
    results = []
    if broker == "ALL (Gabungan)":
        for b in brokers:
            fp = os.path.join(BROKER_DIR, b, f"{selected_date}.json")
            if os.path.exists(fp):
                with open(fp) as f:
                    for item in json.load(f):
                        if item.get("Code") == ticker: results.append(item)
    else:
        fp = os.path.join(BROKER_DIR, broker, f"{selected_date}.json")
        if os.path.exists(fp):
            with open(fp) as f:
                for item in json.load(f):
                    if item.get("Code") == ticker: results.append(item)
    
    if not results:
        st.warning(f"Tidak ada data {ticker} pada {selected_date}.")
    else:
        df = pd.DataFrame(results)
        df['BVal_Num'] = df['BVal'].apply(parse_val)
        df['SVal_Num'] = df['SVal'].apply(parse_val)
        df['NVal_Num'] = df['NVal'].apply(parse_val)
        
        tb, ts = df['BVal_Num'].sum(), df['SVal_Num'].sum()
        st.success(f"✅ {len(df)} transaksi untuk **{ticker}** pada **{selected_date}**")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Beli", f"Rp {tb:,.0f}")
        c2.metric("Total Jual", f"Rp {ts:,.0f}")
        c3.metric("Net Value", f"Rp {tb-ts:,.0f}", "🟢 Akumulasi" if tb>ts else "🔴 Distribusi")
        
        st.divider()
        cols = ['broker_code','Code','Name','BVol','BVal','BAvg','SVol','SVal','SAvg','NVol','NVal']
        cols = [c for c in cols if c in df.columns]
        st.dataframe(df[cols], use_container_width=True, hide_index=True)
