# File: forecasting.py
from prophet import Prophet
import pandas as pd  # <- ini sumber 'pd'
import sqlite3

# Inisialisasi dataframe
df = pd.DataFrame()  # <- ini sumber 'df'

# Koneksi database dan ambil data
try:
    conn = sqlite3.connect('finance.db')
    df = pd.read_sql('SELECT * FROM transactions', conn)
except Exception as e:
    print(f"Error loading data from database: {e}")
finally:
    conn.close()  # Pastikan koneksi ditutup

# Pastikan kolom 'date' diubah menjadi datetime
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Siapkan data harian
if 'amount' in df.columns:
    daily = df.resample('D', on='date')['amount'].sum().reset_index()
    daily.columns = ['ds', 'y']

    # Model AI forecasting
    model = Prophet(seasonality_mode='multiplicative')
    model.fit(daily)

    # Buat prediksi 90 hari
    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)

    # Plot hasil
    fig = model.plot(forecast)
    fig.savefig('forecast.png')
else:
    print("Kolom 'amount' tidak ditemukan dalam data.")
