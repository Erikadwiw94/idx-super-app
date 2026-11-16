# ⚡ IDX Super App

### Platform Analisis Saham Indonesia Terpadu & Open-Source

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

[![GitHub stars](https://img.shields.io/github/stars/Erikadwiw94/web-gabungan?style=social)](https://github.com/Erikadwiw94/web-gabungan/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Erikadwiw94/web-gabungan?style=social)](https://github.com/Erikadwiw94/web-gabungan/network/members)
[![GitHub issues](https://img.shields.io/github/issues/Erikadwiw94/web-gabungan)](https://github.com/Erikadwiw94/web-gabungan/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**Sebuah "Super App" untuk analisis saham IDX yang menggabungkan Teknikal, Fundamental, Bandarmology, dan Sentimen AI dalam satu dashboard.**

[Fitur](#-fitur-utama) • [Instalasi](#-instalasi) • [Screenshots](#-screenshots) • [Roadmap](#-roadmap) • [Kontribusi](#-berkontribusi)

</div>

---

## 📖 Tentang Proyek

**IDX Super App** adalah platform analisis saham *self-hosted* untuk pasar modal Indonesia (Bursa Efek Indonesia). Proyek ini lahir dari kebutuhan akan alat analisis yang **gratis, transparan, dan bisa dikustomisasi** — sesuatu yang jarang ditemukan di platform komersial.

Alih-alih hanya mengandalkan satu indikator, platform ini menggunakan pendekatan **Multi-Factor Analysis** yang menggabungkan:

- 📈 **Analisis Teknikal** (113+ indikator dari `pandas-ta-classic`)
- 💰 **Analisis Fundamental** (PER, PBV, ROE, DER dari Bursarium)
- 🕵️ **Bandarmology** (OBV, Volume Spike, Broker Summary)
- 🤖 **Sentimen Pasar** (NLP dari berita Google News)

Semua berjalan di server Anda sendiri, tanpa biaya langganan bulanan.

---

## ✨ Fitur Utama

| Fitur | Deskripsi | Status |
| :--- | :--- | :---: |
| 📊 **Screener Full Market** | Scan 900+ saham IDX dengan RSI, MA20, dan filter fundamental secara instan. | ✅ |
| 🔥 **Mega Dashboard (113 Indikator)** | Hitung 113 indikator teknikal sekaligus (Trend, Momentum, Volatilitas, Volume). | ✅ |
| 🕵️ **Bandarmology Tracker** | Deteksi akumulasi/distribusi "Bandar" via On-Balance Volume & Volume Spike. | ✅ |
| 📉 **Pro Technical Chart** | Grafik candlestick interaktif dengan 14+ overlay indikator profesional. | ✅ |
| 🎛️ **Indicator Playground** | Kombinasikan overlay & oscillator sesuka hati dalam satu grafik. | ✅ |
| 📋 **Dashboard Angka** | Nilai numerik semua indikator (multi-timeframe: Harian/Mingguan/Bulanan). | ✅ |
| 📡 **Broker Summary Live** | Integrasi dengan `jv-idx-mcp` (Docker) untuk data Top Buyer/Seller real-time. | ✅ |
| 🧠 **Ultimate AI Analyzer** | Skor komposit 0-100 (Teknikal+Fundamental+Bandar+Sentimen) untuk sinyal BUY/HOLD/SELL. | ✅ |
| 🤖 **Sentiment AI** | Analisis sentimen berita via VADER NLP. | ✅ |
| ⚙️ **Backtest Engine** | Uji strategi MA Crossover dengan grafik ekuitas vs Buy & Hold. | ✅ |
| ⚡ **Live Price WebSocket** | Streaming harga real-time via WebSocket (eksperimental). | 🚧 |
| 🗄️ **Full Fundamental DB** | Import 842 saham fundamental dari Bursarium. | 🚧 |
| 🔔 **Telegram Bot Alert** | Notifikasi otomatis hasil screener harian ke Telegram. | 📅 |

**Legend:** ✅ Selesai · 🚧 Dalam Pengembangan · 📅 Direncanakan

---

## 📸 Screenshots

> *Tambahkan screenshot Anda sendiri di folder `screenshots/` untuk membuat README ini lebih hidup!*

| Landing Page | Mega Dashboard 113 Indikator |
| :---: | :---: |
| ![Home](screenshots/home.png) | ![Mega Dashboard](screenshots/mega-dashboard.png) |

| Bandarmology | Ultimate Analyzer |
| :---: | :---: |
| ![Bandarmology](screenshots/bandarmology.png) | ![Analyzer](screenshots/analyzer.png) |

*(Cara menambahkan: buat folder `screenshots/`, lalu letakkan file gambar dengan nama sesuai di atas).*

---

## 🛠️ Teknologi yang Digunakan

<table>
<tr>
<td valign="top" width="33%">

**Frontend**
- Streamlit
- Plotly (Interactive Charts)
- Custom CSS

**Data & Analisis**
- Pandas & NumPy
- pandas-ta-classic
- yfinance

</td>
<td valign="top" width="33%">

**Backend & Storage**
- Python 3.11+
- SQLite (lokal)
- PostgreSQL (Stocks Dashboard)
- APScheduler (cron)

**Integrasi & AI**
- requests, WebSocket
- VADER Sentiment
- feedparser (RSS)

</td>
<td valign="top" width="33%">

**Infrastruktur**
- Docker & Compose
- systemd (auto-start)
- GitHub Actions (CI/CD)

**Data Source**
- Yahoo Finance
- Bursarium
- jv-idx-mcp (MCP Server)

</td>
</tr>
</table>

---

## 🏗️ Arsitektur Sistem

```text
┌──────────────────────────────────────────────────────────────────┐
│                      USER (Browser / HP)                         │
└───────────────────────────┬──────────────────────────────────────┘
                            │ HTTP :8501
┌───────────────────────────▼──────────────────────────────────────┐
│             STREAMLIT FRONTEND (Multi-Page App)                  │
│  Screener │ Bandarmology │ 113 Indikator │ Broker Summary │ AI   │
└───────┬──────────────────────┬──────────────────────┬────────────┘
        │                      │                      │
   ┌────▼────┐          ┌──────▼──────┐        ┌──────▼──────┐
   │ SQLite  │          │  yfinance   │        │  jv-idx-mcp │
   │ (Lokal) │          │ (Yahoo API) │        │  (Docker)   │
   └─────────┘          └─────────────┘        └─────────────┘
        │                                             │
   ┌────▼─────────┐                             ┌─────▼───────┐
   │   Bursarium  │                             │  MCP Server │
   │  (Fundamental│                             │  Port 8000  │
   └──────────────┘                             └─────────────┘

## 🚀 Instalasi

### Prasyarat

- **Python 3.11+**
- **Git**
- *(Opsional)* **Docker & Docker Compose**

### Langkah Cepat

```bash
# 1. Clone repositori
git clone https://github.com/Erikadwiw94/web-gabungan.git
cd web-gabungan

# 2. Buat virtual environment
python3 -m venv venv
source venv/bin/activate     # Linux/Mac
# venv\Scripts\activate      # Windows

# 3. Install dependensi
pip install -r requirements.txt

# 4. (Opsional) Inisialisasi database saham
python update_all_stocks.py

# 5. Jalankan aplikasi
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Akses di browser: **`http://localhost:8501`**

### 🐳 Instalasi via Docker (Coming Soon)

```bash
docker compose up -d
```

---

## 📁 Struktur Proyek

```text
web-gabungan/
│
├── app.py                     # Landing page utama
├── update_database.py         # Scraper 50 saham (quick)
├── update_all_stocks.py       # Scraper 900+ saham (full market)
├── requirements.txt           # Dependensi Python
├── .gitignore                 # File yang diabaikan Git
│
├── pages/                     # Halaman Streamlit
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
├── screenshots/               # Gambar untuk README
├── LICENSE                    # MIT License
├── CONTRIBUTING.md            # Panduan kontribusi
└── README.md
```

---

## 🗺️ Roadmap

- [x] Screener Full Market (900+ saham)
- [x] Mega Dashboard 113 Indikator
- [x] Bandarmology via OBV
- [x] Ultimate AI Analyzer (Composite Score)
- [x] Integrasi Broker Summary (MCP)
- [ ] Full Import 842 Saham Fundamental
- [ ] Live Price via WebSocket Stabil
- [ ] Auto-Start via systemd
- [ ] Docker Compose Siap Pakai
- [ ] Telegram Bot Alert Harian
- [ ] Mobile-Friendly Layout
- [ ] REST API Publik (FastAPI)
- [ ] Unit Test & CI/CD Pipeline
- [ ] Terjemahan Multibahasa (ID/EN)

Lihat [Issues](https://github.com/Erikadwiw94/web-gabungan/issues) untuk daftar lengkap fitur yang sedang dikerjakan.

---

## 🤝 Berkontribusi

Kami sangat terbuka untuk kontribusi dari siapa pun! Baik itu perbaikan bug, penambahan fitur, perbaikan dokumentasi, atau sekadar memberi ⭐ pada repositori ini.

Silakan baca **[CONTRIBUTING.md](CONTRIBUTING.md)** untuk panduan lengkap.

### Cara Cepat Berkontribusi:

1. 🍴 **Fork** repositori ini
2. 🌿 Buat branch baru (`git checkout -b feature/FiturKeren`)
3. 💾 Commit perubahan (`git commit -m 'Menambahkan FiturKeren'`)
4. 📤 Push ke branch (`git push origin feature/FiturKeren`)
5. 🔃 Buat **Pull Request**

### 💡 Ide Kontribusi untuk Pemula:

- Perbaiki typo di dokumentasi
- Tambahkan screenshot baru
- Menambahkan indikator teknikal baru
- Menerjemahkan README ke bahasa Inggris
- Membuat unit test

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah **MIT License** — lihat file [LICENSE](LICENSE) untuk detailnya.

Anda bebas menggunakan, memodifikasi, dan mendistribusikan kode ini, termasuk untuk tujuan komersial, selama menyertakan atribusi.

---

## ⚠️ Disclaimer

> **Platform ini dibuat untuk tujuan edukasi dan riset.**
> Segala keputusan investasi yang diambil berdasarkan informasi dari platform ini adalah tanggung jawab pengguna sepenuhnya. Selalu lakukan riset mandiri (**DYOR**) sebelum bertransaksi di pasar modal. Saham adalah instrumen berisiko tinggi — Anda bisa kehilangan seluruh modal Anda.

---

## 🙏 Acknowledgments

Terima kasih kepada para pengembang open-source yang karyanya menjadi fondasi proyek ini:

- [Streamlit](https://streamlit.io/) · [Pandas TA Classic](https://github.com/StreamAlpha/pandas_ta) · [yfinance](https://github.com/ranaroussi/yfinance)
- [jv-idx-mcp](https://github.com/ibpme/jv-idx-mcp) · [idx-bei](https://github.com/nichsedge/idx-bei) · [Bursarium](https://github.com/herbras/bursarium)
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment) · [Plotly](https://plotly.com/python/)
- Seluruh kontributor komunitas IDX yang telah berbagi data dan ide.

---

<div align="center">

**⭐ Jika proyek ini bermanfaat, jangan lupa beri bintang! ⭐**

Dibuat dengan ❤️ untuk komunitas investor Indonesia.

</div>
