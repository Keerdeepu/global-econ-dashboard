from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MacroData(Base):
    __tablename__ = "macro_data"

    id = Column(Integer, primary_key=True, index=True)
    iso3 = Column(String, index=True)
    date = Column(Date, index=True)

    inflation_rate = Column(Float)
    wage_index = Column(Float)
    commodity_price = Column(Float)

