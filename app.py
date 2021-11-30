from flask import Flask, g, request
import sqlite3
import os.path

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
    if not os.path.isfile(DATABASE):
        with app.app_context():
            db = get_db()
            with app.open_resource('src\\database\\schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()


def create_request(query, params=''):
    db = get_db()
    cur = db.cursor()
    cur.execute(query, params)
    db.commit()
    return cur


def insert_or_replace_meal_request(params):
    query = ''' INSERT OR REPLACE INTO meal(id,name,description,category)
        VALUES(?,?,?,?) '''
    return create_request(query, params)


def insert_or_replace_ingredient_request(params):
    query = ''' INSERT OR REPLACE INTO ingredient(id,name,kcal,carbohydrates,fats,proteins)
        VALUES(?,?,?,?,?,?) '''
    return create_request(query, params)


def insert_or_replace_meal_indredient_request(params):
    query = ''' INSERT OR REPLACE INTO meal_indredient(id,ingredient_name,meal_id,description,amount)
        VALUES(?,?,?,?,?) '''
    return create_request(query, params)


def select_all_from_table(table):
    query = f''' SELECT * FROM {table} '''
    return create_request(query)


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/insert_meal')
def insert_meal():
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


@app.route('/meals')
def get_meals():
    output = select_all_from_table('meal').fetchall()
    return str(output)

@app.route('/ingredients')
def get_ingredients():
    output = select_all_from_table('ingredient').fetchall()
    return str(output)

@app.route('/meals_ingredients')
def get_meals_ingredients():
    output = select_all_from_table('meal_indredient').fetchall()
    return str(output)


if __name__ == '__main__':
    init_db()
    app.run(host='localhost', port=5000, debug=True)
