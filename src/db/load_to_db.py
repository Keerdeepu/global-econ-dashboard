import pandas as pd
from sqlalchemy.orm import Session
from src.db.config import engine, SessionLocal
from src.db.models import Base, MacroData

def create_tables():
    print("📦 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✔ Tables created successfully!")

def load_csv_to_db():
    file_path = "data/processed/cleaned_global_data.csv"
    print(f"📥 Loading CSV: {file_path}")

    df = pd.read_csv(file_path)

    # Convert date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    print("📤 Inserting rows into database...")

    session = SessionLocal()

    try:
        for _, row in df.iterrows():
            entry = MacroData(
                iso3=row["iso3"],
                date=row["date"],
                inflation_rate=row.get("inflation_rate"),
                wage_index=row.get("wage_index"),
                commodity_price=row.get("commodity_price")
            )
            session.add(entry)

        session.commit()
        print("✅ All data inserted successfully!")

    except Exception as e:
        session.rollback()
        print("❌ Error inserting data:", e)

    finally:
        session.close()

def main():
    create_tables()
    load_csv_to_db()

if __name__ == "__main__":
    main()
