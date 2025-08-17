@app.route('/my-purchases')
def my_purchases():
    if 'user_id' not in session:
        return redirect('/login')
    conn = sqlite3.connect('blogs.db')
    purchases = conn.execute('''
        SELECT blogs.title, blogs.price, users.username
        FROM purchases
        JOIN blogs ON purchases.blog_id = blogs.id
        JOIN users ON blogs.user_id = users.id
        WHERE purchases.user_id=?
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('purchases.html', purchases=purchases)