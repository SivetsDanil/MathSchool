import sqlite3
import os
from typing import List, Dict, Optional


DB_PATH = 'tutors.db'


def init_db():
    """Создаёт базу данных по шаблону из словаря"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создаём таблицу преподавателей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            degree TEXT NOT NULL,
            experience TEXT NOT NULL,
            bio TEXT NOT NULL,
            tags TEXT NOT NULL  -- хранится как JSON-строка
        )
    ''')

    # Проверяем, есть ли уже данные
    cursor.execute('SELECT COUNT(*) FROM tutors')
    if cursor.fetchone()[0] == 0:
        # Вставляем начальные данные (как в твоём словаре)
        initial_data = [
            # Математика
            ('Великий математик', 'math', 'КФУ, бакалавриат филологии', '7 лет',
             'Окончил бакалавриат мехмат СПБГУ с красным дипломом. Математик.',
             '["ЕГЭ", "СПбГУ", "опыт 7 лет"]'),
            ('Алексей Смирнов', 'math', 'МФТИ, кандидат наук', '12 лет',
             'Преподаю математику с 2012 года. Автор 3 курсов по олимпиадной математике.',
             '["МФТИ", "олимпиады", "12 лет"]'),

            # Информатика
            ('Иван Петров', 'it', 'ВШЭ, магистратура', '5 лет',
             'Разработчик и преподаватель. Создал курс «Python для школьников» с нуля.',
             '["ВШЭ", "Python", "5 лет"]'),

            # Физика
            ('Отец физики', 'physics', 'МГУ, кандидат наук', '9 лет',
             'Преподаю физику с 2015 года. Лучший Репетитор по физике на 90+ баллов',
             '["МГУ", "ЕГЭ", "9 лет"]')
        ]

        cursor.executemany('''
            INSERT INTO tutors (name, subject, degree, experience, bio, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', initial_data)

    conn.commit()
    conn.close()


def add_tutor(name: str, subject: str, degree: str, experience: str, bio: str, tags: List[str]):
    """Добавляет нового преподавателя"""
    import json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tutors (name, subject, degree, experience, bio, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, subject, degree, experience, bio, json.dumps(tags)))

    conn.commit()
    conn.close()


def delete_tutor_by_name(name: str):
    """Удаляет преподавателя по имени"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM tutors WHERE name = ?', (name,))

    conn.commit()
    conn.close()


def get_tutors_by_subject(subject: str) -> List[Dict]:
    """Возвращает список преподавателей по предмету"""
    import json
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # чтобы получать словари
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tutors WHERE subject = ?', (subject,))
    rows = cursor.fetchall()

    tutors = []
    for row in rows:
        tutor = dict(row)
        tutor['tags'] = json.loads(tutor['tags'])  # преобразуем строку обратно в список
        tutors.append(tutor)

    conn.close()
    return tutors