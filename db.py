import sqlite3
from sqlite3 import Error
import config
import numpy as np

DATABASE = config.DATABASE_DB


def get_db():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)

    return conn


def insert_or_replace_meal_request(params):
    query = ''' INSERT OR REPLACE INTO meal(id, name, description, category, classification)
        VALUES(?,?,?,?,?) '''
    return create_request(query, params)


def insert_or_replace_ingredient_request(params):
    query = ''' INSERT OR REPLACE INTO ingredient(id, name, kcal, carbohydrates, fats, proteins, tags)
        VALUES(?,?,?,?,?,?,?) '''
    return create_request(query, params)


def insert_or_replace_meal_ingredient_request(params):
    query = ''' INSERT OR REPLACE INTO meal_ingredient(id, ingredient_id, meal_id, description, amount)
        VALUES(?,?,?,?,?) '''
    return create_request(query, params)


def update_meal_classification_request(params):
    query = ''' UPDATE meal SET classification = ? WHERE id = ? '''
    return create_request(query, params)


def select_all_from_table_request(table):
    query = f''' SELECT * FROM {table} '''
    return create_request(query)


def select_by_id_request(table, params):
    query = f''' SELECT * FROM {table} WHERE id = ?'''
    return create_request(query, params)


def get_all_meal_nutriments_request(params):
    query = ''' SELECT kcal, carbohydrates, fats, proteins, amount
        FROM ingredient LEFT JOIN meal_ingredient ON ingredient.id = ingredient_id 
        WHERE meal_id = ? 
        ORDER BY kcal desc '''
    return create_request2(query, params)

def get_all_meal_nutriments_with_tags_request(params):
    query = ''' SELECT kcal, carbohydrates, fats, proteins, amount, tags
        FROM ingredient LEFT JOIN meal_ingredient ON ingredient.id = ingredient_id 
        WHERE meal_id = ? 
        ORDER BY kcal desc '''
    return create_request2(query, params)


def get_all_meal_ids_request():
    query = '''SELECT id FROM meal'''
    return create_request(query)


def get_all_meal_ids_with_classification_and_category_request():
    query = '''SELECT id, classification, category FROM meal'''
    return create_request(query)


def get_meals_classification(id):
    query = '''SELECT classification FROM meal WHERE id = ?'''
    return create_request(query, [id])


def create_request(query, params=''):
    db = get_db()
    cur = db.cursor()

    if params == '':
        cur.execute(query, params)
    else:
        cur.execute(query, [params])
    db.commit()
    return cur


def create_request2(query, params=''):
    db = get_db()
    cur = db.cursor()

    cur.execute(query, params)
    db.commit()
    return cur


def insert_meals(meals):
    for meal in meals:
        params = (meal[0], meal[1], meal[2], meal[3], None)
        insert_or_replace_meal_request(params)


def update_classfication_by_id(id, classfication):
    params = (classfication, id)
    update_meal_classification_request(params)


def insert_ingredients(ingredients):
    for ingr in ingredients:
        params = (ingr[0], ingr[1], ingr[2],
                  ingr[3], ingr[4], ingr[5], ingr[6])
        insert_or_replace_ingredient_request(params)


def insert_meals_ingredients(meals_ingredients):
    for mi in meals_ingredients:
        params = (mi[0], mi[1], mi[2], mi[3], mi[4])
        insert_or_replace_meal_ingredient_request(params)


def find_ingredient_id(name, ingredients):
    for ing in ingredients:
        if ing[1] == name:
            return ing[0]
    return None


def swap_ingredient_name(names, ingredients):
    ingredients_arr = list(ingredients)
    ids = []
    for name in names:
        ids.append(find_ingredient_id(name, ingredients_arr))
    return ids


def sorting_func(x):
    return x[1]


def get_all_meals_with_nutriments():
    ids = np.array(list(get_all_meal_ids_request().fetchall()))[:, 0]
    meals_with_nutriments = []
    for id in ids:
        ingredient_nutriments_arr = list(
            get_all_meal_nutriments_request([str(id)]).fetchall())
        # kcal carbs fats proteins
        all_meal_nutriments = [0, 0, 0, 0]

        for ingredient in ingredient_nutriments_arr:
            amount = ingredient[4]
            nutriments = np.array(
                [ingredient[0]*amount, ingredient[1]*amount, ingredient[2]*amount, ingredient[3]*amount])
            all_meal_nutriments += nutriments

        meals_with_nutriments.append(
            [id, all_meal_nutriments[0], all_meal_nutriments[2], all_meal_nutriments[1], all_meal_nutriments[3], get_meals_classification(id).fetchall()])
        # kcal fats carbs proteins
    return sorted(meals_with_nutriments, key=sorting_func, reverse=True)


def get_all_meals_with_nutriments_and_classification():
    data = np.array(
        list(get_all_meal_ids_with_classification_and_category_request().fetchall()))
    ids = data[:, 0]
    results = data[:, 1]
    categories = data[:, 2]

    meals_with_nutriments = []
    for id, result, category in zip(ids, results, categories):
        ingredient_nutriments_with_tags_arr = list(
            get_all_meal_nutriments_with_tags_request([str(id)]).fetchall())
        # kcal carbs fats proteins
        all_meal_nutriments = [0, 0, 0, 0]
        all_tags = []

        for ingredient in ingredient_nutriments_with_tags_arr:
            amount = ingredient[4]
            tags = ingredient[5]
            nutriments = np.array(
                [ingredient[0]*amount, ingredient[1]*amount, ingredient[2]*amount, ingredient[3]*amount])
            all_meal_nutriments += nutriments
            if tags != '':
                all_tags.append(tags)

        all_tags = list(dict.fromkeys(all_tags))

        meals_with_nutriments.append(
            {
                "id": id,
                "kcal": all_meal_nutriments[0],
                "fats": all_meal_nutriments[2],
                "carbohydrates": all_meal_nutriments[1],
                "proteins": all_meal_nutriments[3],
                "result": result,
                "preferences": all_tags,
                "category": category
            }
        )

    # for m in meals_with_nutriments:
    #     print(m)

        # kcal fats carbs proteins
    return meals_with_nutriments
