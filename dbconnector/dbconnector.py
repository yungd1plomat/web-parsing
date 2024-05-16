import sqlite3
import logging

class DbContext:
    def __init__(self):
        # Подключаемся к БД
        self.__db = sqlite3.connect('data/bspu.db')
        self.cursor = self.__db.cursor()
        
        # Создаем таблицу teachers (Преподаватели)
        self.__db.execute('CREATE TABLE IF NOT EXISTS teachers (name VARCHAR NOT NULL PRIMARY KEY UNIQUE, type VARCHAR NOT NULL);')
        
        # Создаем таблицу articles (Статьи)
        self.__db.execute('CREATE TABLE IF NOT EXISTS articles (teacher VARCHAR REFERENCES teachers (name) NOT NULL, authors TEXT NOT NULL, article_name TEXT NOT NULL);')
    
    def save_college(self, teachers):
        try:
            data = [(name, 'college') for name in teachers]
            # Пытаемся вставить запись, если name уже существует, она будет обновлена
            self.cursor.executemany('''INSERT OR REPLACE INTO teachers (name, type) 
                                       VALUES (?, ?)''', data)
            self.__db.commit()
        except sqlite3.Error as e:
            logging.error(f'Ошибка при вставке данных: {e}')
    
    def save_university(self, teachers):
        try:
            data = [(name, 'university') for name in teachers]
            # Пытаемся вставить запись, если name уже существует, она будет обновлена
            self.cursor.executemany('''INSERT OR REPLACE INTO teachers (name, type) 
                                       VALUES (?, ?)''', data)
            self.__db.commit()
        except sqlite3.Error as e:
            logging.error(f'Ошибка при вставке данных: {e}')
    
    def get_articles(self):
        try:
            self.cursor.execute('''SELECT * FROM articles''')
            rows = self.cursor.fetchall()
            all_data = []
            for row in rows:
                data = {
                    'teacher': row[0],
                    'authors': row[1],
                    'article_name': row[2],
                    #'link': row[3]
                }
                all_data.append(data)
            return all_data
        except sqlite3.Error as e:
            logging.error(f'Ошибка при получении данных: {e}')