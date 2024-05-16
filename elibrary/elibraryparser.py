from twocaptcha import TwoCaptcha
import requests
from bs4 import BeautifulSoup
import logging

class ElibraryParser:
    
    def __init__(self, api_key, cookies):
        # Решалка капчи
        self.solver = TwoCaptcha(api_key)

        # Сессия для запросов
        self.session = requests.session()

        # Заголовки для каждого запроса
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Priority': 'u=1',
            'Referer': 'https://elibrary.ru',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Cookie': cookies
        }


    def solve_captcha(self, captcha):
        sitekey = captcha.get('data-sitekey')
        while True:
            logging.info(f'Solving captcha with sitekey {sitekey}')
            response = self.solver.recaptcha(sitekey, 'https://elibrary.ru/check_captcha.asp')
            data = {
                'g-recaptcha-response': (None, response['code']),
                'rpage': (None, 'https://elibrary.ru')
            }
            resp = self.session.post('https://elibrary.ru/query_results.asp', files=data, headers=self.headers, verify=False)
            if resp.ok:
                logging.info(f'Captcha successfully solved!')
                break

    def parse_initial_page(self, author):
        # Выделяем фамилию автора
        surname = author.split(' ')[0]

        # Выделяем первую букву имени автора
        name_letter = author.split(' ')[1][0]

        # Выделяем первую букву отчества
        patronymic_letter = author.split(' ')[2][0]
        
        # Преобразуем в формат который нужен для поиска (Пример Старцева+О+Г|)
        initials = f'{surname}+{name_letter}+{patronymic_letter}|'
        
        # Данные запроса (искать везде, с указанным автором, сортировка по дате добавления)
        # Форма name - value без указания filename
        data = {
            'querybox_name': (None, ''),
            'authors_all': (None, initials),
            'titles_all': (None, ''),
            'rubrics_all': (None, ''),
            'changed': (None, '1'),
            'queryid': (None, ''),
            'ftext': (None, ''),
            'where_references': (None, ''),
            'type_article': (None, 'on'),
            'type_disser': (None, 'on'),
            'type_book': (None, 'on'),
            'type_report': (None, 'on'),
            'type_conf': (None, 'on'),
            'type_patent': (None, 'on'),
            'type_preprint': (None, 'on'),
            'type_grant': (None, 'on'),
            'type_dataset': (None, 'on'),
            'search_itemboxid': (None, ''),
            'search_morph': (None, 'on'),
            'begin_year': (None, '0'),
            'end_year': (None, '0'),
            'issues': (None, 'all'),
            'orderby': (None, 'insdate'),
            'order': (None, 'rev'),
            'queryboxid': (None, '0'),
            'save_queryboxid': (None, '0')
        }
        response = self.session.post('https://elibrary.ru/query_results.asp', files=data, headers=self.headers)
        html = BeautifulSoup(response.content, features="html.parser")
        captcha = html.select_one('.g-recaptcha')
        if captcha:
            self.solve_captcha(captcha)
            return self.parse_initial_page(author)
        print('Parsed!')


        
