from fuzzywuzzy import fuzz, process

# Созданные руками, тестовые данные
data = [
    {"author": "Старцева Оксана Геннадиевна", "title": "Анализ данных с использованием Python"},
    {"author": "Абдрахманова Флорида Ривхатовна", "title": "Машинное обучение и глубокое обучение"},
    {"author": "Абдуллин Рамиль Раисович", "title": "Введение в нейронные сети"},
    {"author": "Анастасьев Алексей Геннадьевич", "title": "Обработка естественного языка"},
    {"author": "Амирова Зарема Канзафаровна", "title": "Естественные духовные скрепы"},
    {"author": "Амирова Людмила Александровна", "title": "Введение в высшую математику"},
    {"author": "Амирова Оксана Георгиевна", "title": "Абстракция у млекопитающих"},
    {"author": "Биккинин Ирек Анасович", "title": "Абстракция беспилотников и птиц"},
    {"author": "Бикметов Рустам Фаритович", "title": "Абстракция беспилотников для самых маленьких"},
    {"author": "Валеева Гульнара Рашитовна", "title": "Машинное обучение и глубокий математический анализ"},
    {"author": "Валеева Лиана Фанитовна", "title": "Анализ данных с использованием 1С"},
]


"""
Выполняет нечеткий поиск статей по заданному запросу.

:param query: Строка запроса для поиска
:param data: Список словарей с данными статей
:param threshold: Порог сходства для определения совпадений
:return: Список найденных статей, удовлетворяющих критерию сходства
"""
def search_articles(query, data, threshold=90):

    results = []
    for entry in data:
        title = entry["title"]
        ratio = fuzz.partial_ratio(query, title)
        if ratio >= threshold:
            results.append({"author": entry["author"], "title": title, "similarity": ratio})
    

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results

query = input("Введите название статьи для поиска: ")
results = search_articles(query, data)

print("Результаты поиска:")
for result in results:
    print(f"Автор: {result['author']}, Название: {result['title']}, Сходство: {result['similarity']}%")
