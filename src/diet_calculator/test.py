import input
import calc as calc

user_calories, user_proteins, user_fats, user_carbs, preferences = input.calcInput(
    True, 22, 70, 175, 2, 2, 'Preferences')

print(calc)

result = calc.get_user_classification(user_calories)
print("User classification:", result)
