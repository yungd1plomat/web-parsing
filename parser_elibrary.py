import logging
from dbconnector.dbconnector import DbContext
from dotenv import load_dotenv
import os
from elibrary.elibraryparser import ElibraryParser

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