"""Scrape the 2024-25 English Premier League final table into a CSV."""
import csv
import re
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://www.rsssf.org/tablese/eng2025.html"
OUTPUT = Path(__file__).with_name("premier_league_2024_25_standings.csv")

# RSSSF displays this table as preformatted text. Selenium loads the page,
# and Beautiful Soup locates the block that contains the final standings.
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1440,1200")

driver = webdriver.Chrome(options=options)
try:
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")
finally:
    driver.quit()

blocks = soup.find_all("pre")
if not blocks:
    raise RuntimeError("No preformatted text found. The source page may have changed.")

# The source page can place the Premier League table in a pre block with
# the remainder of the season results. Locate the first Final Table section.
page_text = "\n".join(block.get_text("\n") for block in blocks)
start = page_text.find("Final Table:")
if start == -1:
    raise RuntimeError("Could not find 'Final Table:' on the source page.")
section = page_text[start:]
round_start = section.find("Round 1")
if round_start != -1:
    section = section[:round_start]

# Rows are formatted as: position, club, played, won, drawn, lost,
# goals-for/goals-against, points. Ignore separator lines and headings.
row_pattern = re.compile(
    r"^\s*(\d+)\.(.*?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+"
    r"(\d+)\s*-\s*(\d+)\s+(\d+)\b"
)
rows = []
for line in section.splitlines():
    match = row_pattern.match(line)
    if not match:
        continue
    position, club, played, won, drawn, lost, goals_for, goals_against, points = match.groups()
    position = int(position)
    gf, ga = int(goals_for), int(goals_against)
    status = "Champions" if position == 1 else "Relegated" if position >= 18 else ""
    rows.append({
        "season": "2024-25",
        "league": "English Premier League",
        "position": position,
        "club": club.strip(),
        "played": int(played),
        "won": int(won),
        "drawn": int(drawn),
        "lost": int(lost),
        "goals_for": gf,
        "goals_against": ga,
        "goal_difference": gf - ga,
        "points": int(points),
        "status": status,
        "source_url": URL,
    })

if len(rows) != 20:
    raise RuntimeError(f"Expected 20 clubs, parsed {len(rows)}. Check the source page format.")

with OUTPUT.open("w", newline="", encoding="utf-8-sig") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Created {OUTPUT} with {len(rows)} clubs.")
