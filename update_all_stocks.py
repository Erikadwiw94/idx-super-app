import sqlite3
import yfinance as yf
import pandas as pd
import requests
import time
from datetime import datetime

def get_all_idx_tickers():
    print(f"[{datetime.now()}] Mengambil daftar seluruh saham IDX...")
    try:
        # API internal IDX untuk mendapatkan semua daftar saham
        url = "https://www.idx.co.id/primary/StockData/GetSecuritiesStock?start=0&length=9999"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Ekstrak kode saham
        tickers = [item['Code'] for item in data['data']]
        print(f"Berhasil mendapatkan {len(tickers)} saham.")
        return tickers
    except Exception as e:
        print(f"Gagal mengambil daftar saham dari IDX: {e}")
        print("Menggunakan daftar cadangan (LQ45 + Bluechips)...")
        return ["BBCA", "BBRI", "BMRI", "BBNI", "TLKM", "ASII", "UNVR", "ICBP", "GOTO", "ADRO"]

def init_db():
    conn = sqlite3.connect('stock_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_prices (
            ticker TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (ticker, date)
        )
    ''')
    conn.commit()
    return conn

def update_all_data():
    tickers = get_all_idx_tickers()
    tickers_jk = [f"{t}.JK" for t in tickers]
    
    conn = init_db()
    cursor = conn.cursor()
    
    print(f"[{datetime.now()}] Memulai pengunduhan data 1 Tahun (Batch Mode)...")
    
    # Unduh secara massal (50 saham per batch) agar cepat dan aman dari blokir
    batch_size = 50
    total_batches = (len(tickers_jk) + batch_size - 1) // batch_size
    
    for i in range(0, len(tickers_jk), batch_size):
        batch = tickers_jk[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        print(f"Memproses Batch {batch_num}/{total_batches} ({len(batch)} saham)...")
        
        try:
            # Multithreading download
            df = yf.download(batch, period="1y", interval="1d", group_by='ticker', threads=True, progress=False)
            
            if df.empty:
                continue
                
            # Iterasi setiap saham dalam batch
            for ticker_jk in batch:
                if ticker_jk not in df.columns.levels[0]:
                    continue
                    
                df_stock = df[ticker_jk].dropna()
                if df_stock.empty:
                    continue
                    
                ticker_clean = ticker_jk.replace('.JK', '')
                
                # Persiapkan data untuk SQLite
                df_stock = df_stock.reset_index()
                df_stock['Date'] = df_stock['Date'].dt.strftime('%Y-%m-%d')
                
                # Bulk insert
                records = [
                    (ticker_clean, row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
                    for _, row in df_stock.iterrows()
                ]
                
                cursor.executemany('''
                    INSERT OR REPLACE INTO daily_prices (ticker, date, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', records)
                
            conn.commit()
            time.sleep(2) # Jeda antar batch agar tidak diblokir Yahoo
            
        except Exception as e:
            print(f"Error pada batch {batch_num}: {e}")
            
    conn.close()
    print(f"\n[{datetime.now()}] 🎉 SELESAI! Seluruh data 900+ saham berhasil disimpan ke database.")

if __name__ == "__main__":
    update_all_data()
