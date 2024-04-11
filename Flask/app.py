from flask import Flask, render_template, g
import sqlite3

DATABASE = 'Flask\chinook.db'

app = Flask(__name__)

#helper function to get the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


#the home route- renders the home.html template
@app.route('/')
def home():
    return render_template('home.html')


#a route to query for the artists
@app.route('/artists')
def artists():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM artists')
    artists = cursor.fetchall()
    return render_template('artists.html', artists=artists)

#run the main app
if __name__ == '__main__':
    app.run(debug=True)