@app.route('/error')
def error():
    return "<h1>⚠️ Something went wrong with payment. Try again later.</h1>"