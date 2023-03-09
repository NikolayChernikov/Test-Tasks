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
                a = cols[1]
                a = a.replace("\r", "")
                a = list(filter(None, a.split("\n")))
                for i in range(len(a)):
                    a[i] = " ".join(a[i].split())
                name = a[0]
                del a[0]
                themes = " ".join(a)
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
        a = Parser()
        a.start_parser()
        print("Codeforce parsed")
        d.con.close()
        time.sleep(3600)
