import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Indeks Konstituen", page_icon="📋", layout="wide")

st.title("📋 Indeks Konstituen (IDX-Data)")
st.write("Daftar saham yang tergabung dalam Indeks IDX80, Kompas100, dan Universe (seluruh IDX).")

DATA_DIR = "/home/server/IDX-Data"

def baca_file(nama_file):
    path = os.path.join(DATA_DIR, nama_file)
    if os.path.exists(path):
        with open(path, "r") as f:
            saham = [line.strip() for line in f if line.strip()]
        return saham
    return []

tab1, tab2, tab3 = st.tabs(["📊 IDX80", "📈 Kompas100", "🌐 Universe (Semua)"])

# TAB 1: IDX80
with tab1:
    st.subheader("Konstituen IDX80 (80 Saham Paling Likuid)")
    saham = baca_file("IDX80")
    
    if saham:
        # Fitur pencarian
        search = st.text_input("🔍 Cari Saham di IDX80:", "", key="search_idx80")
        filtered = [s for s in saham if search.upper() in s] if search else saham
        
        # Tampilkan dalam bentuk tabel grid (5 kolom)
        df = pd.DataFrame(filtered, columns=["Kode Saham"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total: {len(saham)} saham.")
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download IDX80 (CSV)", csv, "idx80.csv", "text/csv")
    else:
        st.warning("File IDX80 tidak ditemukan.")

# TAB 2: KOMPAS100
with tab2:
    st.subheader("Konstituen Kompas100 (100 Saham)")
    saham = baca_file("Kompas100")
    
    if saham:
        search = st.text_input("🔍 Cari Saham di Kompas100:", "", key="search_kompas")
        filtered = [s for s in saham if search.upper() in s] if search else saham
        
        df = pd.DataFrame(filtered, columns=["Kode Saham"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total: {len(saham)} saham.")
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Kompas100 (CSV)", csv, "kompas100.csv", "text/csv")
    else:
        st.warning("File Kompas100 tidak ditemukan.")

# TAB 3: UNIVERSE (SEMUA SAHAM)
with tab3:
    st.subheader("Universe (Seluruh Saham di IDX)")
    saham = baca_file("Universe")
    
    if saham:
        search = st.text_input("🔍 Cari Saham di Universe:", "", key="search_universe")
        filtered = [s for s in saham if search.upper() in s] if search else saham
        
        df = pd.DataFrame(filtered, columns=["Kode Saham"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Total: {len(saham)} saham.")
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Universe (CSV)", csv, "universe.csv", "text/csv")
    else:
        st.warning("File Universe tidak ditemukan.")
