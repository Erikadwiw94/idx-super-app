# ⚡ IDX Super App - Platform Analisis Saham Terpadu

Selamat datang di **IDX Super App**, sebuah platform analisis saham Indonesia (IDX) yang komprehensif dan berjalan 100% di server pribadi Anda. Proyek ini menggabungkan berbagai teknik analisis (Teknikal, Fundamental, Bandarmology, Sentimen AI) ke dalam satu antarmuka web yang modern dan interaktif.

Dibangun dengan **Streamlit** dan **Python**, platform ini mengintegrasikan puluhan proyek open-source dan library analisis data untuk memberikan wawasan pasar yang *real-time* dan mendalam.

## ✨ Fitur Utama

*   📊 **Screener Saham (Full Market):** Memindai 900+ saham IDX secara instan menggunakan database lokal SQLite (RSI, MA20, dll).
*   🔥 **Mega Dashboard (113 Indikator):** Menghitung lebih dari 100 indikator teknikal sekaligus (Trend, Momentum, Volatilitas, Volume) berdasarkan daftar indikator Stockbit Pro, menggunakan library `pandas-ta-classic`.
*   🕵️ **Bandarmology (Big Money Tracker):** Melacak akumulasi dan distribusi "Bandar" menggunakan indikator On-Balance Volume (OBV) dan Volume Spike.
*   📉 **Pro Technical & Playground:** Visualisasi grafik candlestick interaktif dengan overlay indikator (Bollinger Bands, Supertrend, Ichimoku, dll).
*   📡 **Broker Summary Live:** Integrasi dengan server MCP lokal (`jv-idx-mcp`) untuk mengambil data ringkasan broker (Top Buyer/Seller) secara *real-time*.
*   🤖 **Sentiment AI:** Analisis sentimen berita pasar menggunakan NLP (VADER) untuk memberikan gambaran psikologis pasar.
*   ⚙️ **Backtest:** Uji strategi trading (misal: MA Crossover) dengan data historis.
*   🧠 **Ultimate Analyzer:** Skor komposit (0-100) yang menggabungkan Teknikal, Fundamental, Bandarmologi, dan Sentimen untuk memberikan rekomendasi BUY/HOLD/SELL.

## 🛠️ Teknologi yang Digunakan

*   **Frontend & Web Framework:** [Streamlit](https://streamlit.io/)
*   **Analisis Data & Indikator:** Pandas, NumPy, [pandas-ta-classic](https://github.com/StreamAlpha/pandas_ta)
*   **Visualisasi Data:** [Plotly](https://plotly.com/python/)
*   **Data Pasar:** [yfinance](https://github.com/ranaroussi/yfinance)
*   **Database:** SQLite (Lokal)
*   **Integrasi API:** `requests`, `jv-idx-mcp` (Docker), WebSocket
*   **AI & Sentimen:** VADER Sentiment, Feedparser (Google News RSS)

## 🚀 Cara Instalasi (Local / Server)

Ikuti langkah-langkah berikut untuk menjalankan platform ini di server Anda sendiri:

1. **Clone Repositori:**
   ```bash
   git clone https://github.com/Erikadwiw94/web-gabungan.git
   cd web-gabungan
Buat Virtual Environment & Install Dependensi:

bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
(Catatan: Jika requirements.txt belum ada, Anda bisa menginstal library utama secara manual: pip install streamlit yfinance pandas pandas-ta-classic plotly requests feedparser vaderSentiment)

Jalankan Aplikasi:

bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Buka di Browser:
Akses http://localhost:8501 atau http://<IP_SERVER_ANDA>:8501.

📁 Struktur Proyek
text
web-gabungan/
│
├── app.py                     # Halaman utama (Landing Page)
├── update_database.py         # Script scraper data saham ke SQLite
├── update_all_stocks.py       # Script scraper 900+ saham IDX
├── stock_data.db              # Database lokal (di-ignore oleh Git)
│
├── pages/                     # Folder halaman Streamlit
│   ├── 1_Screener.py
│   ├── 2_Bandarmology.py
│   ├── 3_Backtest.py
│   ├── 4_Sentiment_AI.py
│   ├── 5_Live_Price.py
│   ├── 6_Ultimate_Analyzer.py
│   ├── 7_Pro_Technical.py
│   ├── 8_Indicator_Playground.py
│   ├── 9_Dashboard_Angka.py
│   └── 10_Broker_Summary_Live.py
│
└── README.md
🤝 Berkontribusi
Proyek ini dibangun untuk keperluan edukasi dan riset pribadi. Jika Anda ingin menambahkan fitur baru atau memperbaiki bug, silakan lakukan Pull Request.

⚠️ Disclaimer
Platform ini dibuat untuk tujuan edukasi dan analisis. Segala keputusan investasi yang diambil berdasarkan informasi dari platform ini adalah tanggung jawab pengguna sepenuhnya. Selalu lakukan riset mandiri (DYOR) sebelum bertransaksi di pasar modal.
