if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    blog_id = int(session['metadata']['blog_id'])
    user_id = int(session['metadata']['user_id'])

    conn = sqlite3.connect('blogs.db')
    conn.execute('INSERT INTO purchases (user_id, blog_id, session_id) VALUES (?, ?, ?)',
                 (user_id, blog_id, session['id']))
    conn.commit()
    conn.close()