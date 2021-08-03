import requests
import re
from bs4 import BeautifulSoup

def get_current_version():
    url = 'https://iit.com.ua/downloads'
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        container = soup.find("div", {"class" : "container iit-container"})
        rows = container.findAll("div", {"class" : "row iit-row"})
        for row in rows:
            a = row.findAll("a")
            if len(a) > 1:
                name = str(a[1].contents[0])
                if re.search('CACertificates', name):
                    span = row.find("span")
                    tmp = span.text.split(" ")
                    if tmp[0] == "Розміщено":
                        date = reversed(tmp[1].split("/"))
                        time = tmp[2].split(":")
                        return "".join(date) + "".join(time)
    return False

def get_old_version():
    try:
        file = open('app/crontab/ver.txt', 'r')
        old = file.read()
        file.close()
    except:
        old=0
    return old

def save_current_version(new):
    file = open('app/crontab/ver.txt', 'w')
    file.write(new)
    file.close()
