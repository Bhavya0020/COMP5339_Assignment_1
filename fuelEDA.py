import pandas as pd
import numpy as np


df = pd.read_csv("/Users/bhavyadhingra/Desktop/USYD_Study/SEM_3/Data Engineering/COMP5339_Assignment_1/cleaned_fuelcheck_data.csv")


print(df.columns)

print(df["Brand"].unique())