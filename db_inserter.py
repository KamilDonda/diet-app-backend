import csv
import numpy as np
from db import get_all_meals_with_nutriments, insert_ingredients, insert_meals, insert_meals_ingredients, select_all_from_table_request, swap_ingredient_name, get_db
from app import init_db


def open_file(filename):
    tsv_file = open(filename, encoding="utf8")
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    return read_tsv 


def main():
    conn = get_db()
    with conn:
        meals = open_file('inserter_files/meal.tsv')
        ingredients = list(open_file('inserter_files/ingredient.tsv'))
        meals_ingredients = open_file('inserter_files/relation.tsv')
        meals_ingredients_arr = np.array(list(meals_ingredients))

        meals_ingredients_arr[:, 1] = swap_ingredient_name(
            meals_ingredients_arr[:, 1], ingredients)

        insert_meals(meals)
        print('Inserted meals')
        insert_ingredients(ingredients)
        print('Inserted ingredients')
        insert_meals_ingredients(meals_ingredients_arr)
        print('Inserted meals_ingredients_arr')

        # all_meals = select_all_from_table_request('meal').fetchall()
        # print(all_meals)

        # all_ingredients = select_all_from_table_request(
        #     'ingredient').fetchall()
        # print(all_ingredients)

        # all_meal_ingredients = select_all_from_table_request(
        #     'meal_ingredient').fetchall()
        # print(all_meal_ingredients)

        # meals_with_nutriments = get_all_meals_with_nutriments()
        # print(meals_with_nutriments)


if __name__ == '__main__':
    init_db()
    main()
