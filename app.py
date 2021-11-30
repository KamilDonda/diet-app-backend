from flask import Flask, g, request, jsonify
import sqlite3
import os.path
from src.database.entities.MealIngredientEntity import MealIngredientEntity
from src.database.entities.IngredientEntity import IngredientEntity
from src.database.entities.MealEntity import MealEntity

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


def select_by_id(table, id):
    query = f''' SELECT * FROM {table} WHERE ID = {id}'''
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


@app.route('/meals/')
def get_meals():
    meals = select_all_from_table('meal').fetchall()

    mealsJSON = []
    for meal in meals:
        id, name, desc, cat = meal
        mealsJSON.append(MealEntity(id, name, desc, cat).serialize())

    return jsonify(mealsJSON)


@app.route('/meals/<id>')
def get_meal_by_id(id):
    id, name, desc, cat = select_by_id('meal', id).fetchone()
    return MealEntity(id, name, desc, cat).serialize()


@app.route('/ingredients/')
def get_ingredients():
    ingredients = select_all_from_table('ingredient').fetchall()
    ingredientsJSON = []
    for ingredient in ingredients:
        id, name, kcal, carbs, fats, prots, tags = ingredient
        ingredientsJSON.append(IngredientEntity(id, name, kcal, carbs, fats, prots, tags).serialize())
    return jsonify(ingredientsJSON)


@app.route('/ingredients/<id>')
def get_ingredient_by_id(id):
    id, name, kcal, carbs, fats, prots, tags = select_by_id('ingredient', id).fetchone()
    return IngredientEntity(id, name, kcal, carbs, fats, prots, tags).serialize()


@app.route('/meals_ingredients/')
def get_meals_ingredients():
    meals_ingredients = select_all_from_table('meal_indredient').fetchall()
    meals_ingredientsJSON = []
    for mi in meals_ingredients:
        id, meal_id, ing_name, desc, amount = mi
        meals_ingredientsJSON.append(MealIngredientEntity(id, meal_id, ing_name, desc, amount).serialize())
    return jsonify(meals_ingredientsJSON)


@app.route('/meals_ingredients/<id>')
def get_meals_ingredients_by_id(id):
    id, meal_id, ing_name, desc, amount = select_by_id('meal_indredient', id).fetchone()
    return MealIngredientEntity(id, meal_id, ing_name, desc, amount).serialize()


if __name__ == '__main__':
    init_db()
    app.config['JSON_AS_ASCII'] = False
    app.run(host='localhost', port=5000, debug=True)
