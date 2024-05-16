import sqlite3
import requests
from bs4 import BeautifulSoup


def parse_teachers_fio():
    request = requests.get("https://bspu.ru/sveden/employees")
    soup = BeautifulSoup(request.content, 'html.parser')

    university_data = soup.find("div", id="collapseTwo")
    colleague_data = soup.find("div", id="collapseThree")

    university_fio = university_data.find_all("td", itemprop="fio")
    colleague_fio = colleague_data.find_all("td", itemprop="fio")

    bspu_teachers_fio = []

    for fio in university_fio:
        bspu_teachers_fio.append(fio.text.strip())

    for fio in colleague_fio:
        print(fio.text.strip())

def add_into_db(list array):
    connection = sqlite3.connect('db/teachers_fios.db')

    connection.close()

parse_teachers_fio()