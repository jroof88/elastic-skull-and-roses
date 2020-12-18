from bs4 import BeautifulSoup
import requests
import re


class DeadShow:
    def __init__(self, month_day, year, venue, details_url):
        month = month_day.split(" ")[0]
        day = month_day.split(" ")[1]
        self.day = day
        self.month = month
        self.year = year
        self.venue = venue
        self.details_url = details_url

    def __str__(self):
        return f"{self.month} {self.day}, {self.year} -- {self.venue} -- {self.details_url}"


def get_dead_shows():
    dead_shows = []
    page_max = 20
    for page_num in range(0, page_max):
        print(f"Getting dead shows from Page {page_num} of {page_max}")
        dead_shows.extend(get_shows_from_page(page_num))

    for show in dead_shows:
        print(show)


def get_shows_from_page(page_num: int) -> []:
    dead_shows = []
    page = requests.get(f"https://www.dead.net/archives?field_show_date_value=&field_show_date_value_1=&title=&sort_by=field_show_date_value&sort_order=ASC&page={page_num}")
    soup = BeautifulSoup(page.content, 'html.parser')
    month_days_raw = soup.find_all("div", {"class": "month_date"})
    month_days = [x.contents[0] for x in month_days_raw]
    years_raw = soup.find_all("div", {"class": "year"})
    years = [x.contents[0] for x in years_raw]
    locations_raw = soup.find_all("a", {"href": re.compile("/show/"), "class": None, "hreflang": None})
    locations = [x.contents[0] for x in locations_raw]
    hrefs = [x["href"] for x in locations_raw]
    for month_day, year, location, href in zip(month_days, years, locations, hrefs):
        dead_show = DeadShow(month_day, year, location, href)
        dead_shows.append(dead_show)

    return dead_shows


if __name__ == '__main__':
    get_dead_shows()
