import pandas as pd

df = pd.read_csv("/Users/bhavyadhingra/Desktop/USYD_Study/SEM_3/Data Engineering/COMP5339_Assignment_1/cleaned_fuelcheck_data.csv")

print(df['FuelCode'].unique())