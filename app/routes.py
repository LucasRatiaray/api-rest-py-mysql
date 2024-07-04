from flask import request, jsonify
from . import mysql
import bcrypt

def register_routes(app):
    @app.route('/api/register', methods=['POST'])
    def register():
        user_data = request.get_json()
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            return jsonify({'message': 'Email is already in use'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mysql.connection.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    @app.route('/api/login', methods=['POST'])
    def login():
        user_data = request.get_json()
        email = user_data['email']
        password = user_data['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
