from flask import Flask, request, jsonify, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, phone) VALUES (?, ?, ?)",
        (name, email, phone)
    )
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name=?, email=?, phone=? WHERE id=?",
        (name, email, phone, id)
    )
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    user_list = []
    for user in users:
        user_list.append({
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "phone": user[3]
        })

    return jsonify(user_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)