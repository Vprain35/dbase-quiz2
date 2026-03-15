import requests
from bs4 import BeautifulSoup
import csv
import re
import urllib.parse

def clean_text(text):
    """Clean text by removing extra whitespace and newlines."""
    return re.sub(r'\s+', ' ', text).strip()

def parse_scans(soup, piece_title):
    """Parse scan information from the page."""
    scans = []
    file_divs = soup.find_all('div', class_='we_file_download')
    for div in file_divs:
        scan_data = {'piece_title': piece_title}
        # Find the bold text for scan_type
        b = div.find('b')
        if b:
            scan_data['scan_type'] = clean_text(b.get_text())
        # Find the info span
        info_span = div.find('span', class_='we_file_info2')
        if info_span:
            text = clean_text(info_span.get_text())
            # Extract scan_id
            match = re.search(r'#(\d+)', text)
            if match:
                scan_data['scan_id'] = int(match.group(1))
            # Extract page_count
            match = re.search(r'(\d+)\s*pp', text)
            if match:
                scan_data['page_count'] = int(match.group(1))
        scans.append(scan_data)
    return scans

def scrape_scans(url):
    """Scrape scan data for a single piece."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None, []
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the work info table to get title
    tables = soup.find_all('table', {'border': '0'})
    table = None
    for t in tables:
        if t.find('th', string=re.compile(r'Work Title', re.IGNORECASE)):
            table = t
            break
    if not table:
        print("No work info table found")
        return None, []
    # Extract title
    title = None
    rows = table.find_all('tr')
    for row in rows:
        th = row.find('th')
        td = row.find('td')
        if th and td and 'Work Title' in clean_text(th.get_text()):
            title = clean_text(td.get_text())
            break
    if not title:
        return None, []
    scans = parse_scans(soup, title)
    return title, scans

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
    with open('sheet_music.csv', 'a', newline='', encoding='utf-8') as sheetfile:
        sheet_fields = ['piece_title', 'scan_type', 'scan_id', 'page_count']
        sheet_writer = csv.DictWriter(sheetfile, fieldnames=sheet_fields)
        for url in piece_urls:
            print(f"Scraping scans from {url}")
            title, scans = scrape_scans(url)
            if title:
                for scan in scans:
                    sheet_writer.writerow(scan)
                print(f"Added {len(scans)} scans for {title}")
            else:
                print(f"Failed to scrape {url}")

if __name__ == '__main__':
    main()