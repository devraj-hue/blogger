@app.route('/buy/<int:blog_id>', methods=['POST'])
def buy_blog(blog_id):
    conn = sqlite3.connect('blogs.db')
    blog = conn.execute('SELECT title, price FROM blogs WHERE id=?', (blog_id,)).fetchone()
    conn.close()

    if not blog:
        return "Blog not found", 404

    checkout_url = create_checkout_session(blog[0], blog[1])
    return redirect(checkout_url, code=303)