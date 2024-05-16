import requests
from bs4 import BeautifulSoup
import logging
from dbconnector import DbContext

class BspuParser:

    def __init__(self):
        self.__database = DbContext()

    def parse_college(self):
        # Делаем запрос чтобы получить таблицу с преподавателями
        request = requests.get("https://bspu.ru/sveden/employees")

        # Парсим html
        soup = BeautifulSoup(request.content, 'html.parser')

        # Парсим таблицу с преподавателями колледжа БГПУ
        colleague_data = soup.find("div", id="collapseThree")

        # Получаем ФИО преподавателей колледжа
        colleague_fio = colleague_data.find_all("td", itemprop="fio")

        teachers = []
        for fio in colleague_fio:
             # Добавляем ФИО в список
            teachers.append(fio.text.strip())
        logging.info(f'Parsed {len(teachers)} college teachers')

        # Сохраняем данные в бд
        self.__database.save_college(teachers)
    
    def parse_university(self):
        # Делаем запрос чтобы получить таблицу с преподавателями
        request = requests.get("https://bspu.ru/sveden/employees")

        # Парсим html
        soup = BeautifulSoup(request.content, 'html.parser')

        # Парсим таблицу с преподавателями Вуза
        university_data = soup.find("div", id="collapseTwo")

        # Получаем ФИО преподавателей Вуза
        university_fio = university_data.find_all("td", itemprop="fio")

        teachers = []
        for fio in university_fio:
            # Добавляем ФИО в список
            teachers.append(fio.text.strip())
        logging.info(f'Parsed {len(teachers)} university teachers')
        
        # Сохраняем данные в бд
        self.__database.save_university(teachers)