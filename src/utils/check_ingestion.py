# import pandas as pd

# # Load datasets
# imf = pd.read_csv("data/raw/imf_commodity_price.csv")
# wb = pd.read_csv("data/raw/worldbank_inflation.csv")
# oecd = pd.read_csv("data/raw/oecd_wages.csv")

# # Print shapes & sample rows
# print("IMF:", imf.shape)
# print(imf.head(3))
# print("\nWorld Bank:", wb.shape)
# print(wb.head(3))
# print("\nOECD:", oecd.shape)
# print(oecd.head(3))

import pandas as pd
import os

raw_path = "data/raw/"

for file in ["imf_prices.csv", "worldbank_inflation.csv", "oecd_wages.csv"]:
    file_path = os.path.join(raw_path, file)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(f"\n📊 {file}: {df.shape} rows x columns")
        print(df.head(3))
    else:
        print(f"⚠️ {file} not found in data/raw/")
