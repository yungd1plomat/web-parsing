from twocaptcha import TwoCaptcha
from elibraryparser import ElibraryParser
from time import sleep
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import urllib.parse
import logging
from dbconnector import DbContext

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)


load_dotenv()

api_key = os.getenv('API_KEY')
cookies = os.getenv('COOKIES')
database = DbContext()
parser = ElibraryParser(api_key, cookies)

teachers = database.get_all_teachers()
remain = len(teachers)
for teacher in teachers:
    articles = parser.parse_articles(teacher)
    database.save_articles(teacher, articles)
    remain -= 1
    logging.info(f'Remain {remain}')
    
