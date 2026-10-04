# Premier League standings scraper

This small project uses Selenium to load the RSSSF 2024-25 England season page and Beautiful Soup to parse the final Premier League table. It writes a CSV file with one row per club.

## Requirements

- Python 3.9 or newer
- Google Chrome installed

Install the Python packages:

```bash
python -m pip install selenium beautifulsoup4
```

Recent Selenium versions use Selenium Manager to locate or download a compatible Chrome driver automatically.

## Run

From this folder, run:

```bash
python scrape_standings.py
```

The output `premier_league_2024_25_standings.csv` is saved beside the script. It includes position, club, match record, goals, goal difference, points, status, and the source URL.

Source page: https://www.rsssf.org/tablese/eng2025.html

The parser expects RSSSF's final table to remain in preformatted text and stops reading at `Round 1`. If the website changes its layout, the script raises an error instead of silently writing an incomplete CSV.
