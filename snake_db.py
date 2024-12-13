# snake_db.py

import sqlite3

# Function to create a database and necessary tables
def create_db():
    conn = sqlite3.connect('snake_game.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        level INTEGER DEFAULT 1,
                        high_score INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_score (
                        user_id INTEGER,
                        score INTEGER,
                        level INTEGER,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES user (id))''')
    conn.commit()
    conn.close()

# Function to get user details from the database
def get_user_details(username):
    conn = sqlite3.connect('snake_game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to save the user's score to the database
def save_user_score(user_id, score, level):
    conn = sqlite3.connect('snake_game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_score (user_id, score, level) VALUES (?, ?, ?)", (user_id, score, level))
    conn.commit()
    conn.close()

# Function to save or update user details (username, level, high score)
def save_user(username, level, high_score):
    conn = sqlite3.connect('snake_game.db')
    cursor = conn.cursor()
    existing_user = get_user_details(username)
    if existing_user:
        cursor.execute("UPDATE user SET level = ?, high_score = ? WHERE username = ?", (level, high_score, username))
    else:
        cursor.execute("INSERT INTO user (username, level, high_score) VALUES (?, ?, ?)", (username, level, high_score))
    conn.commit()
    conn.close()
