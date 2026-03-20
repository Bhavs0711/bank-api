from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all banks
@app.get("/banks")
def get_banks(
    search: str = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(models.Bank)

    if search:
        query = query.filter(models.Bank.name.ilike(f"%{search}%"))

    return query.offset(offset).limit(limit).all()

# Get branches of a bank
@app.get("/branches")
def get_branches(
    city: str = None,
    bank_name: str = None,
    ifsc: str = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(models.Branch).join(models.Bank)

    if city:
        query = query.filter(models.Branch.city.ilike(f"%{city}%"))

    if bank_name:
        query = query.filter(models.Bank.name.ilike(f"%{bank_name}%"))

    if ifsc:
        query = query.filter(models.Branch.ifsc == ifsc)

    return [
        {
            "ifsc": b.ifsc,
            "branch": b.branch,
            "city": b.city,
            "bank_name": db.query(models.Bank).filter(models.Bank.id == b.bank_id).first().name
        }
        for b in query.offset(offset).limit(limit).all()
    ]

# Get branch by IFSC
@app.get("/branches/{ifsc}")
def get_branch(ifsc: str, db: Session = Depends(get_db)):
    return db.query(models.Branch).filter(models.Branch.ifsc == ifsc).first()