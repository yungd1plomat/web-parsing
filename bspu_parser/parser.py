import requests
from bs4 import BeautifulSoup


def parse_teachers_fio():

    request = requests.get("https://bspu.ru/sveden/employees")

    soup = BeautifulSoup(request.content, 'html.parser')

    university_data = soup.find("div", id="collapseTwo")

    colleague_data = soup.find("div", id="collapseThree")

    university_fio = university_data.find_all("td", itemprop="fio")
    colleague_fio = colleague_data.find_all("td", itemprop="fio")

    print("Преподаватели из ВУЗа:\n")

    for fio in university_fio:
        print(fio.text.strip())

    print("\nПреподаватели из Колледжа:\n")

    for fio in colleague_fio:
        print(fio.text.strip())

parse_teachers_fio()