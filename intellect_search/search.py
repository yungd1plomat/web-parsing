from fuzzywuzzy import fuzz, process
from dbconnector.dbconnector import DbContext

class IntelliSearch:
    def __init__(self):
        self.__database = DbContext()
    
    def search_articles(self, query, threshold=90):
        articles = self.__database.get_articles()
        results = []
        for entry in articles:
            authors = entry['authors']
            name = entry['article_name']
            link = entry['link']
            ratio = fuzz.partial_ratio(query, name)
            if ratio >= threshold:
                results.append({'authors': authors, 'name': name, 'link': link, 'similarity': ratio})


        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results

