import random
import string

from bs4 import BeautifulSoup
import pymysql
import requests
import user_agent
import json
from tomorrow3 import threads
from pymysql import connect
from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql, 10, host="127.0.0.1", user="test", passwd="", db="wenben_book", port=8889)
con = connect("localhost", "test", "", "wenben_book", 8889)


def generate_headers():
    return {"user-agent": user_agent.generate_user_agent()}


def generate_cookie():
    return {"bid": "".join(random.sample(string.ascii_letters + string.digits, 11))}


def exesql(con: con, sql: str):
    cur = con.cursor()
    cur.execute(sql)
    cur.close()


def getproxy():
    a = json.loads(requests.get("54.190.145.159:8000").text)
    return a



@threads(10)
def get_bs(url: str, headers: dict, cookie: dict):
    bs = BeautifulSoup(requests.get(url, cookies=cookie, headers=headers).text, "html.parser")
    p = bs.find_all("script", type="application/ld+json")
    data = p[0].get_text()

    ul = json.loads(data, strict=False)["url"]
    exesql(con, f"insert into test values ('{ul}','{data}')")


for page in range(1, 10000):
    print(f"开始第{page}页")
    url = f"https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start={page * 20}&year_range=2017,2017"
    a = requests.get(url, cookies=generate_cookie(), headers=generate_headers())
    print(a.text)
    data = json.loads(a.text)
    for url in data["data"]:
        headers = {"user-agent": user_agent.generate_user_agent()}
        cookie = {"bid": "".join(random.sample(string.ascii_letters + string.digits, 11))}
        get_bs(url["url"], headers=headers, cookie=cookie)
