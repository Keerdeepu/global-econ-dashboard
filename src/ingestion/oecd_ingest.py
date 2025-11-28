import requests
import pandas as pd
from pathlib import Path

OUT_DIR = Path("data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = Path("data/raw")

OECD_FILE = Path("infra/data_sources/oecd_wages.csv")  # local file

def ingest_oecd():
    df = pd.read_csv(OECD_FILE)
    print(df.head())
    out_file = RAW_DIR/"oecd_wages.csv"
    df.to_csv(out_file, index=False)
    print(f"✅ Saved OECD wage data → {out_file}")

if __name__ == "__main__":
    ingest_oecd()

