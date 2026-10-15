# dump_db.py
import sqlite3, json

conn = sqlite3.connect('tutors.db')
cur = conn.cursor()

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print('Таблицы:', tables)

data = []
for t in tables:
    cols = [d[1] for d in cur.execute(f'PRAGMA table_info({t})').fetchall()]
    for row in cur.execute(f'SELECT * FROM {t}').fetchall():
        data.append(dict(zip(cols, row)))

with open('content/tutors.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Готово! Сохранено {len(data)} записей в tutors.json')