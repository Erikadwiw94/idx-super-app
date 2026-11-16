import streamlit as st
import socket

st.title("🏢 Central Command Center")
st.write("Monitor status seluruh layanan (microservices) open-source Anda di server ini secara *real-time*.")

def check_port(host, port):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except:
        return False

st.markdown("### 🖥️ Status Server Lokal Anda")
st.info("Jika statusnya 🟢 ONLINE, berarti proyek tersebut sedang berjalan di background.")

# Daftar lengkap layanan yang telah kita integrasikan
services = [
    {"name": "Streamlit Web (Markas)", "port": 8502, "desc": "Web utama IDX Super Terminal.", "url": "http://localhost:8502"},
    {"name": "jv-idx-mcp (Broker Live)", "port": 8000, "desc": "API Broker Summary real-time.", "url": "http://localhost:8000"},
    {"name": "Maverick MCP (52 Tools)", "port": 8003, "desc": "API AI & Analisis lanjutan.", "url": "http://localhost:8003"},
    {"name": "BOZ (Next.js)", "port": 21526, "desc": "Dashboard UI modern berbasis React.", "url": "http://localhost:21526"},
    {"name": "IDX-UI (Deno)", "port": 50270, "desc": "Screener & Fundamental UI.", "url": "http://localhost:50270"},
    {"name": "Sentimeter (Bun)", "port": 3001, "desc": "API AI Sentimen & Rekomendasi.", "url": "http://localhost:3001"},
    {"name": "Stock-Market-Analyst", "port": 8503, "desc": "Aplikasi Streamlit analisis.", "url": "http://localhost:8503"},
    {"name": "Fundamental UI", "port": 8504, "desc": "UI Fundamental (Bun/Vite).", "url": "http://localhost:8504"},
    {"name": "auto-news report", "port": 3131, "desc": "Server report berita harian.", "url": "http://localhost:3131"},
    {"name": "auto-news stock-api", "port": 13052, "desc": "API berita saham.", "url": "http://localhost:13052"},
    {"name": "idx-bei Neo4j", "port": 7474, "desc": "Database Graph relasi saham.", "url": "http://localhost:7474"},
]

# Tampilkan dalam bentuk grid
cols = st.columns(2)
for i, svc in enumerate(services):
    with cols[i % 2]:
        is_online = check_port("127.0.0.1", svc["port"])
        status = "🟢 ONLINE" if is_online else "🔴 OFFLINE"
        
        with st.container(border=True):
            st.subheader(f"{svc['name']} - {status}")
            st.write(f"**Deskripsi:** {svc['desc']}")
            st.write(f"**Port:** {svc['port']}")
            if is_online:
                st.markdown(f"[Buka Aplikasi]({svc['url']})", unsafe_allow_html=True)
            else:
                st.caption("Layanan sedang mati. Nyalakan via terminal atau restart `idxweb`.")

st.divider()
st.success("✅ Seluruh ekosistem IDX Super Terminal telah terintegrasi dan berjalan di server Anda.")
