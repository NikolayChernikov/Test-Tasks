import requests
import psycopg2
import time
from bs4 import BeautifulSoup


class DataBase:
    def __init__(self):
        self.con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="1234",
            host="127.0.0.1",
            port="5432"
        )
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS codeforseparser  
             (ID TEXT UNIQUE,
             NAME TEXT,
             THEMES TEXT,
             LEVEL TEXT,
             SOLVED TEXT
             );''')


class Parser(DataBase):
    def __init__(self):
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
                self.cur.execute(
                    "INSERT INTO codeforseparser (ID, NAME,THEMES,LEVEL,SOLVED) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (ID) DO NOTHING",
                    (cols[0], name, themes, cols[3], cols[4]))
                self.con.commit()

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
        d.create_table()
        print("Table create or exist")
        a = Parser()
        a.start_parser()
        print("Value update")
        d.con.close()
        time.sleep(3600)
