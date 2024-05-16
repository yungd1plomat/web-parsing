from twocaptcha import TwoCaptcha
from bs4 import BeautifulSoup
import logging
from curl_cffi import requests
import random
import urllib.parse
import time

class ElibraryParser:

    # Константа указывающая на максимальное количество статей на странице
    ARTICLES_PER_PAGE = 100

    # Константа минимальная задержка
    MIN_DELAY = 1

    # Константа максимальная задержка
    MAX_DELAY = 5

    # Фингерпринты TLS для подмены
    __fingerprints = ['chrome99', 'chrome100', 'chrome101', 'chrome104', 'chrome107', 'chrome110', 'chrome116', 'chrome119', 'chrome120', 'chrome123', 'chrome124']

    def __init__(self, api_key, cookies):
        # Решалка капчи
        self.__solver = TwoCaptcha(api_key)

        # Заголовки для каждого запроса
        self.__headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://elibrary.ru',
            'Pragma': 'no-cache',
            'Priority': 'u=1',
            'Referer': 'https://elibrary.ru/querybox.asp?scope=newquery',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Cookie': cookies
        }

        # Выбираем рандомный TLS фингерпринт
        self.__fingerprint = random.choice(self.__fingerprints)
    
    def parse_articles(self, author):
        # Храним все статьи
        all_articles = []
        try:
            # Парсим статьи с первой страницы
            init_articles = self.__parse_initial_page(author)
            logging.info(f'Parsed init {len(init_articles)} articles for {author}')

            # Добавляем ко всем статьям
            all_articles += init_articles

            # Если статей максимальное кол-во, значит есть еще страницы
            if len(init_articles) == self.ARTICLES_PER_PAGE:

                # Случайная задержка, чтобы эмулировать поведение пользователя
                self.__random_delay()
                page = 2
                while True:
                    # Парсим статьи на n странице
                    articles = self.__parse_page_num(page)
                    
                    # Добавляем к общим статьям
                    all_articles += articles
                    logging.info(f'Parsed {len(articles)} articles for {author} on {page} page')

                    # Статей меньше чем максимальное количество - нет больше страниц
                    if len(articles) < self.ARTICLES_PER_PAGE:
                        break

                    page += 1

                    # Случайная задержка, чтобы эмулировать поведение пользователя
                    self.__random_delay()
        except Exception as ex:
            # В случае ошибки просто отображаем ошибку
            logging.error(ex)
        logging.info(f'Parsed {len(all_articles)} articles for {author}')
        return all_articles

    def __random_delay(self):
        delay = random.randint(self.MIN_DELAY, self.MAX_DELAY)
        logging.info(f'Sleeping {delay} seconds..')
        time.sleep(delay)

    def __solve_captcha(self, captcha):
        # Получаем sitekey
        sitekey = captcha.get('data-sitekey')
        while True:
            try:
                logging.info(f'Solving captcha with sitekey {sitekey}')
                # Кидаем на решение с sitekey и url
                response = self.__solver.recaptcha(sitekey, 'https://elibrary.ru/check_captcha.asp')
                
                # Капча успешно решена, формируем данные формы с ответом
                data = {
                    'g-recaptcha-response': response['code'],
                    'rpage': 'https://elibrary.ru'
                }

                # Кодируем данные в строку
                payload_str = urllib.parse.urlencode(data, safe=':+')

                # Посылаем решенную капчу на сервер
                resp = requests.post('https://elibrary.ru/check_captcha.asp', data=payload_str, headers=self.__headers, verify=False, impersonate=self.__fingerprint)
                
                # Если все ок - капча решена
                if resp.ok:
                    logging.info(f'Captcha successfully solved!')
                    break
            except:
                # Не удалось решить капчу, пробуем снова в беск цикле
                logging.error('Can\'t solve captcha, retrying..')
    
    # Парсинг html разметки страницы со статьями
    def __parse_page(self, html: BeautifulSoup):
        # Парсим все строки со статьями
        article_rows = html.select("a[href*=\/item\.asp\?]")
        articles = []
        for article_row in article_rows:
            # Получаем название статьи
            name = article_row.select_one('span').text

            # Получаем авторов статьи
            authors = article_row.parent.select_one('i').text

            # Закидываем все в список
            articles.append((authors, name))
        # Возвращаем список статей
        return articles


    # Парсит последующие страницы
    def __parse_page_num(self, page_num = 2):
        # query_results.asp?pagenum=2
        response = requests.get(f'https://elibrary.ru/query_results.asp?pagenum={page_num}', headers=self.__headers, verify=False, impersonate=self.__fingerprint)
        
        # Загружаем html
        html = BeautifulSoup(response.content, features="html.parser")
        
        # Парсим капчу, если она есть
        captcha = html.select_one('.g-recaptcha')
        if captcha:
            # Решаем капчу и пытаемся сделать запрос снова
            self.__solve_captcha(captcha)
            return self.__parse_page_num(page_num)
        
        # Парсим все статьи на странице и возвращаем
        articles = self.__parse_page(html)
        return articles

    # Парсит первую страницу со статьями
    def __parse_initial_page(self, author):
        # Выделяем фамилию автора
        surname = author.split(' ')[0]

        # Выделяем первую букву имени автора
        name_letter = author.split(' ')[1][0]

        # Выделяем первую букву отчества
        patronymic_letter = author.split(' ')[2][0]
        
        # Преобразуем в формат который нужен для поиска (Пример Старцева+О+Г|)
        initials = f'{surname}+{name_letter}+{patronymic_letter}|'
        
        # Данные запроса (искать везде, с указанным автором, сортировка по дате добавления)
        # Форма name = value
        data = {
            'querybox_name': '',
            'authors_all': initials,
            'titles_all': '',
            'rubrics_all': '',
            'changed': '1',
            'queryid': '',
            'ftext': '',
            'where_name': 'on',
            'where_abstract': 'on',
            'where_keywords': 'on',
            'where_references': '',
            'type_article': 'on',
            'type_disser': 'on',
            'type_book': 'on',
            'type_report': 'on',
            'type_conf': 'on',
            'type_patent': 'on',
            'type_preprint': 'on',
            'type_grant': 'on',
            'type_dataset': 'on',
            'search_itemboxid': '',
            'search_morph': 'on',
            'begin_year': '0',
            'end_year': '0',
            'issues': 'all',
            'orderby': 'insdate',
            'order': 'rev',
            'queryboxid': '0',
            'save_queryboxid': '0'
        }

        # Кодируем данные в строку
        payload_str = urllib.parse.urlencode(data, safe=':+')
        
        # Делаем запрос
        response = requests.post('https://elibrary.ru/query_results.asp', data=payload_str, headers=self.__headers, verify=False, impersonate=self.__fingerprint)
        
        # Загружаем html
        html = BeautifulSoup(response.content, features="html.parser")
        
        # Парсим капчу, если она есть
        captcha = html.select_one('.g-recaptcha')
        if captcha:
            # Решаем капчу и пытаемся сделать запрос снова
            self.__solve_captcha(captcha)
            return self.__parse_initial_page(author)
        
        # Парсим список статей и возвращаем
        articles = self.__parse_page(html)
        return articles
        


        
