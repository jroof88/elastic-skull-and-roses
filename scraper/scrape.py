from bs4 import BeautifulSoup
import requests


class DeadShow:
    def __init__(self, month_day, year, location):
        month = month_day.split(" ")[0]
        day = month_day.split(" ")[1]
        self.day = day
        self.month = month
        self.year = year
        self.location = location

    def __str__(self):
        return f"{self.month} {self.day}, {self.year} -- {self.location}"


def get_dead_shows():
    dead_shows = []
    for i in range(0, 10):
        dead_shows.extend(get_shows_from_page(i))

    for show in dead_shows:
        print(show)


def get_shows_from_page(page_num: int) -> []:
    print(f"Getting dead shows from page {page_num}")
    dead_shows = []
    page = requests.get(f"https://www.dead.net/archives?field_show_date_value=&field_show_date_value_1=&title=&sort_by=field_show_date_value&sort_order=ASC&page={page_num}")
    soup = BeautifulSoup(page.content, 'html.parser')
    month_day = soup.find_all("div", {"class": "month_date"})
    year = soup.find_all("div", {"class": "year"})
    for month_day, year in zip(month_day, year):
        dead_show = DeadShow(month_day.contents[0], year.contents[0], "")
        dead_shows.append(dead_show)

    print(len(dead_shows))
    return dead_shows


if __name__ == '__main__':
    get_dead_shows()
