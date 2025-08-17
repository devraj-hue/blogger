@app.route('/download/<int:blog_id>')
def download_blog(blog_id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = sqlite3.connect('blogs.db')
    purchase = conn.execute('SELECT * FROM purchases WHERE user_id=? AND blog_id=?', (session['user_id'], blog_id)).fetchone()
    blog = conn.execute('SELECT title, content FROM blogs WHERE id=?', (blog_id,)).fetchone()
    conn.close()

    if not purchase:
        return "Access denied", 403

    return f"<pre>{blog[1]}</pre>"  # You can also trigger a file download