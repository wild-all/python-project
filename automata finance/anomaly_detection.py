# File: anomaly_detection.py
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlite3
import re  # untuk regex

# Inisialisasi dataframe
df = pd.DataFrame()  # <- ini sumber 'df'

# Ambil data dari database
def load_data():
    conn = sqlite3.connect('finance.db')
    return pd.read_sql('SELECT * FROM transactions', conn)

df = load_data()  # <- inisialisasi df

# Siapkan data
df['amount_log'] = np.log(df['amount'])  # Perbaiki di sini
df['day_of_month'] = pd.to_datetime(df['date']).dt.day  # Pastikan 'date' ada di df
features = df[['amount_log', 'day_of_month']]

# Train model
clf = IsolationForest(contamination=0.05)
df['anomaly'] = clf.fit_predict(features)

# Visualisasi
plt.scatter(df['date'], df['amount'], c=df['anomaly'], cmap='viridis')
plt.title('Deteksi Transaksi Tidak Normal')
plt.savefig('anomalies.png')
plt.show()  # Menampilkan plot
