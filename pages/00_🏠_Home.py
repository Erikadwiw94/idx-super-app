import streamlit as st

# CSS
st.markdown("""
<style>
    .hero { 
        background: linear-gradient(135deg, #00c853 0%, #009624 100%);
        padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem;
        text-align: center; color: white;
    }
    .hero h1 { font-size: 3rem; margin: 0; font-weight: 800; }
    .hero p { font-size: 1.1rem; margin-top: 0.5rem; opacity: 0.9; }
    .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
    .metric-box { 
        background: #1e2130; padding: 1.5rem; border-radius: 12px;
        text-align: center; border: 1px solid #2a2f3f;
    }
    .metric-box .value { font-size: 2.5rem; font-weight: 800; color: #00c853; }
    .metric-box .label { font-size: 0.9rem; color: #8b92a8; text-transform: uppercase; letter-spacing: 1px; }
    .category-header {
        font-size: 1.5rem; font-weight: 700; color: #00c853;
        margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #00c853;
    }
    .page-card {
        background: #1e2130; padding: 1rem 1.2rem; border-radius: 10px;
        border-left: 4px solid #00c853; margin-bottom: 0.75rem;
    }
    .page-card .title { font-weight: 600; color: #fafafa; }
    .page-card .desc { font-size: 0.85rem; color: #8b92a8; margin-top: 0.2rem; }
    .footer { text-align: center; color: #8b92a8; padding: 2rem 0 1rem 0; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>⚡ IDX SUPER TERMINAL</h1>
    <p>Platform Analisis Saham Indonesia Terpadu</p>
    <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.8;">
        36 Halaman • 6 Aplikasi Embed • 5 Backend Service • 40+ Open Source Projects
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="metric-grid">
    <div class="metric-box">
        <div class="value">963</div>
        <div class="label">Saham IDX</div>
    </div>
    <div class="metric-box">
        <div class="value">36</div>
        <div class="label">Halaman Web</div>
    </div>
    <div class="metric-box">
        <div class="value">6</div>
        <div class="label">Aplikasi Embed</div>
    </div>
    <div class="metric-box">
        <div class="value">113</div>
        <div class="label">Indikator</div>
    </div>
</div>
""", unsafe_allow_html=True)

categories = [
    {
        "name": "📊 Analisis Saham",
        "desc": "Screener, teknikal, fundamental, dan analisis multi-saham",
        "pages": [
            ("01_📊_Screener.py", "📊 Screener", "Scan 900+ saham dengan RSI & MA"),
            ("02_⚡_Ultimate_Analyzer.py", "⚡ Ultimate Analyzer", "Skor AI komprehensif"),
            ("03_📉_Pro_Technical.py", "📉 Pro Technical", "Candlestick + 14 indikator"),
            ("04_🔢_Dashboard_Angka.py", "🔢 Dashboard Angka", "113 indikator dalam tabel"),
            ("05_📈_Multi_Stock.py", "📈 Multi Stock", "Komparasi multi-saham + korelasi"),
        ],
    },
    {
        "name": "🕵️ Bandarmology",
        "desc": "Pelacak aliran dana bandar & broker besar",
        "pages": [
            ("06_🕵️_Bandar_OBV.py", "🕵️ Bandar OBV", "Deteksi akumulasi via OBV"),
            ("07_🕵️_Bandar_Simulasi.py", "🕵️ Bandar Simulasi", "Simulasi data broker"),
            ("08_🕵️_Bandar_Accumulation.py", "🕵️ Bandar Accumulation", "Bandar Score 958 saham"),
            ("09_💰_Broker_Summary.py", "💰 Broker Summary", "Broker summary dataset"),
        ],
    },
    {
        "name": "⚙️ Backtest",
        "desc": "Uji strategi trading dengan data historis",
        "pages": [
            ("10_⚙️_Backtest_MA.py", "⚙️ Backtest MA Crossover", "Golden/Death Cross"),
            ("11_⚙️_Backtest_Wyckoff.py", "⚙️ Backtest Wyckoff", "Wyckoff + Minervini"),
        ],
    },
    {
        "name": "📰 Berita & Sentimen",
        "desc": "Analisis sentimen berita via AI/NLP",
        "pages": [
            ("12_📰_News_Sentiment.py", "📰 News Sentiment", "NLP VADER untuk berita"),
            ("13_🤖_Sentimeter.py", "🤖 Sentimeter", "AI sentiment + rekomendasi"),
            ("14_📰_Auto_News.py", "📰 Auto News", "Laporan berita AI"),
        ],
    },
    {
        "name": "🤖 AI & Machine Learning",
        "desc": "Agentic AI, LLM, dan analisis cerdas",
        "pages": [
            ("15_🧠_StockAI.py", "🧠 StockAI", "AI trading toolkit"),
            ("16_🤖_AI_Saham.py", "🤖 AI Saham", "AI agent CLI"),
            ("17_🦅_Maverick_MCP.py", "🦅 Maverick MCP", "52 AI tools via MCP"),
            ("18_🏦_Stock_MCP_Pro.py", "🏦 Stock MCP Pro", "Market segmentation"),
            ("19_🚀_Pulse_CLI.py", "🚀 Pulse CLI", "AI + ML trading"),
        ],
    },
    {
        "name": "📡 Data & API",
        "desc": "Sumber data IDX, SDK, dan scraper",
        "pages": [
            ("20_⚡_Live_Price.py", "⚡ Live Price", "Harga real-time"),
            ("21_🏦_IDX_SDK.py", "🏦 IDX SDK", "Direct API bursa"),
            ("22_💰_Bursarium.py", "💰 Bursarium", "Live API Cloudflare"),
            ("23_🏦_IDX_API.py", "🏦 IDX API", "Server lokal Deno"),
            ("24_📋_Indeks_Konstituen.py", "📋 Indeks Konstituen", "IDX80, KOMPAS100"),
            ("25_📑_IDXLens.py", "📑 IDXLens", "Ekstraksi XBRL"),
            ("26_📊_Indo_Scraper.py", "📊 Indo Scraper", "Scraper harga"),
            ("27_📥_Bulk_Download.py", "📥 Bulk Download", "Download broker"),
        ],
    },
    {
        "name": "🌐 Aplikasi Embed",
        "desc": "UI dari proyek open-source lain",
        "pages": [
            ("28_🚀_BOZ_NextJS.py", "🚀 BOZ Next.js", "Intelligence dashboard"),
            ("29_💎_IDX_UI.py", "💎 IDX-UI", "Screener + fundamental"),
            ("30_📊_Fundamental_UI.py", "📊 Fundamental UI", "UI fundamental"),
            ("31_📊_Stock_Analyst.py", "📊 Stock Analyst", "App Streamlit"),
            ("32_📈_Saham_Analyze.py", "📈 SAHAM Analyzer", "FastAPI + React"),
            ("33_🖥️_Stocks_Dashboard.py", "🖥️ Stocks Dashboard", "Next.js + PostgreSQL"),
        ],
    },
    {
        "name": "🎯 Trading & Sistem",
        "desc": "Bot trading dan monitoring",
        "pages": [
            ("34_🎯_Saftrade.py", "🎯 Saftrade", "AI trading bot + Telegram"),
            ("35_🏢_Project_Hub.py", "🏢 Project Hub", "Monitor service"),
            ("36_✅_System_Health_Check.py", "✅ System Health Check", "Cek status halaman"),
        ],
    },
]

for cat in categories:
    st.markdown(f'<div class="category-header">{cat["name"]}</div>', unsafe_allow_html=True)
    st.caption(cat["desc"])

    cols = st.columns(2)
    for i, (path, title, desc) in enumerate(cat["pages"]):
        with cols[i % 2]:
            st.page_link(f"pages/{path}", label=f"**{title}**", help=desc)
            st.caption(f"    _{desc}_")

st.markdown("""
<div class="footer">
    🏆 IDX Super Terminal v3.0 — 40+ Open Source Projects<br>
    Streamlit • FastAPI • Next.js • Deno • Bun • Docker • PostgreSQL • MCP
</div>
""", unsafe_allow_html=True)
