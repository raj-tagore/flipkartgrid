import pandas as pd

df = pd.read_csv("packagedata.csv")
print(df.head())
for i, j in zip(df['Induct Station'], df['Destination']):
