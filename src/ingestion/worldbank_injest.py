# src/ingestion/worldbank_ingestion.py
import requests
import pandas as pd
import os

def fetch_worldbank_inflation():
    """Fetch global inflation data from World Bank API and save to data/raw/."""
    print("🌍 Fetching inflation data from World Bank API...")

    # World Bank API endpoint for inflation (% change in CPI)
    url = "http://api.worldbank.org/v2/country/all/indicator/FP.CPI.TOTL.ZG?format=json&per_page=20000"

    try:
        # sends a GET request to an endpoint
        response = requests.get(url)
        # Raises an error if HTTP status is not successful(Ex: 404, 500).
        response.raise_for_status()
        # Takes the json request and selects the second element, which contains the data list.
        data = response.json()[1]

        # Convert JSON to Pandas DataFrame
        df = pd.json_normalize(data)
        # Selects only the relevent columns from the raw data
        df = df[["country.id", "country.value", "date", "value"]]
        # Rename columns to clearer names
        df.columns = ["country_code", "country", "year", "inflation_rate"]

        # Clean data
        # removes the row where the inflation_rate is missing
        df = df.dropna(subset=["inflation_rate"])
        # Converts the year column from string to integer
        df["year"] = df["year"].astype(int)
        # Converts the infalation_rate from string to float
        df["inflation_rate"] = df["inflation_rate"].astype(float)

        # Ensure output folder exists.....If not creates the file.
        os.makedirs("data/raw", exist_ok=True)

        # Save to CSV
        # Sets the path for the output file
        output_path = "data/raw/worldbank_inflation.csv"
        # Saves the cleaned dataframe as a csv file without including the index column.
        df.to_csv(output_path, index=False)
        print(f"✅ Inflation data saved to: {output_path}")
        print(f"📊 Total records: {len(df)}")

    except Exception as e:
        print(f"❌ Error fetching World Bank data: {e}")


if __name__ == "__main__":
    fetch_worldbank_inflation()
