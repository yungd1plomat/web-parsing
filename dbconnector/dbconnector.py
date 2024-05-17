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
        self.__db.execute('CREATE TABLE IF NOT EXISTS articles (teacher VARCHAR REFERENCES teachers (name) NOT NULL, authors TEXT NOT NULL, article_name TEXT NOT NULL, link VARCHAR NOT NULL);')
    
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
                    'link': row[3]
                }
                all_data.append(data)
            return all_data
        except sqlite3.Error as e:
            logging.error(f'Ошибка при получении данных: {e}')
    
    def get_all_teachers(self):
        # Получаем всех преподавателей из БД
        self.cursor.execute('SELECT name FROM teachers')
        rows = self.cursor.fetchall()
        teachers = [row[0] for row in rows]
        return teachers

    def save_articles(self, teacher, articles):
        for authors, name, link in articles:
            # Проверяем существует ли уже такая запись в БД
            self.cursor.execute('''SELECT teacher FROM articles WHERE teacher = ? AND authors = ? AND article_name = ? AND link = ?''', (teacher, authors, name, link, ))
            exist = self.cursor.fetchone()
            # Если записи не существует вставляем, если существует - скип
            if not exist:
                self.cursor.execute('''INSERT INTO articles (teacher, authors, article_name, link) VALUES (?, ?, ?, ?)''', (teacher, authors, name, link, ))
        self.__db.commit()