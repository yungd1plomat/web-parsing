from sentence_transformers import SentenceTransformer, util

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

model = SentenceTransformer('all-MiniLM-L6-v2')

# Получение эмбеддингов для всех заголовков
titles = [entry["title"] for entry in data]
title_embeddings = model.encode(titles, convert_to_tensor=True)

"""
Выполняет семантический поиск статей по заданному запросу.

:param query: Строка запроса для поиска
:param data: Список словарей с данными статей
:param model: Модель SentenceTransformer для получения эмбеддингов
:param title_embeddings: Эмбеддинги заголовков статей
:param threshold: Порог сходства для определения совпадений
:return: Список найденных статей, удовлетворяющих критерию сходства
"""
def search_articles(query, data, model, title_embeddings, threshold=0.5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, title_embeddings)[0]
    
    results = []
    for idx, similarity in enumerate(similarities):
        if similarity >= threshold:
            results.append({
                "author": data[idx]["author"],
                "title": data[idx]["title"],
                "similarity": similarity.item()
            })
    
    # Сортировка результатов по убыванию сходства
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results

query = input("Введите название статьи для поиска: ")
results = search_articles(query, data, model, title_embeddings)

print("Результаты поиска:")
for result in results:
    print(f"Автор: {result['author']}, Название: {result['title']}, Сходство: {result['similarity']:.2f}")
