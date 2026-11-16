import streamlit as st
import httpx
import json
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Broker Summary Live", page_icon="📡", layout="wide")

st.title("📡 Broker Summary (Live Data)")
st.write("Data ditarik langsung dari server `jv-idx-mcp` secara *real-time*.")

MCP_SERVER_URL = "http://localhost:8000/mcp"

ticker = st.sidebar.text_input("Kode Saham (tanpa .JK)", value="BBCA").upper()

st.sidebar.markdown("---")
periode_opsi = st.sidebar.radio("Pilih Periode Analisis:", ["1 Hari", "1 Minggu", "1 Bulan", "1 Tahun"])

def get_last_trading_day(date_obj):
    while date_obj.weekday() >= 5:
        date_obj -= timedelta(days=1)
    return date_obj

end_date = get_last_trading_day(datetime.now())

if periode_opsi == "1 Hari":
    start_date = end_date
elif periode_opsi == "1 Minggu":
    start_date = end_date - timedelta(days=7)
elif periode_opsi == "1 Bulan":
    start_date = end_date - timedelta(days=30)
else:
    start_date = end_date - timedelta(days=365)

if datetime.now().weekday() >= 5:
    st.sidebar.warning("⚠️ Hari ini akhir pekan. Sistem otomatis menggunakan data hari bursa terakhir (Jumat).")

st.sidebar.info(f"Periode Aktif:\n{start_date.strftime('%Y-%m-%d')} s/d {end_date.strftime('%Y-%m-%d')}")

def parse_mcp_response(response):
    text = response.text.strip()
    if not text:
        return {"error": "Server mengembalikan respons kosong."}
    if "data:" in text:
        for line in reversed(text.split("\n")):
            if line.startswith("data:"):
                data_str = line[5:].strip()
                if data_str:
                    try: return json.loads(data_str)
                    except: pass
    try: return response.json()
    except: return {"error": f"Respons bukan JSON: {text[:200]}"}

if st.sidebar.button("Tarik Data Broker", type="primary"):
    with st.spinner(f"Menarik data {ticker} ({periode_opsi})..."):
        try:
            headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
            
            with httpx.Client(timeout=120.0, follow_redirects=True) as client:
                # 1. Inisialisasi Sesi Baru
                init_payload = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "st", "version": "1.0"}}}
                init_resp = client.post(MCP_SERVER_URL, json=init_payload, headers=headers)
                
                if init_resp.status_code != 200:
                    st.error(f"Gagal inisialisasi: {init_resp.text}")
                    st.stop()
                    
                session_id = init_resp.headers.get("mcp-session-id")
                if not session_id:
                    st.error("Server tidak memberikan Session ID.")
                    st.stop()
                
                # 2. Kirim Notifikasi
                headers["Mcp-Session-Id"] = session_id
                client.post(MCP_SERVER_URL, json={"jsonrpc": "2.0", "method": "notifications/initialized"}, headers=headers)
                
                # 3. Panggil Tool
                tool_payload = {
                    "jsonrpc": "2.0", "id": 2, "method": "tools/call",
                    "params": {
                        "name": "get_broker_summary", 
                        "arguments": {
                            "code": ticker, 
                            "start": start_date.strftime("%Y-%m-%d"), 
                            "end": end_date.strftime("%Y-%m-%d")
                        }
                    }
                }
                tool_resp = client.post(MCP_SERVER_URL, json=tool_payload, headers=headers)
                parsed = parse_mcp_response(tool_resp)
                
                if "error" in parsed:
                    st.error(f"❌ {parsed['error']}")
                    st.stop()
                    
                if "result" in parsed and "content" in parsed["result"]:
                    raw_text = parsed["result"]["content"][0]["text"]
                    
                    # PERBAIKAN: Tangkap error jika teks yang dikirim server bukan JSON
                    try:
                        data = json.loads(raw_text)
                    except json.JSONDecodeError:
                        st.warning("Server merespons, tetapi datanya tidak bisa dibaca (mungkin saham tidak aktif atau data tidak tersedia untuk periode ini).")
                        with st.expander("Lihat Pesan Asli dari Server"):
                            st.code(raw_text)
                        st.stop()
                    
                    st.success(f"✅ Data **{data.get('stock', ticker)}** berhasil ditarik! (Periode: {periode_opsi})")
                    
                    summary = data.get("summary", {})
                    st.markdown("### 📊 Ringkasan Pasar")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Total Nilai Transaksi", f"Rp {summary.get('total_value_raw') or '0'}")
                    c2.metric("Rata-rata Harga", f"Rp {summary.get('avg_price') or 0:,.0f}")
                    c3.metric("Total Lot", f"{summary.get('total_lot') or 0:,.0f}")
                    c4.metric("Net Asing", f"Rp {summary.get('foreign_net_value_raw') or '0'}")
                    
                    st.divider()
                    
                    col_buy, col_sell = st.columns(2)
                    with col_buy:
                        st.markdown("### 🟢 Top 10 Broker Akumulasi (Beli)")
                        df_buy = pd.DataFrame(data.get("buyers", []))
                        if not df_buy.empty:
                            df_buy = df_buy[['broker', 'type', 'value_raw', 'avg']]
                            df_buy.columns = ['Broker', 'Tipe', 'Nilai (Rp)', 'Harga Avg']
                            st.dataframe(df_buy, use_container_width=True, hide_index=True)
                        else:
                            st.info("Tidak ada data pembelian.")
                            
                    with col_sell:
                        st.markdown("### 🔴 Top 10 Broker Distribusi (Jual)")
                        df_sell = pd.DataFrame(data.get("sellers", []))
                        if not df_sell.empty:
                            df_sell = df_sell[['broker', 'type', 'value_raw', 'avg']]
                            df_sell.columns = ['Broker', 'Tipe', 'Nilai (Rp)', 'Harga Avg']
                            st.dataframe(df_sell, use_container_width=True, hide_index=True)
                        else:
                            st.info("Tidak ada data penjualan.")
                            
                    st.divider()
                    
                    st.markdown("### 🕵️ Pergerakan Net (Bandarmology)")
                    df_net = pd.DataFrame(data.get("net_positions", []))
                    if not df_net.empty and 'net_lot' in df_net.columns:
                        df_net_aktif = df_net[df_net['net_lot'] != 0].copy()
                        if not df_net_aktif.empty:
                            df_net_aktif = df_net_aktif[['broker', 'type', 'net_lot', 'buy_lot', 'sell_lot', 'buy_avg', 'sell_avg']]
                            df_net_aktif.columns = ['Broker', 'Tipe', 'Net Lot', 'Beli Lot', 'Jual Lot', 'Avg Beli', 'Avg Jual']
                            st.dataframe(df_net_aktif, use_container_width=True, hide_index=True)
                        else:
                            st.info("Tidak ada data Net Buy/Sell yang signifikan.")
                            
                else:
                    st.error("Format data dari server tidak dikenali.")
                    with st.expander("Lihat Raw Response"):
                        st.json(parsed)
                        
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")
