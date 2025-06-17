from utils.extract import scrape_all_pages
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql
import pandas as pd

if __name__ == "__main__":
    BASE_URL = "https://fashion-studio.dicoding.dev/"
    
    # --- Konfigurasi untuk Tahap Load ---
    CSV_FILENAME = 'products.csv'
    GOOGLE_SHEETS_URL = 'https://docs.google.com/spreadsheets/d/1sDRcgTyUDPXKVN-qgMHrshYGZB73VyNld7lFXanmjGI/edit?gid=0#gid=0'
    GOOGLE_SHEETS_CREDENTIALS = 'google-sheets-api.json' 

    # Ganti dengan detail koneksi database PostgreSQL Anda
    POSTGRES_PARAMS = {
        "host": "localhost",
        "port": "5432",
        "dbname": "fashion_etl_db",
        "user": "postgres",
        "password": "bangaji313_" 
    }
    
    # =======================================
    
    print("Memulai proses ETL...")
    
    # 1. TAHAP EKSTRAKSI
    print("\nTahap 1: Ekstraksi Data...")
    raw_df = scrape_all_pages(BASE_URL, total_pages=50)
    
    if raw_df.empty:
        print("Ekstraksi data gagal. Proses ETL dihentikan.")
    else:
        print("Ekstraksi Data Selesai.")
        
        # 2. TAHAP TRANSFORMASI
        print("\nTahap 2: Transformasi Data...")
        cleaned_df = transform_data(raw_df)
        
        if cleaned_df.empty:
            print("Transformasi data gagal. Proses ETL dihentikan.")
        else:
            print("Transformasi Data Selesai.")
            
            # 3. TAHAP PEMUATAN DATA (LOAD)
            print("\nTahap 3: Pemuatan Data...")
    
            load_to_csv(cleaned_df, CSV_FILENAME)
            load_to_google_sheets(cleaned_df, GOOGLE_SHEETS_URL, GOOGLE_SHEETS_CREDENTIALS)
            load_to_postgresql(cleaned_df, POSTGRES_PARAMS)
            
            print("\nProses ETL selesai.")