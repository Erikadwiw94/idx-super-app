import sqlite3
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

# Daftar 50+ Saham IDX Populer (LQ45 + Bluechips)
TICKERS = [
    "BBCA", "BBRI", "BMRI", "BBNI", "TLKM", "ASII", "UNVR", "ICBP", "GOTO", "ADRO",
    "ANTM", "CPIN", "KLBF", "MDKA", "PGAS", "TPIA", "RAJA", "AMRT", "BRPT", "CPIN",
    "EXCL", "INCO", "INDF", "INKP", "ISAT", "ITMG", "JSMR", "MBMA", "MEDC", "MTEL",
    "PGEO", "PTBA", "SIDO", "SMGR", "SMRA", "TBIG", "TINS", "TOWR", "UNTR", "ACES",
    "AKRA", "ARTO", "BFIN", "BRIS", "BSDE", "BTPS", "CTRA", "ELSA", "ERAA", "ESSA"
]

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

def update_data():
    conn = init_db()
    cursor = conn.cursor()
    
    print(f"[{datetime.now()}] Memulai update data {len(TICKERS)} saham...")
    
    for i, ticker in enumerate(TICKERS):
        try:
            print(f"({i+1}/{len(TICKERS)}) Mengunduh {ticker}...", end=" ")
            df = yf.download(f"{ticker}.JK", period="1y", interval="1d", progress=False)
            
            if df.empty:
                print("Data kosong, dilewati.")
                continue
                
            # Ratakan MultiIndex jika ada
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            df = df.reset_index()
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
            df['Ticker'] = ticker
            
            # Simpan ke SQLite (Abaikan jika data sudah ada)
            for index, row in df.iterrows():
                cursor.execute('''
                    INSERT OR IGNORE INTO daily_prices (ticker, date, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (row['Ticker'], row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))
            
            conn.commit()
            print("Sukses!")
            time.sleep(0.5) # Jeda agar tidak diblokir Yahoo
            
        except Exception as e:
            print(f"Error: {e}")
            
    conn.close()
    print(f"\n[{datetime.now()}] Update database selesai!")

if __name__ == "__main__":
    update_data()
