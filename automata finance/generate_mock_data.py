# File: generate_mock_data.py
import pandas as pd
import numpy as np

dates = pd.date_range('2023-01-01', '2023-12-31')
data = {
    'date': np.random.choice(dates, 200),
    'amount': np.random.lognormal(mean=3, sigma=1, size=200),
    'description': ['Pembayaran ' + x for x in np.random.choice(['listrik', 'gaji', 'vendor', 'pajak'], 200)]
}

pd.DataFrame(data).to_excel('keuangan.xlsx', index=False)