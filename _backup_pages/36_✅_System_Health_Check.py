import streamlit as st
import os, ast, re, subprocess, socket
import pandas as pd

st.set_page_config(page_title="System Health", page_icon="✅", layout="wide")
st.title("✅ System Health Check")
st.write("Uji semua halaman web dan dependensinya secara otomatis.")
st.divider()

PAGES_DIR = "/home/server/web-gabungan/pages"
SERVER_DIR = "/home/server"

def check_syntax(fp):
    try:
        with open(fp) as f: ast.parse(f.read())
        return True, ""
    except SyntaxError as e: return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e: return False, str(e)

def check_port(port):
    try:
        with socket.create_connection(("127.0.0.1", int(port)), timeout=1): return True
    except: return False

def check_folder(f):
    return os.path.isdir(os.path.join(SERVER_DIR, f))

def check_file(f):
    return os.path.exists(os.path.join(SERVER_DIR, "web-gabungan", f))

EXTERNAL = {
    "11_🤖_Sentimeter": [("port", "3001")],
    "16_🚀_BOZ_NextJS": [("port", "21526")],
    "17_💎_IDX_UI": [("port", "50270")],
    "18_📊_Fundamental_UI": [("port", "8504")],
    "19_📊_Stock_Analyst": [("port", "8503")],
    "30_🏦_IDX_API": [("port", "52060")],
    "09_⚙️_Backtest_Wyckoff": ["idx-quant-research-platform"],
    "12_🧠_StockAI": ["stockai"],
    "13_🤖_AI_Saham": ["ai-saham"],
    "23_📥_Bulk_Download": ["Bulk-Download-Table-From-IDX"],
    "24_🎯_Saftrade": ["Saftrade"],
    "25_Idx_Broker_Summary": ["idx-transaction-summary"],
    "26_🚀_Pulse_CLI": ["Pulse-CLI"],
    "28_🏦_IDX_SDK": ["idx-indonesia-stock-exchange"],
    "31_📋_Indeks_Konstituen": ["IDX-Data"],
    "32_📑_IDXLens": ["idxlens"],
    "33_Stock_MCP_Pro": ["stock_mcp"],
}

# === TOMBOL AKSI DI TENGAH ===
st.markdown("### 🔧 Aksi Cepat")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔄 Refresh Health Check", use_container_width=True):
        st.rerun()
with c2:
    if st.button("🐳 Nyalakan Semua Docker", use_container_width=True):
        with st.spinner("Menyalakan Docker..."):
            for ct in ["jv-idx-mcp","maverick-mcp-backend-1","maverick-mcp-postgres-1","maverick-mcp-redis-1","idx-stock-api","idx-report-server"]:
                subprocess.run(["docker","start",ct], capture_output=True)
            st.success("✅ Docker dinyalakan!")
            st.rerun()
with c3:
    if st.button("🔁 Restart Web", use_container_width=True):
        subprocess.Popen(["systemctl","restart","idxweb"])
        st.success("✅ Web direstart. Refresh dalam 5 detik.")

st.divider()

# Scan halaman
page_files = sorted([f for f in os.listdir(PAGES_DIR) if f.endswith(".py")])
st.markdown(f"### 📊 Scanning {len(page_files)} halaman...")

results = []
for pf in page_files:
    fp = os.path.join(PAGES_DIR, pf)
    name = pf.replace(".py", "")
    ok, err = check_syntax(fp)
    
    if not ok:
        results.append({"Halaman": name, "Syntax": "❌", "Dependensi": err, "Status": "❌ FAILED"})
        continue
    
    missing = []
    for dep in EXTERNAL.get(name, []):
        if isinstance(dep, tuple) and dep[0] == "port":
            if not check_port(dep[1]): missing.append(f"Port {dep[1]} offline")
        elif isinstance(dep, str):
            if not check_folder(dep): missing.append(f"Folder {dep}/ tidak ada")
    
    status = "⚠️ Butuh Setup" if missing else "✅ OK"
    dep_txt = "; ".join(missing[:2]) + (f" (+{len(missing)-2})" if len(missing) > 2 else "") if missing else "OK"
    results.append({"Halaman": name, "Syntax": "✅", "Dependensi": dep_txt, "Status": status})

total = len(results)
ok_n = sum(1 for r in results if r["Status"] == "✅ OK")
warn_n = sum(1 for r in results if r["Status"] == "⚠️ Butuh Setup")
fail_n = sum(1 for r in results if r["Status"] == "❌ FAILED")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total", total); c2.metric("✅ OK", ok_n); c3.metric("⚠️ Setup", warn_n); c4.metric("❌ Failed", fail_n)
st.divider()

filter_st = st.radio("Filter:", ["Semua", "✅ OK", "⚠️ Butuh Setup", "❌ FAILED"], horizontal=True)
if filter_st != "Semua":
    results = [r for r in results if r["Status"] == filter_st]

st.markdown(f"### 📋 Hasil ({len(results)} halaman)")
if results: st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
else: st.info("Tidak ada halaman dengan status tersebut.")

with st.expander("🐳 Status Docker Containers"):
    try:
        out = subprocess.run(["docker","ps","--format","{{.Names}}\t{{.Status}}"], capture_output=True, text=True, timeout=5).stdout.strip()
        if out: st.code(out, language="text")
        else: st.warning("Tidak ada container aktif.")
    except Exception as e: st.error(f"Error: {e}")
