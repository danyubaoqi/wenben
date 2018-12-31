import requests
import re
import user_agent

from bs4 import BeautifulSoup
def generate_headers():
    return {"user-agent": user_agent.generate_user_agent()}

a=requests.session()
data={
    "source":None,
    "redir":"https://www.douban.com",
    "form_email":"18811523867@163.com",
    "form_password":"dybq19940419",
    "login":"登录"
}
b=a.post("https://accounts.douban.com/login",data=data,headers=generate_headers())

print(b.text)
