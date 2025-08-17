from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize DB
def init_db():
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS blogs (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    title TEXT,
                    content TEXT,
                    price REAL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('blogs.db')
    blogs = conn.execute('SELECT blogs.id, title, price, username FROM blogs JOIN users ON blogs.user_id = users.id').fetchall()
    conn.close()
    return render_template('index.html', blogs=blogs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('blogs.db')
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        except:
            return "Username already exists"
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('blogs.db')
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/dashboard')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        price = float(request.form['price'])
        conn = sqlite3.connect('blogs.db')
        conn.execute('INSERT INTO blogs (user_id, title, content, price) VALUES (?, ?, ?, ?)',
                     (session['user_id'], title, content, price))
        conn.commit()
        conn.close()
    return render_template('dashboard.html', username=session['username'])

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    conn = sqlite3.connect('blogs.db')
    blog = conn.execute('SELECT title, content, price, username FROM blogs JOIN users ON blogs.user_id = users.id WHERE blogs.id=?', (blog_id,)).fetchone()
    conn.close()
    return render_template('blog.html', blog=blog)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)