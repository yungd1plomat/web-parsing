from sentence_transformers import SentenceTransformer, util
from dbconnector.dbconnector import DbContext

class IntelliSearch:
    def __init__(self):
        self.__model = SentenceTransformer('all-MiniLM-L6-v2')
        self.__database = DbContext()
    
    """
    Выполняет семантический поиск статей по заданному запросу.

    :param query: Строка запроса для поиска
    :param data: Список словарей с данными статей
    :param model: Модель SentenceTransformer для получения эмбеддингов
    :param title_embeddings: Эмбеддинги заголовков статей
    :param threshold: Порог сходства для определения совпадений
    :return: Список найденных статей, удовлетворяющих критерию сходства
    """
    def __search_articles(self, query, data, title_embeddings, threshold=0.5):
        query_embedding = self.__model.encode(query, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_embedding, title_embeddings)[0]
        
        results = []
        for idx, similarity in enumerate(similarities):
            if similarity >= threshold:
                results.append({
                    "authors": data[idx]["authors"],
                    "article_name": data[idx]["article_name"],
                    "similarity": similarity.item()
                })
        
        # Сортировка результатов по убыванию сходства
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results

    def __get_embeddings(self, articles):
        
        # Получение эмбеддингов для всех заголовков
        names = [entry["article_name"] for entry in articles]
        name_embeddings = self.__model.encode(names, convert_to_tensor=True)
        return name_embeddings

    def search_articles(self, query):
        articles = self.__database.get_articles()
        embeddings = self.__get_embeddings(articles)
        results = self.__search_articles(query, articles, embeddings)
        return results

