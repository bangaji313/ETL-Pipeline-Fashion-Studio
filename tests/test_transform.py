import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):

    def test_transform_data(self):
        # Menyiapkan data mentah sampel
        raw_data = {
            'title': ['T-shirt 1', 'Unknown Product', 'Pants 2'],
            'price': ['$50.00', 'Price Unavailable', '$75.50'],
            'rating': ['Rating: ⭐ 4.5 / 5', 'Not Rated', 'Rating: ⭐ 3.0 / 5'],
            'colors': ['3 Colors', '5 Colors', '2 Colors'],
            'size': ['Size: M', 'Size: L', 'Size: S'],
            'gender': ['Gender: Women', 'Gender: Unisex', 'Gender: Men'],
            'timestamp': pd.to_datetime(['2025-01-01', '2025-01-01', '2025-01-01'])
        }
        raw_df = pd.DataFrame(raw_data)
        
        # Memanggil fungsi transformasi
        cleaned_df = transform_data(raw_df.copy()) # Menggunakan .copy() agar tidak mengubah raw_df asli
        
        # Pengecekan
        # Harusnya hanya ada 2 baris yang valid
        self.assertEqual(len(cleaned_df), 2)
        
        # Cek harga T-shirt 1 (50 * 16000 = 800000)
        self.assertEqual(cleaned_df.loc[0, 'price'], 800000.0)
        
        # Cek rating Pants 2
        self.assertEqual(cleaned_df.loc[1, 'rating'], 3.0)
        
        # Cek tipe data
        self.assertEqual(cleaned_df['price'].dtype, 'float64')
        self.assertEqual(cleaned_df['colors'].dtype, 'int64')

if __name__ == '__main__':
    unittest.main()