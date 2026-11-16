#!/bin/bash
# Script untuk menyalakan semua layanan pendukung secara otomatis

LOG_FILE="/home/server/web-gabungan/services.log"
echo "=== $(date): Memulai semua layanan ===" >> "$LOG_FILE"

port_up() {
    ss -tulpn 2>/dev/null | grep -q ":$1 " && return 0 || return 1
}

# 1. Docker Containers
echo "[1/10] Menyalakan Docker containers..." >> "$LOG_FILE"
docker start jv-idx-mcp 2>/dev/null
docker start maverick-mcp-backend-1 maverick-mcp-postgres-1 maverick-mcp-redis-1 2>/dev/null
docker start idx-stock-api idx-report-server 2>/dev/null
docker start saham 2>/dev/null

# 2. Stocks Backend & Frontend (systemd)
echo "[2/10] Stocks Dashboard (systemd)..." >> "$LOG_FILE"
systemctl start stocks-backend 2>/dev/null
systemctl start stocks-frontend 2>/dev/null

# 3. BOZ (Next.js)
if ! port_up 21526; then
    echo "[3/10] Menyalakan BOZ..." >> "$LOG_FILE"
    cd /home/server/BOZ
    nohup npx next dev --webpack --hostname 0.0.0.0 --port 21526 > boz_web.log 2>&1 &
fi

# 4. IDX-UI (Deno)
if ! port_up 50270; then
    echo "[4/10] Menyalakan IDX-UI..." >> "$LOG_FILE"
    cd /home/server/IDX-UI
    nohup deno task api:serve > idx_ui_api.log 2>&1 &
fi

# 5. Sentimeter (Bun API)
if ! port_up 3001; then
    echo "[5/10] Menyalakan Sentimeter API..." >> "$LOG_FILE"
    cd /home/server/sentimeter
    nohup bun run dev > sentimeter.log 2>&1 &
fi

# 6. Stock-Market-Analyst
if ! port_up 8503; then
    echo "[6/10] Menyalakan Stock Analyst..." >> "$LOG_FILE"
    cd /home/server/Stock-Market-Analyst
    if [ -f venv/bin/activate ]; then
        source venv/bin/activate
        nohup streamlit run appv1.py --server.port 8503 --server.address 0.0.0.0 > analyst.log 2>&1 &
        deactivate
    fi
fi

# 7. Fundamental UI (Bun)
if ! port_up 5173; then
    echo "[7/10] Menyalakan Fundamental UI..." >> "$LOG_FILE"
    cd /home/server/idx-fundamental-analysis/app/ui
    nohup env PUBLIC_API_BASE_URL="http://localhost:8001" bun run dev --host 0.0.0.0 --port 5173 --strictPort > ui.log 2>&1 &
fi

# 8. Fundamental API Backend (port 8001)
if ! port_up 8001; then
    echo "[8/10] Menyalakan Fundamental API..." >> "$LOG_FILE"
    cd /home/server/idx-fundamental-analysis
    nohup .venv/bin/python run_api.py > api.log 2>&1 &
fi

# 9. IDX-API (Deno port 52060)
if ! port_up 52060; then
    echo "[9/10] Menyalakan IDX-API..." >> "$LOG_FILE"
    cd /home/server/IDX-API
    nohup deno task serve > idx_api.log 2>&1 &
fi

# 10. Saham-Analyze Docker (port 8765)
echo "[10/10] Saham Docker (jika belum jalan)..." >> "$LOG_FILE"
docker start saham 2>/dev/null

echo "=== $(date): Semua layanan dijalankan ===" >> "$LOG_FILE"
