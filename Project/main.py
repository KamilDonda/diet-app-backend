import input
import calc

calories, proteins, fats, carbs = input.calcInput(True, 22, 70, 175, 2, 2, 'Preferences')

df = calc.load_data_pandas()
print(df)