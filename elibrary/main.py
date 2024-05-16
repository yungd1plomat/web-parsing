from twocaptcha import TwoCaptcha
from elibraryparser import ElibraryParser
from time import sleep
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import urllib.parse
import logging

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

load_dotenv()

api_key = os.getenv('API_KEY')
cookies = os.getenv('COOKIES')
parser = ElibraryParser(api_key, cookies)

articles = parser.parse_articles('Старцева Оксана Геннадиевна')