# BMR = Basal Metabolic Rate
# AMR = Active Metabolic Rate
# Weight in kg
# Height in cm
# Age in years
# Gender: True = man
#         False = woman
# Activity [1, 2, 3, 4, 5]
#           1 - lowest
#           5 - highest
# Goal [1, 2, 3]
#       1 - losing weight
#       2 - constant weight
#       3 - gaining weight
#
# 1g proteins       = 4 kcal
# 1g fats           = 9 kcal
# 1g carbohydrates  = 4 kcal

def calcInput(gender, age, weight, height, activity, goal, preferences):

    BMR = calcBMR(gender, age, weight, height)
    AMR = calcAMR(activity, BMR)
    totalCalories = includeGoal(goal, AMR)

    proteins = calcProteinsNeeded(weight, goal)
    fats = calcFatsNeeded(totalCalories)
    carbs = calcCarbs(totalCalories, proteins, fats)

    # temporary function, only for display input and output
    printResults(gender, age, weight, height, activity, goal,
                 preferences, BMR, AMR, totalCalories, proteins, fats, carbs)
    return totalCalories, proteins, fats, carbs, preferences


def calcBMR(gender, age, weight, height):
    # Mifflin-St Jeor Equation:
    BMR = 10 * weight + 6.25 * height - 5 * age
    if gender:
        BMR += 5
    else:
        BMR -= 161
    return BMR


def calcBMR2(gender, age, weight, height):
    # Revised Harris-Benedict Equation:
    BMR = 0
    if gender:
        BMR = 13.397 * weight + 4.799 * height - 5.677 * age + 88.362
    else:
        BMR = 9.247 * weight + 3.098 * height - 4.330 * age + 447.593
    return BMR


def calcAMR(activity, BMR):
    result = 0

    # Little/no exercise
    if activity == 1:
        result = BMR * 1.2
    # Light exercise
    if activity == 2:
        result = BMR * 1.35
    # Moderate exercise (3-5 days/wk)
    if activity == 3:
        result = BMR * 1.55
    # Very active (6-7 days/wk)
    if activity == 4:
        result = BMR * 1.725
    # Extra active (very active & physical job)
    if activity == 5:
        result = BMR * 1.9

    return result


def includeGoal(goal, AMR):
    result = AMR

    # Losing weight
    if goal == 1:
        result -= 250
    # Gaining weight
    if goal == 3:
        result += 250

    return result


def calcProteinsNeeded(weight, goal):
    if goal == 1:
        return 2 * weight
    if goal == 2:
        return 1.2 * weight
    if goal == 3:
        return 1.6 * weight


def calcFatsNeeded(calories):
    return 0.23 * calories * 0.125


def calcCarbs(calories, proteins, fats):
    P = proteins * 4
    F = fats * 9
    return (calories - F - P) * 0.25


def printResults(gender, age, weight, height, activity, goal, preference, BMR, AMR, totalCalories, proteins, fats, carbs):
    a = ['Gender', 'Age', 'Weight', 'Height', 'Activity', 'Goal', 'Preference']
    b = [gender, age, weight, height, activity, goal, preference]
    c = ['BMR', 'AMR', 'Total cal', 'Proteins', 'Fats', 'Carbs']
    d = [BMR, AMR, totalCalories, proteins, fats, carbs]
    e = ['kcal', 'kcal', 'kcal', 'g', 'g', 'g']
    f = [0, 0, 0, proteins * 4, fats * 9, carbs * 4]
    g = ['', '', '', 'kcal', 'kcal', 'kcal']

    print('\n INPUT')
    for i in range(len(a)):
        print('{0:10} {1}'.format(a[i], b[i]))
    print('\n OUTPUT')
    for i in range(len(c)):
        print('{0:<10} {1:5.0f} {2:5} {3:5.0f} {4}'.format(
            c[i], d[i], e[i], f[i], g[i]))


# Gender, Age, Weight, Height, Activity, Goal, Preferences
# calcInput(True, 22, 70, 175, 2, 2, 'Preferences')
