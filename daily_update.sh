#!/bin/bash
# Script untuk update database saham otomatis

# Masuk ke folder proyek
cd /home/server/web-gabungan

# Aktifkan virtual environment
source venv/bin/activate

# Jalankan script Python dan simpan log-nya
echo "=== Mulai Update: $(date) ===" >> daily_update.log
python update_all_stocks.py >> daily_update.log 2>&1
echo "=== Selesai Update: $(date) ===" >> daily_update.log
