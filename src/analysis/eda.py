import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -------------------------------------------------------------------
# Load merged dataset
# -------------------------------------------------------------------

def load_data():
    file_path = "data/processed/cleaned_global_data.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"cleaned_global_data.csv not found at: {file_path}")

    print("📂 Loading merged dataset...")
    df = pd.read_csv(file_path)

    # Convert date column to datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df


# -------------------------------------------------------------------
# Summary statistics
# -------------------------------------------------------------------

def basic_summary(df):
    print("\n📊 BASIC SUMMARY")
    print(df.describe(include="all"))

    print("\n🔍 Missing Values:")
    print(df.isna().sum())


# -------------------------------------------------------------------
# Correlation Analysis
# -------------------------------------------------------------------

def correlation_analysis(df):
    numeric_df = df.select_dtypes(include=["float64", "int64"])

    print("\n📈 Correlation Matrix:")
    print(numeric_df.corr())

    plt.figure(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()

    output_path = "reports/figures/correlation_heatmap.png"
    os.makedirs("reports/figures", exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    print(f"✅ Correlation heatmap saved to {output_path}")


# -------------------------------------------------------------------
# Trend Plot for each variable
# -------------------------------------------------------------------

def plot_time_series(df):

    variables = ["inflation_rate", "gdp_per_capita", "wage_index"]

    for var in variables:
        if var not in df.columns:
            print(f"⚠️ Skipping {var} (not found in dataset)")
            continue

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x="date", y=var, hue="iso3")

        plt.title(f"{var.replace('_', ' ').title()} Over Time")
        plt.tight_layout()

        output_path = f"reports/figures/{var}_trend.png"
        plt.savefig(output_path)
        plt.close()

        print(f"📈 Saved {var} trend plot → {output_path}")


# -------------------------------------------------------------------
# GDP vs Inflation scatter
# -------------------------------------------------------------------

def scatter_gdp_inflation(df):
    if "gdp_per_capita" not in df.columns or "inflation_rate" not in df.columns:
        print("⚠️ No data available for GDP vs Inflation scatter plot.")
        return

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="gdp_per_capita", y="inflation_rate", hue="iso3")

    plt.title("GDP per Capita vs Inflation Rate")
    plt.tight_layout()

    output_path = "reports/figures/gdp_vs_inflation.png"
    plt.savefig(output_path)
    plt.close()

    print(f"📉 GDP vs Inflation scatter saved to {output_path}")


# -------------------------------------------------------------------
# Main runner
# -------------------------------------------------------------------

def run_eda():
    df = load_data()

    basic_summary(df)
    correlation_analysis(df)
    plot_time_series(df)
    scatter_gdp_inflation(df)

    print("\n🎉 PHASE 4 COMPLETED: All EDA outputs generated in reports/figures/")


if __name__ == "__main__":
    run_eda()
