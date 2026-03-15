import requests
from bs4 import BeautifulSoup
import csv
import re
import urllib.parse

# Fields in the order of the CSV
fields = [
    'title', 'alternate_title', 'internal_ref_number', 'key', 'composition_year',
    'first_performance_year', 'avg_duration', 'composer_time_period', 'piece_style', 'instrumentation'
]

# Mapping from table header text to field name
header_to_field = {
    'Work Title': 'title',
    'Alternative Title': 'alternate_title',
    'Internal Reference Number': 'internal_ref_number',
    'Key': 'key',
    'Year/Date of Composition': 'composition_year',
    'First Performance': 'first_performance_year',
    'Average Duration': 'avg_duration',
    'Composer Time Period': 'composer_time_period',
    'Piece Style': 'piece_style',
    'Instrumentation': 'instrumentation'
}

def clean_text(text):
    """Clean text by removing extra whitespace and newlines."""
    return re.sub(r'\s+', ' ', text).strip()

def parse_table_to_dict(table):
    """Parse the work info table into a dictionary."""
    data = {}
    rows = table.find_all('tr')
    for row in rows:
        th = row.find('th')
        td = row.find('td')
        if th and td:
            header_text = clean_text(th.get_text())
            value_text = clean_text(td.get_text())
            # Map the header text to field
            field = None
            if 'Work Title' in header_text:
                field = 'title'
            elif 'Alternative' in header_text and 'Title' in header_text:
                field = 'alternate_title'
            elif 'Internal' in header_text and 'Reference' in header_text:
                field = 'internal_ref_number'
            elif header_text.strip() == 'Key':
                field = 'key'
            elif 'Year/Date of Composition' in header_text:
                field = 'composition_year'
            elif 'First Performance' in header_text:
                field = 'first_performance_year'
            elif 'Average Duration' in header_text:
                field = 'avg_duration'
            elif 'Composer Time Period' in header_text:
                field = 'composer_time_period'
            elif header_text.strip() == 'Piece Style':
                field = 'piece_style'
            elif header_text.strip() == 'Instrumentation':
                field = 'instrumentation'
            if field:
                data[field] = value_text
    return data


def scrape_piece(url):
    """Scrape data for a single piece."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the work info table
    tables = soup.find_all('table', {'border': '0'})
    table = None
    for t in tables:
        if t.find('th', string=re.compile(r'Work Title', re.IGNORECASE)):
            table = t
            break
    if not table:
        print("No work info table found")
        return None
    data = parse_table_to_dict(table)
    # Convert types
    for field in fields:
        data[field] = convert_value(field, data.get(field))
    return data

def main():
    category_url = 'https://imslp.org/wiki/Category:Mart%C3%ADnez_Garc%C3%ADa,_Salvador'
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', class_='categorypagelink')
    # Filter to only composition links
    composition_links = []
    for link in links:
        href = link.get('href', '')
        unquoted_href = urllib.parse.unquote(href)
        if 'Martínez_García,_Salvador' in unquoted_href:
            composition_links.append(link)
    piece_urls = []
    for link in composition_links:
        href = link['href']
        if href.startswith('http'):
            piece_urls.append(href)
        else:
            piece_urls.append('https://imslp.org' + href)
    print(f"Found {len(piece_urls)} piece URLs")
    with open('compositions.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        for url in piece_urls:
            print(f"Scraping {url}")
            data = scrape_piece(url)
            if data:
                writer.writerow(data)
                print(f"Added data for {data.get('title', 'Unknown')}")
            else:
                print(f"Failed to scrape {url}")

if __name__ == '__main__':
    main()