"""
PHASE 3 - CLEAN AND MERGE ECONOMIC DATA
---------------------------------------

This script:
- Loads raw data (World Bank, IMF, OECD)
- Cleans column formats
- Converts country names to ISO3
- Standardizes numeric formats
- Normalizes date formats
- Merges datasets
- Saves cleaned output to data/processed/

"""

import pandas as pd
import pycountry
import os

RAW_DIR = "data/raw/"
PROCESSED_DIR = "data/processed/"

# -------------------------------------------------------------------------------------
# Helper: Convert country names → ISO3
# -------------------------------------------------------------------------------------

def to_iso3(country_name):
    if pd.isna(country_name):
        return None
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except:
        return None

# -------------------------------------------------------------------------------------
# Load Raw Data
# -------------------------------------------------------------------------------------

def load_data():
    inflation_path = os.path.join(RAW_DIR, "worldbank_inflation.csv")
    imf_path = os.path.join(RAW_DIR, "imf_commodity_price.csv")
    oecd_path = os.path.join(RAW_DIR, "oecd_wages.csv")

    print("📥 Loading raw data...")

    inflation = pd.read_csv(inflation_path)
    imf = pd.read_csv(imf_path)
    wages = pd.read_csv(oecd_path)

    print("✔ Loaded World Bank Inflation:", inflation.shape)
    print("✔ Loaded IMF Commodities:    ", imf.shape)
    print("✔ Loaded OECD Wages:         ", wages.shape)

    return inflation, imf, wages

# -------------------------------------------------------------------------------------
# Clean World Bank Inflation
# -------------------------------------------------------------------------------------

def clean_inflation(df):
    print("🔧 Cleaning World Bank dataset...")

    # Expected columns: country, year, inflation_rate
    df.rename(columns={
        "country": "country",
        "year": "year",
        "inflation_rate": "inflation_rate"
    }, inplace=True)

    # Convert "7.4%" → 7.4
    df["inflation_rate"] = (
        df["inflation_rate"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", "", regex=False)
    )

    df["inflation_rate"] = pd.to_numeric(df["inflation_rate"], errors="coerce")

    # Convert year to datetime
    df["date"] = pd.to_datetime(df["year"].astype(str) + "-01-01", errors="coerce")

    # Convert country to ISO3
    df["iso3"] = df["country"].apply(to_iso3)

    return df[["iso3", "date", "inflation_rate"]]

# -------------------------------------------------------------------------------------
# Clean IMF Commodity Data (GLOBAL — no country column)
# -------------------------------------------------------------------------------------

def clean_imf(df):
    print("🔧 Cleaning IMF dataset...")

    # Rename Date column only
    df.rename(columns={"Date": "date"}, inplace=True)

    # IMF file DOES NOT contain country or price columns
    # Select one global index → All Commodity Price Index
    if "All Commodity Price Index" not in df.columns:
        raise KeyError("Missing 'All Commodity Price Index' column in IMF data.")

    df["commodity_price"] = pd.to_numeric(
        df["All Commodity Price Index"]
        .astype(str)
        .str.replace(r"[^0-9.]", "", regex=True),
        errors="coerce"
    )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Global dataset — no ISO
    df["iso3"] = None

    return df[["iso3", "date", "commodity_price"]]

# -------------------------------------------------------------------------------------
# Clean OECD Wages
# -------------------------------------------------------------------------------------

def clean_wages(df):
    print("🔧 Cleaning OECD wages dataset...")

    # Rename relevant columns
    df.rename(columns={
        "REF_AREA": "country",
        "TIME_PERIOD": "year",
        "OBS_VALUE": "wage_index"
    }, inplace=True)

    # Convert wage index to numeric
    df["wage_index"] = pd.to_numeric(
        df["wage_index"].astype(str).str.replace(r"[^0-9.]", "", regex=True),
        errors="coerce"
    )

    # Convert year → datetime
    df["date"] = pd.to_datetime(df["year"].astype(str) + "-01-01", errors="coerce")

    # Convert country → ISO3
    df["iso3"] = df["country"].apply(to_iso3)

    return df[["iso3", "date", "wage_index"]]


# -------------------------------------------------------------------------------------
# Merge All Datasets
# -------------------------------------------------------------------------------------

def merge_data(inflation, imf, wages):
    print("🔗 Merging datasets...")

    # Merge inflation + wages by country
    merged = inflation.merge(wages, on=["iso3", "date"], how="left")

    # Merge IMF GLOBAL dataset by date only
    merged = merged.merge(imf[["date", "commodity_price"]], on="date", how="left")

    merged = merged.drop_duplicates()

    # Keep countries with enough observations
    merged = merged.groupby("iso3").filter(lambda x: len(x) > 3)

    return merged

# -------------------------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------------------------

def main():
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    inflation, imf, wages = load_data()

    inflation_clean = clean_inflation(inflation)
    imf_clean = clean_imf(imf)
    wages_clean = clean_wages(wages)

    merged = merge_data(inflation_clean, imf_clean, wages_clean)

    output_path = os.path.join(PROCESSED_DIR, "cleaned_global_data.csv")
    merged.to_csv(output_path, index=False)

    print("\n🎉 DONE! Cleaned dataset saved to:")
    print(output_path)
    print("\nFinal shape:", merged.shape)

# -------------------------------------------------------------------------------------
# Run Script
# -------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
