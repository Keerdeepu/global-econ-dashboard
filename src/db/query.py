import pandas as pd
from sqlalchemy import text
from src.db.config import engine

def load_all_data():
    query = text("SELECT * FROM macro_data")
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def load_countries():
    query = text("SELECT DISTINCT iso3 FROM macro_data ORDER BY iso3")
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df['iso3'].tolist()

def load_years():
    query = text("SELECT DISTINCT EXTRACT(YEAR FROM date) AS year FROM macro_data ORDER BY year")
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df['year'].tolist()
