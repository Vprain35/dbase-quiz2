# dbase-quiz2

This project contains a database of compositions by Salvador Martínez García.

## Populating the Compositions CSV

To populate `compositions.csv` with data from IMSLP:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the scraper:
   ```
   python scrape.py
   ```

This will fetch data for all compositions listed in the IMSLP category and append them to the CSV file.

## Populating the Sheet Music CSV

To populate `sheet_music.csv` with scan data:

```
python scrape_scans.py
```

This will scrape scan information for each composition and append to the CSV.

## Models

The `models.py` file defines the SQLModel classes for the database.