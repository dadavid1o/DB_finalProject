from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Db

DATABASE_URL = "postgresql://arutunyandavid@localhost:5432/DB_finalProject"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Model

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    capital = Column(String, nullable=False)
    government_type = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# Schemas

class CountryCreate(BaseModel):
    name: str
    capital: str
    government_type: str

class CountryResponse(CountryCreate):
    id: int

# FastAPI app
app = FastAPI(title="DB Final Project – Geography")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/countries", response_model=CountryResponse)
def create_country(country: CountryCreate):
    db = SessionLocal()
    obj = Country(**country.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    db.close()
    return obj

@app.get("/countries", response_model=list[CountryResponse])
def get_countries(limit: int = 50, offset: int = 0):
    if limit < 1:
        limit = 1
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0

    db = SessionLocal()
    rows = db.query(Country).offset(offset).limit(limit).all()
    db.close()
    return rows

@app.get("/countries/{country_id}", response_model=CountryResponse)
def get_country(country_id: int):
    db = SessionLocal()
    obj = db.get(Country, country_id)
    db.close()
    if not obj:
        raise HTTPException(status_code=404, detail="Country not found")
    return obj

@app.put("/countries/{country_id}", response_model=CountryResponse)
def update_country(country_id: int, data: CountryCreate):
    db = SessionLocal()
    obj = db.get(Country, country_id)
    if not obj:
        db.close()
        raise HTTPException(status_code=404, detail="Country not found")

    obj.name = data.name
    obj.capital = data.capital
    obj.government_type = data.government_type

    db.commit()
    db.refresh(obj)
    db.close()
    return obj

@app.delete("/countries/{country_id}")
def delete_country(country_id: int):
    db = SessionLocal()
    obj = db.get(Country, country_id)
    if not obj:
        db.close()
        raise HTTPException(status_code=404, detail="Country not found")

    db.delete(obj)
    db.commit()
    db.close()
    return {"status": "deleted"}
