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

### Prasyarat

Sebelum memulai, pastikan sistem Anda sudah memiliki:

- **Python 3.11+** — [Download di sini](https://www.python.org/downloads/)
- **Git** — [Download di sini](https://git-scm.com/downloads)
- **(Opsional) Docker & Docker Compose** — [Download di sini](https://www.docker.com/products/docker-desktop/)

Cek versi yang terinstal di terminal:

```bash
python3 --version    # harus 3.11 atau lebih baru
git --version
docker --version     # opsional
