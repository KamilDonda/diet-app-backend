import input
import calc

user_calories, user_proteins, user_fats, user_carbs = input.calcInput(
    True, 22, 70, 175, 2, 2, 'Preferences')

df = calc.load_data_pandas()

calories = df['Calories']
proteins = df['Protein']
fats = df['Fat']
carbs = df['Carbohydrates']

calories_gauss = calc.gaussian(calories, 'cals')
proteins_gauss = calc.gaussian(proteins, 'prots')
fats_gauss = calc.gaussian(fats, 'fats')
carbs_gauss = calc.gaussian(carbs, 'carbs')

def print_data(data):
    for d in data:
        print(d)

print_data(calories_gauss)
print_data(proteins_gauss)
print_data(fats_gauss)
print_data(carbs_gauss)