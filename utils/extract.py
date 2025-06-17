import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def fetching_content(url):
    """
    Mengambil konten HTML dari sebuah URL.
    
    Args:
        url (str): URL dari halaman web.

    Returns:
        BeautifulSoup object: Objek BeautifulSoup dari konten halaman, atau None jika gagal.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Akan menimbulkan error jika status code bukan 200
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return None

def extract_product_info(card):
    """
    Mengekstrak informasi dari satu kartu produk.

    Args:
        card (bs4.element.Tag): Tag HTML yang berisi satu produk.

    Returns:
        dict: Kamus berisi informasi produk, atau None jika data tidak lengkap.
    """
    try:
        # Menggunakan selector yang benar sesuai hasil inspect
        title = card.find('h3', {'class': 'product-title'}).text.strip()
        
        # Menggunakan find(class_='...') agar lebih fleksibel untuk menemukan tag dengan class 'price'
        price_tag = card.find(class_='price')
        price_text = price_tag.text.strip() if price_tag else None

        rating_text = card.find('p', string=lambda text: 'Rating' in text).text.strip()
        colors_text = card.find('p', string=lambda text: 'Colors' in text).text.strip()
        size_text = card.find('p', string=lambda text: 'Size' in text).text.strip()
        gender_text = card.find('p', string=lambda text: 'Gender' in text).text.strip()
        
        product_info = {
            "title": title,
            "price": price_text,
            "rating": rating_text,
            "colors": colors_text,
            "size": size_text,
            "gender": gender_text,
            "timestamp": datetime.now() # Menambahkan timestamp sesuai kriteria 'Skilled'
        }
        return product_info
    except AttributeError:
        # Terjadi jika salah satu elemen penting tidak ditemukan (misal: judul)
        return None

def scrape_all_pages(base_url, total_pages=50):
    """
    Melakukan scraping data dari seluruh halaman website.

    Args:
        base_url (str): URL dasar website.
        total_pages (int): Jumlah total halaman yang akan di-scrape.

    Returns:
        pandas.DataFrame: DataFrame berisi data semua produk.
    """
    all_products = []
    for page in range(1, total_pages + 1):
        # Membentuk URL untuk setiap halaman
        url = f"{base_url}?page={page}"
        print(f"Scraping page {page}...")
        
        soup = fetching_content(url)
        if soup:
            # Menggunakan selector yang benar untuk container produk
            product_cards = soup.find_all('div', {'class': 'collection-card'})
            
            for card in product_cards:
                product_data = extract_product_info(card)
                if product_data:
                    all_products.append(product_data)
    
    if not all_products:
        print("Tidak ada data produk yang berhasil diekstrak.")
        return pd.DataFrame()

    return pd.DataFrame(all_products)