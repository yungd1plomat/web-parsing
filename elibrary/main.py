from twocaptcha import TwoCaptcha
from elibraryparser import ElibraryParser
from time import sleep
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import requests


load_dotenv()

api_key = os.getenv('API_KEY')
cookies = os.getenv('COOKIES')
parser = ElibraryParser(api_key, cookies)
parser.parse_initial_page('Старцева Оксана Геннадиевна')
