import pandas as pd
import numpy as np


df = pd.read_csv("ProductSales - Sheet1.csv")

# Melt the DataFrame
df_long = pd.melt(df, 
                  id_vars=['Month'], 
                  var_name='Product', 
                  value_name='SalesValue')

# Clean and convert values to numeric
df_long['SalesValue'] = (
    df_long['SalesValue']
    .astype(str)
    .str.strip()  # remove whitespace
    .str.replace(',', '', regex=False)  # remove thousands separators
    .replace(
        to_replace=['n.a.', 'n.a', 'NA', 'NaN', '-', '--', ''],
        value=None
    )
)

# Convert to float
df_long['SalesValue'] = pd.to_numeric(df_long['SalesValue'], errors='coerce')

fuel_code_map = {
    'U91': 'Regular (<95 RON) (ML)',
    'P95': 'Premium (95-97 RON) (ML)',
    'P98': 'Premium (98+ RON) (ML)',
    'PDL': 'Diesel oil: premium diesel (ML)',
    'DL': 'Diesel oil: total (ML)',
    'E10': 'Ethanol-blended fuel (ML)',
    'E85': 'E85 (if exists, else custom)',
    'B20': 'B20 (if exists, else custom)',
    'LPG': 'LPG Automotive use (ML)',
}

# Keep only fuels in the mapping
valid_products = list(fuel_code_map.values())
df_filtered = df_long[df_long['Product'].isin(valid_products)].copy()

# Reverse the mapping to go from full name to code
reverse_map = {v: k for k, v in fuel_code_map.items()}

# Add FuelCode column
df_filtered['FuelCode'] = df_filtered['Product'].map(reverse_map)

# Impute missing SalesValue with the mean for each product
df_filtered['SalesValue'] = df_filtered.groupby('Product')['SalesValue'].transform(
    lambda x: x.fillna(x.mean())
)

# Save to CSV
df_filtered.to_csv('fuelcheck_monthly_files/fuel.csv', index=False)
