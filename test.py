import random
import string

from bs4 import BeautifulSoup
from proxy import Proxy
import pymysql
import requests
import random
import user_agent
import json
from tomorrow3 import threads
from pymysql import connect
from sqlite3 import connect as sqc

# pool = PooledDB(pymysql, 10, host="127.0.0.1", user="test", passwd="", db="wenben_book", port=8889)
con3 = connect("localhost", "root", "", "wenben_book", 3306)
# con3 = sqc("book.db")
proxy = Proxy()
try:
    con3.cursor().execute(
        "create table movie(url varchar(30) not null,data text null,constraint movie_pk primary key (url))")
except:
    pass


#
def get_proxy():
    pl = proxy.get_proxy()
    return [x for x in pl if x[2] >= 8]


def randList(ls: list):
    return random.choice(ls)


def delete_proxy(ip):
    proxy.delete_proxy(ip)


#


def generate_headers():
    return {"user-agent": user_agent.generate_user_agent()}


def generate_cookie():
    return {"bid": "".join(random.sample(string.ascii_letters + string.digits, 11))}


def exesql(con: con3, sql: str):
    con.ping(reconnect=True)
    cur = con.cursor()
    cur.execute(sql)
    cur.close()


print(get_proxy())

if __name__ == '__main__':
    proxies = get_proxy()


    @threads(15)
    def get_bs(url: str, headers: dict, cookie: dict):
        rp = random.choice(get_proxy())
        pro = {"http": f"http://{rp[0]}:{rp[1]}", "https": f"http://{rp[0]}:{rp[1]}"}
        p=5
        while p>0:
            try:
                delete_proxy(rp[0])
                rp = random.choice(get_proxy())
                pro = {"http": f"http://{rp[0]}:{rp[1]}", "https": f"http://{rp[0]}:{rp[1]}"}
                bs = BeautifulSoup(requests.get(url, cookies=cookie, headers=headers,proxies=pro).text, "html.parser")
                break
            except:
                p-=1
                continue

        p = bs.find_all("script", type="application/ld+json")
        data = p[0].get_text()
        data = data.decode("utf-8")
        ul = json.loads(data, strict=False)["url"]
        exesql(con3, f"insert into movie values ('{ul}','{data}')")


    for page in range(1, 10000):
        try:
            rp = random.choice(get_proxy())
            pro = {"http": f"http://{rp[0]}:{rp[1]}", "https": f"http://{rp[0]}:{rp[1]}"}
            print(f"开始第{page}页")
            url = f"https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start={page * 20}&year_range=2017,2017"

            a = requests.get(url, cookies=generate_cookie(), headers=generate_headers(), proxies=pro)
        except:
            p = 0
            while p < 3:
                try:
                    delete_proxy(rp[0])
                    rp = random.choice(get_proxy())
                    pro = {"http": f"http://{rp[0]}:{rp[1]}", "https": f"http://{rp[0]}:{rp[1]}"}
                    a = requests.get(url, cookies=generate_cookie(), headers=generate_headers(), proxies=pro)
                    break
                except:
                    p+=1
                    continue
            continue
        data = json.loads(a.text)
        for url in data["data"]:
            headers = {"user-agent": user_agent.generate_user_agent()}
            cookie = {"bid": "".join(random.sample(string.ascii_letters + string.digits, 11))}
            get_bs(url["url"], headers=headers, cookie=cookie)
