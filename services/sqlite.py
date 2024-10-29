import sqlite3

# Подключение к базе данных (если файла нет, он будет создан)
conn = sqlite3.connect('resume_threads.db')

# Создание курсора для выполнения операций с базой данных
cursor = conn.cursor()

# Создание таблицы Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Создание таблицы Threads
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Threads (
#     thread_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     result TEXT,
#     error_message TEXT,
#     status TEXT,
#     FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE
# )
# ''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных и таблицы успешно созданы!")