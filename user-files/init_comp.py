from sqlmodel import create_engine, Session, SQLModel
from models import composition
import csv

# Create engine for the database
engine = create_engine("sqlite:///SMG_Pieces.db")

# Create tables if they don't exist
SQLModel.metadata.create_all(engine)

# Read and insert data from compositions.csv
with Session(engine) as session:
    with open('compositions.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            comp = composition(
                title=row['title'],
                alternate_title=row['alternate_title'] or None,
                internal_ref_number=row['internal_ref_number'] or None,
                key=row['key'] or None,
                composition_year=int(row['composition_year']) if row['composition_year'] else None,
                first_performance_year=int(row['first_performance_year']) if row['first_performance_year'] else None,
                avg_duration=int(row['avg_duration']) if row['avg_duration'] else None,
                composer_time_period=row['composer_time_period'] or None,
                piece_style=row['piece_style'] or None,
                instrumentation=row['instrumentation'] or None
            )
            session.merge(comp)
    session.commit()

print("Compositions data inserted into SMG_Pieces.db")