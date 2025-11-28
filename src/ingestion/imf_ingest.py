# src/ingestion/imf_ingestion.py
# used to read the CSV into a DataFrame.
import pandas as pd
import os
#  defines a function with one parameter, file_path, which has a default value pointing to data/raw/imf_prices.csv.
def load_imf_csv(file_path="data/raw/imf_prices.csv"):
    # checks whether a file actually exists at that path.
    if os.path.exists(file_path):
        # reads the CSV file into a pandas DataFrame called df.
        df = pd.read_csv(file_path)
        print(f"✅ Loaded IMF data: {len(df)} rows")
        return df
    else:
        print("⚠️ IMF CSV not found. Please download manually first.")
        return None
