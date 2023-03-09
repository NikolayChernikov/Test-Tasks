import psycopg2
from config import Config


class DataBase:
    def __init__(self):
        self.config = Config()
        self.con = psycopg2.connect(
            database=str(self.config["DB"]["database"]),
            user=str(self.config["DB"]["user"]),
            password=str(self.config["DB"]["password"]),
            host=str(self.config["DB"]["host"]),
            port=str(self.config["DB"]["port"])
        )
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS codeforseparser  
                     (ID TEXT UNIQUE,
                     NAME TEXT,
                     THEMES TEXT,
                     LEVEL TEXT,
                     SOLVED TEXT,
                     LABEL TEXT
                     );''')
        self.con.commit()

    def add_parsed_page(self, our_id, name, themes, level, solved,label):
        self.cur.execute(
            "INSERT INTO codeforseparser (ID, NAME,THEMES,LEVEL,SOLVED, LABEL) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (ID) DO "
            "NOTHING",
            (our_id, name, themes, level, solved,label))
        self.con.commit()

    def find_by_id(self, a):
        self.cur.execute('''SELECT ID,NAME,THEMES,LEVEL,SOLVED FROM codeforseparser WHERE id = %s;''', (a,))
        self.con.commit()
        value = self.cur.fetchall()
        return value

    def find_by_difficulty_theme(self, dif, theme):
        self.cur.execute(f'''SELECT ID,NAME,THEMES,LEVEL,SOLVED FROM codeforseparser WHERE level = '{str(dif)}' AND label LIKE '%{str(theme)}%' LIMIT 10;
''')
        value = self.cur.fetchall()
        print(value)
        return value
