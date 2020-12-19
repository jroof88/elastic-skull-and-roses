from bs4 import BeautifulSoup
import requests
import re
import multiprocessing as mp
import json


class DeadShow:
    def __init__(self, month_day, year, venue, setlist):
        month = month_day.split(" ")[0]
        day = month_day.split(" ")[1]
        self.day = day
        self.month = month
        self.year = year.strip()
        self.venue = venue
        self.setlist = setlist

    def __str__(self):
        return f"{self.month}, {self.day}, {self.year}, {self.venue}, {self.details_url} \n"


def get_dead_shows():
    pool = mp.Pool(mp.cpu_count())
    for i in range(0, 500):
        pool.map_async(get_shows_from_page, (i,))
    pool.close()
    pool.join()


def get_shows_from_page(page_num) -> []:
    append_f = open("data/shows.txt", "a")
    print(f"Getting Dead Shows from Page {page_num}")
    page = requests.get(f"https://www.dead.net/archives?field_show_date_value=&field_show_date_value_1=&title=&sort_by=field_show_date_value&sort_order=ASC&page={page_num}")
    soup = BeautifulSoup(page.content, 'html.parser')
    month_days_raw = soup.find_all("div", {"class": "month_date"})
    month_days = [x.contents[0] for x in month_days_raw]
    years_raw = soup.find_all("div", {"class": "year"})
    years = [x.contents[0] for x in years_raw]
    locations_raw = soup.find_all("a", {"href": re.compile("/show/"), "class": None, "hreflang": None})
    locations = [x.contents[0] if x.contents[0] != "\n" else x.contents[1] for x in locations_raw]
    hrefs = [x["href"] for x in locations_raw]
    for month_day, year, location, href in zip(month_days, years, locations, hrefs):
        setlist = get_setlist_from_details_page(href)
        print(setlist)
        dead_show = DeadShow(month_day, year, location, setlist)
        append_f.write(f"{json.dumps(dead_show.__dict__)}\n")

    append_f.close()
    return


def get_setlist_from_details_page(details_url):
    details_page = requests.get(f"https://www.dead.net{details_url}")
    soup = BeautifulSoup(details_page.content, "html.parser")
    pres = soup.find_all("pre")
    if len(pres) == 0:
        return []
    return [item for idx, item in enumerate(pres[0].contents) if idx % 2 == 0]


if __name__ == '__main__':
    f = open("data/shows.txt", "w")
    f.close()
    get_dead_shows()
