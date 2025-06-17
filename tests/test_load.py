import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import load_to_csv

class TestLoad(unittest.TestCase):

    @patch('pandas.DataFrame.to_csv')
    def test_load_to_csv(self, mock_to_csv):
        # Menyiapkan DataFrame sampel
        sample_data = {'col1': [1, 2], 'col2': ['A', 'B']}
        sample_df = pd.DataFrame(sample_data)
        
        # Nama file dummy
        filename = "dummy_output.csv"
        
        # Memanggil fungsi
        load_to_csv(sample_df, filename)
        
        # Pengecekan: memastikan fungsi to_csv dipanggil dengan benar
        mock_to_csv.assert_called_once_with(filename, index=False)

if __name__ == '__main__':
    unittest.main()