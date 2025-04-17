import pandas as pd

data = pd.read_csv(
    "/Users/bhavyadhingra/Desktop/USYD_Study/SEM_3/Data Engineering/COMP5339_Assignment_1/data/processed_data.csv"
)

print(data.head(10))

df = data.head(10)

df.to_csv("data/sample.csv", index=False)
