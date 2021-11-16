from flask import Flask, g
import sqlite3

app = Flask(__name__)

DATABASE = 'src\\database\\database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('src\\database\\schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)