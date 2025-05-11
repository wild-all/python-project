# File: data_extractor.py
import pandas as pd
import pytesseract
from pdf2image import convert_from_path
import glob
import re  # untuk regex

# Inisialisasi dataframe
df = pd.DataFrame()  # <- ini sumber 'df'

def extract_image_text(image_path):
    """Ekstrak teks dari gambar/PDF menggunakan OCR"""
    if image_path.endswith('.pdf'):
        images = convert_from_path(image_path)
        text = ''.join([pytesseract.image_to_string(img) for img in images])
    else:
        text = pytesseract.image_to_string(image_path)
    return text

def process_financial_data():
    """Gabungkan data dari berbagai sumber"""
    # 1. Load data Excel
    excel_data = pd.read_excel('data/keuangan.xlsx')
    
    # 2. Proses gambar/PDF
    raw_data = []
    for file in glob.glob('invoices/*'):  # Cari semua file di folder invoices
        text = extract_image_text(file)
        
        # Contoh parsing sederhana (bisa dikembangkan pakai regex/NLP)
        try:
            amount = float(re.search(r'Total\s*:\s*(\d+\.\d+)', text).group(1))
            date = re.search(r'\d{2}-\d{2}-\d{4}', text).group()
            raw_data.append({'date': date, 'amount': amount, 'source': file})
        except AttributeError:
            print(f"Data tidak ditemukan di file: {file}")
        except ValueError:
            print(f"Format jumlah tidak valid di file: {file}")

    # Gabungkan semua data
    raw_df = pd.DataFrame(raw_data)
    
    # Pastikan kolom 'date' diubah menjadi datetime
    raw_df['date'] = pd.to_datetime(raw_df['date'], format='%d-%m-%Y', errors='coerce')
    
    # Gabungkan dengan data Excel
    combined_df = pd.concat([excel_data, raw_df], ignore_index=True)
    
    return combined_df

df = process_financial_data()
