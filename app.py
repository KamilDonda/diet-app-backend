from flask import Flask, g, request, jsonify
import sqlite3
import os.path
from db import insert_or_replace_meal_request, select_all_from_table_request, select_by_id_request, get_all_meals_with_nutriments_and_classification
from src.diet_calculator.input import calcInput
from src.diet.generation import DietGeneration
from src.database.entities.MealIngredientEntity import MealIngredientEntity
from src.database.entities.IngredientEntity import IngredientEntity
from src.database.entities.MealEntity import MealEntity
import config
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)

DATABASE = config.DATABASE_DB

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
firestore_db = firestore.client()
users_ref = firestore_db.collection('users')


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
            with app.open_resource(config.DATABASE_SCHEMA, mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()


@app.route('/')
def hello_world():
    # docs = users_ref.stream()
    # for doc in docs:
    #     print(f'{doc.id} => {doc.to_dict()}')
    return "Hello Wololo"


@app.route(config.INSERT_MEAL)
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


@app.route(config.MEALS)
def get_meals():
    meals = select_all_from_table_request('meal').fetchall()

    mealsJSON = []
    for meal in meals:
        id, name, desc, cat, classification = meal
        mealsJSON.append(MealEntity(id, name, desc, cat).serialize())

    return jsonify(mealsJSON)


@app.route(config.MEALS + '<id>')
def get_meal_by_id(id):
    id, name, desc, cat, classification = select_by_id_request(
        'meal', id).fetchone()
    return MealEntity(id, name, desc, cat).serialize()


@app.route(config.INGREDIENTS)
def get_ingredients():
    ingredients = select_all_from_table_request('ingredient').fetchall()
    ingredientsJSON = []
    for ingredient in ingredients:
        id, name, kcal, carbs, fats, prots, tags = ingredient
        ingredientsJSON.append(IngredientEntity(
            id, name, kcal, carbs, fats, prots, tags).serialize())
    return jsonify(ingredientsJSON)


@app.route(config.INGREDIENTS + '<id>')
def get_ingredient_by_id(id):
    id, name, kcal, carbs, fats, prots, tags = select_by_id_request(
        'ingredient', id).fetchone()
    return IngredientEntity(id, name, kcal, carbs, fats, prots, tags).serialize()


@app.route(config.MEALS_INGREDIENTS)
def get_meals_ingredients():
    meals_ingredients = select_all_from_table_request(
        'meal_ingredient').fetchall()
    meals_ingredientsJSON = []
    for mi in meals_ingredients:
        id, ing_id, meal_id, desc, amount = mi
        meals_ingredientsJSON.append(MealIngredientEntity(
            id, ing_id, meal_id, desc, amount).serialize())
    return jsonify(meals_ingredientsJSON)


@app.route(config.MEALS_INGREDIENTS + '<id>')
def get_meals_ingredients_by_id(id):
    id, ing_id, meal_id, desc, amount = select_by_id_request(
        'meal_ingredient', id).fetchone()
    return MealIngredientEntity(id, ing_id, meal_id, desc, amount).serialize()


# def foo():
#     from random import randint
#     id = 1
#     meals = []
#     for category in ("śniadanie", "obiad", "kolacja"):
#         for _ in range(25):
#             p = randint(10, 100)
#             c = randint(10, 100)
#             f = randint(10, 100)
#             cal = 4 * (p + c) + 8 * f

#             pref = []
#             if randint(1, 3) == 1:
#                 pref.append('mięso')
#             if randint(1, 3) == 1:
#                 pref.append('laktoza')
#             if randint(1, 3) == 1:
#                 pref.append('orzechy')

#             result = 0
#             if cal < 700:
#                 result = -1
#             if cal > 1100:
#                 result = 1

#             meal = {
#                 'id': id,
#                 'name': 'Meal' + str(id),
#                 'proteins': p,
#                 'carbohydrates': c,
#                 'fat': f,
#                 'cal': cal,
#                 'category': category,
#                 'preferences': pref,
#                 'result': result
#             }
#             meals.append(meal)
#             id += 1
#     return meals


@app.route(config.GENERATE_DIET)
def generate_diet():
    # from random import randint
    # pref = []
    # if randint(1, 3) == 1:
    #     pref.append('mięso')
    # if randint(1, 3) == 1:
    #     pref.append('laktoza')
    # if randint(1, 3) == 1:
    #     pref.append('orzechy')
    # input = calcInput(True, 22, 70, 175, 2, 1, pref)
    # diet = DietGeneration(input, foo())
    # return str(diet).replace("'", '"')
    # try:
    uid = request.args.get('uid')
    if uid:
        user = users_ref.document(uid).get().to_dict()
        activity = user['activity']
        age = user['age']
        gender = user['gender']
        goal = user['goal']
        height = user['height']
        weight = user['weight']
        preferences = user['preferences']
        input = calcInput(gender, age, weight, height,
                          activity, goal, preferences)
        meals = get_all_meals_with_nutriments_and_classification()
        diet = DietGeneration(input, meals)
        return jsonify(diet)
    else:
        return 'Error', 400
    # except Exception as e:
    #     return f"An Error Occured: {e}"


if __name__ == '__main__':
    init_db()
    app.config['JSON_AS_ASCII'] = False
    app.run(host=config.HOST, port=config.PORT, debug=True)
