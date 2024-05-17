import sqlite3
import logging


class DbContext:
    def __init__(self):
        # Подключаемся к БД
        self.__db = sqlite3.connect('../data/bspu.db')
        self.cursor = self.__db.cursor()
        
        # Создаем таблицу teachers (Преподаватели)
        self.__db.execute('CREATE TABLE IF NOT EXISTS teachers (name VARCHAR NOT NULL PRIMARY KEY UNIQUE, type VARCHAR NOT NULL);')
        
        # Создаем таблицу articles (Статьи)
        self.__db.execute('CREATE TABLE IF NOT EXISTS articles (teacher VARCHAR REFERENCES teachers (name) NOT NULL, authors TEXT NOT NULL, article_name TEXT NOT NULL, link VARCHAR NOT NULL);')

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