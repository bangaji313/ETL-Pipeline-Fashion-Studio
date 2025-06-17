import pandas as pd
import numpy as np

def transform_data(df):
    """
    Membersihkan dan mentransformasi DataFrame produk dengan urutan yang benar.

    Args:
        df (pandas.DataFrame): DataFrame berisi data produk mentah.

    Returns:
        pandas.DataFrame: DataFrame yang sudah bersih dan ditransformasi.
    """
    try:
        # Membuat salinan eksplisit untuk menghindari SettingWithCopyWarning
        df = df.copy()

        # 1. Pra-pembersihan: Ganti nilai teks yang tidak valid dengan NaN
        df['price'] = df['price'].replace('Price Unavailable', np.nan)
        df['rating'] = df['rating'].replace(['Invalid Rating / 5', 'Not Rated'], np.nan)
        
        # 2. Menghapus baris dengan data krusial yang hilang atau tidak valid
        df.dropna(subset=['price', 'rating'], inplace=True)
        df = df[df['title'] != 'Unknown Product']

        # 3. Melakukan pembersihan dan konversi tipe data
        df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)
        df['price'] = (df['price'] * 16000).astype(float)

        df['rating'] = df['rating'].str.extract(r'(\d+\.\d+)').astype(float)
        df['colors'] = df['colors'].str.extract(r'(\d+)').astype(int)

        df['size'] = df['size'].str.replace('Size: ', '').str.strip()
        df['gender'] = df['gender'].str.replace('Gender: ', '').str.strip()
        
        # 4. Finalisasi: Hapus duplikat dan atur ulang index
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # 5. Memastikan tipe data akhir sesuai kriteria
        df = df.astype({
            'title': 'object',
            'price': 'float64',
            'rating': 'float64',
            'colors': 'int64',
            'size': 'object',
            'gender': 'object'
        })

        print("Transformasi data selesai.")
        return df

    except Exception as e:
        print(f"Error saat melakukan transformasi data: {e}")
        return pd.DataFrame()