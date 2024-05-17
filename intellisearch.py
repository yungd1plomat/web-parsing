from intellect_search.search import IntelliSearch

query = input('Введите название для поиска: ')
intelli_search = IntelliSearch()
result = intelli_search.search_articles(query)
print(result)