from flask import Flask, g, request
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


def create_request(query, params):
    db = get_db()
    cur = db.cursor()
    cur.execute(query, params)
    db.commit()
    return cur.lastrowid


def insert_or_replace_meal_request(params):
    query = ''' INSERT OR REPLACE INTO meal(id,name,description,category)
        VALUES(?,?,?,?) '''
    create_request(query, params)


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/insert_meal')
def insert():
    try:
        id = request.args.get('id')
        name = request.args.get('name')
        description = request.args.get('description')
        category = request.args.get('category')

        if not id.isdigit():
            return 'Not digit'

        if not category in ('breakfast', 'dinner', 'supper'):
            return 'Not in category'
    
        params = (id, name, description, category)
        insert_or_replace_meal_request(params)
        return 'Ok'
    except:
        return 'Exception'


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
