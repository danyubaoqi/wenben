import random
import string
import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup
from proxy import Proxy
import pymysql
import requests
import random
import user_agent
import json
import time
import ssl
from tomorrow3 import threads
from pymysql import connect
from sqlite3 import connect as sqc
ses=requests.session()
# pool = PooledDB(pymysql, 10, host="127.0.0.1", user="test", passwd="", db="wenben_book", port=8889)
con3 = connect("localhost", "test", "", "wenben_book", 8889)
# con3 = sqc("book.db")
print("连接成功")
proxy = Proxy()
try:
    con3.cursor().execute(
        "create table movie2(url varchar(30) not null,data text null,constraint movie_pk primary key (url))")
except:
    pass


def generate_headers():
    return {"user-agent": user_agent.generate_user_agent()}


def generate_cookie():
    return {"bid": "".join(random.sample(string.ascii_letters + string.digits, 11))}


def exesql(con: con3, sql: str):
    con.ping(reconnect=True)
    cur = con.cursor()
    cur.execute(sql)
    cur.close()
    print("插入成功")


@threads(1)
def get_bs(url: str, headers: dict, cookie: dict):
    time.sleep(random.uniform(1,3))
    pro = {"http": "http://204.29.115.149:8080", "https": "http://204.29.115.149:8080"}
    # rp = random.choice(get_proxy())
    p = 5

    try:

        # rp = random.choice(get_proxy())
        # pro = {"http": f"http://{rp[0]}:{rp[1]}", "https": f"http://{rp[0]}:{rp[1]}"}
        bs = BeautifulSoup(ses.get(url, cookies=cookie, headers=headers).text,
                           "html.parser")
        p = bs.find_all("script", type="application/ld+json")
        data = p[0].get_text()
        ul = json.loads(data, strict=False)["url"]
        exesql(con3, f"insert into movie values ('{ul}','{data}')")

    except Exception as e:
        # delete_proxy(rp[0])
        print(e)
        pass



if __name__ == '__main__':
    ses.post("https://accounts.douban.com/login", data={
        "source": None,
        "redir": "https://www.douban.com",
        "form_email": "18811523867@163.com",
        "form_password": "dybq19940419",
        "login": "登录"
    }, headers=generate_headers())
    # proxies = get_proxy()

    for page in range(1, 10000):
        try:
            # rp = random.choice(get_proxy())
            # pro = {"http": f"http://{rp[0]}:{rp[1]}", "https": f"http://{rp[0]}:{rp[1]}"}
            print(f"开始第{page}页")
            url = f"https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start={page * 20}&year_range=2017,2017"

            a = ses.get(url, cookies=generate_cookie(), headers=generate_headers())
            data = json.loads(a.text)
            print(data)
            for url in data["data"]:
                headers = {"user-agent": user_agent.generate_user_agent()}
                cookie = {"bid": "".join(random.sample(string.ascii_letters + string.digits, 11))}
                get_bs(url["url"], headers=headers, cookie=cookie)
        except Exception as e:
            print(e)
            p = 0
            continue
