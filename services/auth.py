from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# Функция для подключения к базе данных
def get_db():
    conn = sqlite3.connect('resume_threads.db')
    conn.row_factory = sqlite3.Row
    return conn

def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Хеширование пароля
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        with get_db() as conn:
            conn.execute('INSERT INTO Users (username, password_hash, email) VALUES (?, ?, ?)',
                         (username, password_hash, email))
            return jsonify({'message': 'Registration successful!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username or email already exists.'}), 400

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    with get_db() as conn:
        user = conn.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            print(session)
            return jsonify({'message': 'Login successful!', 'username': user['username']}), 200
        else:
            return jsonify({'message': 'Invalid username or password.'}), 401

def check_access():
    print(session)
    if 'user_id' not in session:
        return jsonify({'message': 'You need to log in first.'}), 401

    return jsonify({'message': f'Welcome, user {session["user_id"]}!'}), 200

def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'You have been logged out.'}), 200