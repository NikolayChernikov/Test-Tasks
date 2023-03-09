import requests
import time
from bs4 import BeautifulSoup
from database import DataBase


class Parser(DataBase):
    def __init__(self):
        self.db = DataBase()
        super().__init__()
        self.last_page = 0

    def parse_page(self, page):
        URL = f"https://codeforces.com/problemset/page/{page}?order=BY_SOLVED_DESC&locale=ru"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('div', 'datatable')
        table_body = table.find('table')
        rows = table_body.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if cols:
                name_theme = cols[1]
                name_theme = name_theme.replace("\r", "")
                name_theme = list(filter(None, name_theme.split("\n")))
                for i in range(len(name_theme)):
                    name_theme[i] = " ".join(name_theme[i].split())
                name = name_theme[0]
                del name_theme[0]
                themes = " ".join(name_theme)
                self.db.add_parsed_page(cols[0], name, themes, cols[3], cols[4])

    def find_last_page(self):
        page = requests.get("https://codeforces.com/problemset/")
        soup = BeautifulSoup(page.content, 'html.parser')
        soup = soup.find_all("a", href=True)
        pages = []
        for x in soup:
            if "/problemset/page/" in str(x):
                pages.append(x)
        self.last_page = int(pages[-2].getText())

    def start_parser(self):
        self.find_last_page()
        for page in range(self.last_page):
            page += 1
            self.parse_page(page)


if __name__ == "__main__":
    while True:
        d = DataBase()
        print("Database connection")
        p = Parser()
        p.start_parser()
        print("Codeforce parsed")
        d.con.close()
        time.sleep(3600)
