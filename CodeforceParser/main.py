import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.last_page = 0

    @staticmethod
    def parse_page(page):
        page = requests.get(f"https://codeforces.com/problemset/page/1?order=BY_SOLVED_DESC")
        soup = BeautifulSoup(page.text, 'lxml')
        result = soup.find("body").find("table").find_all("tr")
        for i in range(len(result)):
            print(next(result[i].stripped_strings))

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
        self.last_page = 1
        for page in range(self.last_page):
            page += 1
            self.parse_page(page)


a = Parser()
a.start_parser()
