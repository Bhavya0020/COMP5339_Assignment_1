import pandas as pd

data = pd.read_csv(
    "/processed_data.csv"
)
print(data.head(10))
df = data.head(10)

df.to_csv("data/sample.csv", index=False)
