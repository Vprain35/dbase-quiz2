from sqlmodel import create_engine, Session, SQLModel
from models import scans
import csv

# Create engine for the database
engine = create_engine("sqlite:///SMG_Pieces.db")

# Create tables if they don't exist
SQLModel.metadata.create_all(engine)

# Read and insert data from sheet_music.csv
with Session(engine) as session:
    with open('sheet_music.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            scan = scans(
                piece_title=row['piece_title'],
                scan_type=row['scan_type'] or None,
                scan_id=int(row['scan_id']) if row['scan_id'] else None,
                page_count=int(row['page_count']) if row['page_count'] else None
            )
            session.merge(scan)
    session.commit()

print("Scans data inserted into SMG_Pieces.db")