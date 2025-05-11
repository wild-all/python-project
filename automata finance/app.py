# File: app.py
import streamlit as st
import sqlite3
import pandas as pd  # <- ini sumber 'pd'
import numpy as np
from data_extractor import process_financial_data
from data_processing import clean_data
from anomaly_detection import detect_anomalies
from forecasting import make_forecast

# Inisialisasi dataframe
df = pd.DataFrame()  # <- ini sumber 'df'

# Koneksi database
try:
    conn = sqlite3.connect('finance.db')
    df = pd.read_sql('SELECT * FROM transactions', conn)
except Exception as e:
    st.error(f"Error loading data from database: {e}")
finally:
    conn.close()  # Pastikan koneksi ditutup

# Pastikan kolom 'date' diubah menjadi datetime
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Buat dashboard
st.title('🔍 Financial Dashboard')
st.image('anomalies.png')

# Tampilkan grafik jumlah transaksi
if 'amount' in df.columns:
    st.line_chart(df.set_index('date')['amount'])

# Tampilkan prediksi
st.header("🎯 3-Month Forecast")
st.image('forecast.png')

# Filter data
if 'category' in df.columns:
    category_filter = st.multiselect('Pilih Kategori', df['category'].unique())
    if category_filter:
        filtered_data = df[df['category'].isin(category_filter)]
        st.bar_chart(filtered_data.groupby('category')['amount'].sum())
else:
    st.warning("Kolom 'category' tidak ditemukan dalam data.")
