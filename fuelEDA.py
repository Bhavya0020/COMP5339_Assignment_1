import pandas as pd
import numpy as np

df = pd.read_csv("/cleaned_fuelcheck_data.csv")

print(df.columns)

print(df["Brand"].unique())