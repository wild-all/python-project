import os
import pandas as pd
import pytesseract
from pdf2image import convert_from_path
import glob
import re  # untuk regex

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
    # Dapatkan path ke direktori saat ini (folder dimana file script ini berada)
    current_dir = os.path.dirname(__file__)
    # Bangun path lengkap ke file Excel 'keuangan.xlsx' di subfolder 'data'
    excel_path = os.path.join(current_dir, 'data', 'keuangan.xlsx')
    # Load data Excel menggunakan path yang benar
    excel_data = pd.read_excel(excel_path)

    # Proses gambar/PDF dalam folder 'invoices' di direktori saat ini
    raw_data = []
    invoices_dir = os.path.join(current_dir, 'invoices')
    for file in glob.glob(os.path.join(invoices_dir, '*')):
        text = extract_image_text(file)
        try:
            amount = float(re.search(r'Total\s*:\s*(\d+\.\d+)', text).group(1))
            date = re.search(r'\d{2}-\d{2}-\d{4}', text).group()
            raw_data.append({'date': date, 'amount': amount, 'source': file})
        except AttributeError:
            print(f"Data tidak ditemukan di file: {file}")
        except ValueError:
            print(f"Format jumlah tidak valid di file: {file}")

    raw_df = pd.DataFrame(raw_data)
    raw_df['date'] = pd.to_datetime(raw_df['date'], format='%d-%m-%Y', errors='coerce')

    # Gabungkan data Excel dan hasil ekstrak dari gambar/PDF
    combined_df = pd.concat([excel_data, raw_df], ignore_index=True)

    return combined_df