from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import sqlite3

# Функция для подключения к базе данных
def get_db():
    conn = sqlite3.connect('resume_threads.db')
    conn.row_factory = sqlite3.Row
    return conn

def register():
    data = request.get_json()
    password = data.get('password')
    email = data.get('email')

    # Хеширование пароля
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Users (password_hash, email) VALUES (?, ?)',
                         (password_hash, email))
            user_id = cursor.lastrowid
            access_token = create_access_token(identity=user_id)
            return jsonify({'message': 'Registration successful!', 'access_token': access_token}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists.'}), 400

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    with get_db() as conn:
        user = conn.execute('SELECT * FROM Users WHERE email = ?', (email,)).fetchone()

        if user and check_password_hash(user['password_hash'], password):
            access_token = create_access_token(identity=user['user_id'])
            return jsonify({'message': 'Login successful!', 'email': user['email'], 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid username or password.'}), 401

def check_access():
    user_id = get_jwt_identity()
    print(user_id)

    return jsonify({'message': f'Welcome, user {session["user_id"]}!'}), 200

    if 'user_id' not in session:
        return jsonify({'message': 'You need to log in first.'}), 401

    return jsonify({'message': f'Welcome, user {session["user_id"]}!'}), 200