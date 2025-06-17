import unittest
from unittest.mock import patch, Mock
import pandas as pd
from bs4 import BeautifulSoup
import requests # Import requests untuk mock exception
from utils.extract import fetching_content, extract_product_info, scrape_all_pages

# Mendefinisikan data HTML konstan di tingkat modul
SAMPLE_HTML_CARD = """
<div class="collection-card">
    <h3 class="product-title">Test Product</h3>
    <span class="price">$123.45</span>
    <p>Rating: ⭐ 4.5 / 5</p>
    <p>3 Colors</p>
    <p>Size: L</p>
    <p>Gender: Unisex</p>
</div>
"""

class TestExtract(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_fetching_content_success(self, mock_get):
        # Menyiapkan mock response yang sukses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html><body><p>Test Content</p></body></html>'
        mock_get.return_value = mock_response

        # Memanggil fungsi
        soup = fetching_content("http://fakeurl.com")
        
        # Pengecekan
        self.assertIsNotNone(soup)
        self.assertEqual(soup.find('p').text, "Test Content")

    @patch('utils.extract.requests.get')
    def test_fetching_content_fail(self, mock_get):
        # Menyiapkan mock response yang gagal
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")

        # Memanggil fungsi
        result = fetching_content("http://fakeurl.com")
        
        # Pengecekan
        self.assertIsNone(result)

    def test_extract_product_info(self):
        # Membuat BeautifulSoup object dari data konstan
        card_soup = BeautifulSoup(SAMPLE_HTML_CARD, 'html.parser')
        
        # Memanggil fungsi
        product_info = extract_product_info(card_soup)
        
        # Pengecekan
        self.assertIsNotNone(product_info)
        self.assertEqual(product_info['title'], 'Test Product')
        self.assertEqual(product_info['price'], '$123.45')
        self.assertIn('4.5 / 5', product_info['rating'])

    # === FUNGSI TES BARU UNTUK scrape_all_pages ===
    @patch('utils.extract.fetching_content')
    def test_scrape_all_pages(self, mock_fetching_content):
        # Menyiapkan data HTML palsu yang berisi dua kartu produk
        mock_html_page = f"<html><body>{SAMPLE_HTML_CARD}{SAMPLE_HTML_CARD}</body></html>"
        mock_soup = BeautifulSoup(mock_html_page, 'html.parser')
        
        # Mengatur agar mock `fetching_content` mengembalikan soup palsu kita
        mock_fetching_content.return_value = mock_soup
        
        # Memanggil fungsi scrape_all_pages (cukup tes 1 halaman)
        result_df = scrape_all_pages("http://fakeurl.com", total_pages=1)
        
        # Pengecekan
        # 1. Pastikan fungsi fetching_content dipanggil
        mock_fetching_content.assert_called_once()
        
        # 2. Pastikan DataFrame tidak kosong
        self.assertFalse(result_df.empty)
        
        # 3. Pastikan jumlah baris sesuai (2 kartu produk)
        self.assertEqual(len(result_df), 2)
        
        # 4. Pastikan data di salah satu baris benar
        self.assertEqual(result_df.iloc[0]['title'], 'Test Product')

if __name__ == '__main__':
    unittest.main()