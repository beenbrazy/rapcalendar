import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime

# URL source
URL = "https://hiphopdx.com/new-hip-hop-albums"

def scrape_hiphopdx():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    albums = []
    for card in soup.find_all("div", class_="card card--horizontal release-date-card"):
        title_tag = card.find("h3", class_="card__title")
        date_tag = card.find("span", class_="card__date")

        if not title_tag or not date_tag:
            continue

        title = title_tag.get_text(strip=True)
        date_str = date_tag.get_text(strip=True)

        try:
            date = datetime.strptime(date_str, "%B %d, %Y")
            albums.append({"title": title, "date": date})
        except:
            continue

    return albums

def create_ics(albums, output_file="rap_album_releases.ics"):
    calendar = Calendar()
    for album in albums:
        event = Event()
        event.name = album["title"]
        event.begin = album["date"]
        event.make_all_day()
        calendar.events.add(event)

    with open(output_file, "w") as f:
        f.writelines(calendar)

    print(f"ICS file saved to {output_file}")

# Main logic
if __name__ == "__main__":
    albums = scrape_hiphopdx()
    create_ics(albums)
