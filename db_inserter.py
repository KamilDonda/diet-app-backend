import sqlite3
from sqlite3 import Error
import csv


DATABASE = 'src\\database\\database.db'


def get_db():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)

    return conn


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


def open_file(filename):
    tsv_file = open(filename, encoding="utf8")
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    return read_tsv
    # for row in read_tsv:
    #     print(row[0])


def insert_meals(meals):
    for meal in meals:
        category = meal[3]
        if category == 'śniadanie':
            category = 'breakfast'
        if category == 'obiad':
            category = 'dinner'
        if category == 'kolacja':
            category = 'supper'
        params = (meal[0], meal[1], meal[2], category)
        insert_or_replace_meal_request(params)


def insert_ingredients(ingredients):
    for ingr in ingredients:
        params = (ingr[0], ingr[1], ingr[2], ingr[3], ingr[4], ingr[5])
        insert_or_replace_ingredient_request(params)


def insert_meals_indredients(meals_ingredients):
    for mi in meals_ingredients:
        params = (mi[0], mi[1], mi[2], mi[3], mi[4])
        insert_or_replace_meal_indredient_request(params)


def main():
    conn = get_db()
    with conn:
        meals = open_file('inserter_files/meal.tsv')
        ingredients = open_file('inserter_files/ingredient.tsv')
        meals_ingredients = open_file('inserter_files/relation.tsv')

        # insert_meals(meals)
        # insert_ingredients(ingredients)
        # insert_meals_indredients(meals_ingredients)

        # all_meals = select_all_from_table('meal').fetchall()
        # print(all_meals)

        # all_meals = select_all_from_table('ingredient').fetchall()
        # print(all_meals)

        # all_meals = select_all_from_table('meal_indredient').fetchall()
        # print(all_meals)


if __name__ == '__main__':
    main()
