import pandas as pd
import gspread
from sqlalchemy import create_engine

def load_to_csv(df, filename):
    """
    Menyimpan DataFrame ke dalam file CSV.
    """
    try:
        df.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"Error saat menyimpan ke CSV: {e}")

def load_to_google_sheets(df, sheet_url, credentials_path):
    """
    Memuat DataFrame ke Google Sheets.
    """
    try:
        # Membuat salinan DataFrame untuk diubah tipe datanya
        df_to_load = df.copy()
        
        # Mengubah kolom timestamp menjadi string untuk menghindari masalah serialisasi
        if 'timestamp' in df_to_load.columns:
            df_to_load['timestamp'] = df_to_load['timestamp'].astype(str)

        gc = gspread.service_account(filename=credentials_path)
        spreadsheet = gc.open_by_url(sheet_url)
        worksheet = spreadsheet.get_worksheet(0)
        
        worksheet.clear()
        # Menggunakan df_to_load yang sudah diubah
        worksheet.update([df_to_load.columns.values.tolist()] + df_to_load.values.tolist())
        print("Data berhasil dimuat ke Google Sheets.")
    except Exception as e:
        print(f"Error saat memuat ke Google Sheets: {e}")

def load_to_postgresql(df, db_params):
    """
    Memuat DataFrame ke tabel PostgreSQL.
    """
    try:
        connection_str = f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
        engine = create_engine(connection_str)
        
        df.to_sql('products', engine, if_exists='replace', index=False)
        print("Data berhasil dimuat ke PostgreSQL.")
    except Exception as e:
        print(f"Error saat memuat ke PostgreSQL: {e}")