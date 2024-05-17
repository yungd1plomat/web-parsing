from intellect_search.search import IntelliSearch
import logging

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

query = input('Введите название для поиска: ')
intelli_search = IntelliSearch()
result = intelli_search.search_articles(query)
for article in result:
    logging.info(f'Авторы: {article[0]["authors"]}, Статья: {article[0]["article_name"]}, Ссылка: {article[0]["link"]}')