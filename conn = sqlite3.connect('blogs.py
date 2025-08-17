conn = sqlite3.connect('blogs.db')
blog = conn.execute('SELECT title, content, price, username FROM blogs JOIN users ON blogs.user_id = users.id WHERE blogs.id=?', (blog_id,)).fetchone()

# Check if user has purchased
unlocked = False
if 'user_id' in session:
    purchase = conn.execute('SELECT * FROM purchases WHERE user_id=? AND blog_id=?', (session['user_id'], blog_id)).fetchone()
    if purchase:
        unlocked = True

conn.close()
return render_template('blog.html', blog=blog, blog_id=blog_id, unlocked=unlocked)
