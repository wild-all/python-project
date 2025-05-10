# File: data_processing.py
from sklearn.preprocessing import LabelEncoder
from transformers import pipeline
import pandas as pd  # <- ini sumber 'pd'
import numpy as np
import sqlite3
import re  # untuk regex

# Inisialisasi dataframe
df = pd.DataFrame()  # <- ini sumber 'df'

# Inisialisasi classifier
classifier = pipeline('zero-shot-classification')

categories = ["operational", "gaji", "investasi", "pajak", "lainnya"]

def auto_categorize(description):
    """Kategorisasi transaksi menggunakan AI"""
    result = classifier(
        description,
        candidate_labels=categories,
        multi_label=False
    )
    return result['labels'][0]

# Ambil data dari database (misalnya, jika Anda ingin memproses data dari database)
def load_data():
    conn = sqlite3.connect('finance.db')
    return pd.read_sql('SELECT * FROM transactions', conn)

# Mengisi DataFrame dengan data dari database
df = load_data()

# Contoh pemakaian
df['category'] = df['description'].apply(auto_categorize)  # Perbaiki di sini
df['date'] = pd.to_datetime(df['date'])  # Perbaiki di sini
df = df.sort_values('date')

# Simpan ke database
df.to_sql('transactions', sqlite3.connect('finance.db'), if_exists='replace', index=False)  # Menambahkan index=False
