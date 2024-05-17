from fuzzywuzzy import fuzz, process
from dbconnector.dbconnector import DbContext
from fuzzywuzzy import process

class IntelliSearch:
    def __init__(self):
        self.__database = DbContext()

    # Поиск в массиве статей с помощью fuzz.WRatio()
    def search_articles(self, query):
        # Получаем список статей
        articles = self.__database.get_articles()
        # Ищем топ 10 похожих статьи по запросу
        results = process.extract(query, articles, limit=10)
        return results
