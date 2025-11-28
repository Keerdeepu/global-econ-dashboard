import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

IMF_FILE = RAW_DIR / "imf_commodity_prices.csv"

def ingest_imf():
    # Read file in raw mode (no delimiter parsing)
    with open(IMF_FILE, "r", encoding="ISO-8859-1") as f:
        lines = f.readlines()

    print("Preview of raw file (first 10 lines):")
    for l in lines[:10]:
        print(l.strip())

    # Try flexible CSV reading (handles inconsistent delimiters)
    try:
        df = pd.read_csv(IMF_FILE, encoding="ISO-8859-1", on_bad_lines="skip")
    except Exception:
        df = pd.read_csv(IMF_FILE, sep=";", encoding="ISO-8859-1", on_bad_lines="skip")

    # Drop empty columns
    df = df.dropna(axis=1, how="all")

    # Drop empty rows
    df = df.dropna(how="all")

    # Save cleaned version
    out_file = RAW_DIR / "imf_commodity_prices_clean.csv"
    df.to_csv(out_file, index=False)
    print(f"\n✅ Cleaned IMF data saved → {out_file}")
    print(df.head())

if __name__ == "__main__":
    ingest_imf()
