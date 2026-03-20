import pandas as pd
from database import engine, SessionLocal
from models import Base, Bank, Branch

Base.metadata.create_all(bind=engine)

df = pd.read_csv("bank_branches.csv")  # adjust filename

db = SessionLocal()

banks_map = {}

for _, row in df.iterrows():
    bank_name = row['bank_name']

    if bank_name not in banks_map:
        bank = Bank(name=bank_name)
        db.add(bank)
        db.commit()
        db.refresh(bank)
        banks_map[bank_name] = bank.id

    branch = Branch(
        ifsc=row['ifsc'],
        branch=row['branch'],
        address=row['address'],
        city=row['city'],
        district=row['district'],
        state=row['state'],
        bank_id=banks_map[bank_name]
    )

    existing = db.query(Branch).filter(Branch.ifsc == row['ifsc']).first()

    if not existing:
        db.add(branch)

db.commit()
db.close()