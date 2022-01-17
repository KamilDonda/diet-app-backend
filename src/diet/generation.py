from calc import get_user_classification
import random

from Meal import Meal, dictToMeal, DaySum


class DietGeneration():
    def setup_allowed_goals(self):
        allowed_goals = ['-1', '0', '1']
        u_goal = get_user_classification(self.u_cal)
        # print('u_goal', u_goal)
        if u_goal == -1:
            allowed_goals.remove('1')
        if u_goal == 1:
            allowed_goals.remove('-1')
        return allowed_goals

    def get_meal_from_list(self, items):
        item = random.choice(items)
        items.remove(item)
        return item

    # def generateDiet(self, meals):
    #     breakfasts = []
    #     dinners = []
    #     suppers = []

    #     allowed_goals = self.setup_allowed_goals(self)

    #     for m in meals:
    #         # if not m['result'] in allowed_goals:
    #         #     continue
    #         if [pref for pref in m['preferences'] if pref in self.u_pref]:
    #             continue
    #         if m['category'] == 'śniadanie':
    #             breakfasts.append(m)
    #         elif m['category'] == 'obiad':
    #             dinners.append(m)
    #         else:
    #             suppers.append(m)

    #     diet = {}
    #     totals = []

    #     days = ['monday', 'tuesday', 'wednesday',
    #             'thursday', 'friday', 'saturday', 'sunday']

    #     for d in days:
    #         breakfast = self.get_meal_from_list(self, breakfasts)
    #         dinner = self.get_meal_from_list(self, dinners)
    #         supper = self.get_meal_from_list(self, suppers)
    #         day = {
    #             'meals': {
    #                 'breakfast': breakfast,
    #                 'dinner': dinner,
    #                 'supper': supper
    #             }
    #         }

    #         kcal = 0
    #         prot = 0
    #         carb = 0
    #         fat = 0
    #         for _, v in day['meals'].items():
    #             kcal += v['kcal']
    #             prot += v['proteins']
    #             carb += v['carbohydrates']
    #             fat += v['fats']
    #         total = {
    #             'kcal': float(format(kcal, '.2f')),
    #             'proteins': float(format(prot, '.2f')),
    #             'carbohydrates': float(format(carb, '.2f')),
    #             'fats': float(format(fat, '.2f'))
    #         }
    #         day['day_total'] = total
    #         diet[d] = day
    #         totals.append(total)

    #     result = {}
    #     for d in totals:
    #         for k in d.keys():
    #             result[k] = result.get(k, 0) + d[k]
    #     diet['week_total'] = result
    #     return diet

    def generateDiet(self, meals):
        breakfasts = []
        dinners = []
        suppers = []

        allowed_goals = self.setup_allowed_goals(self)

        for m in meals:
            # if not m['result'] in allowed_goals:
            #     continue
            if [pref for pref in m['preferences'] if pref in self.u_pref]:
                continue
            if m['category'] == 'śniadanie':
                breakfasts.append(m)
            elif m['category'] == 'obiad':
                dinners.append(m)
            else:
                suppers.append(m)

        diet = []

        for _ in range(7):
            breakfast = dictToMeal(self.get_meal_from_list(self, breakfasts))
            dinner = dictToMeal(self.get_meal_from_list(self, dinners))
            supper = dictToMeal(self.get_meal_from_list(self, suppers))
            day = DaySum(breakfast, dinner, supper)

            diet.append(day)

        return diet

    def __new__(self, user_input, meals):
        self.u_cal, self.u_prot, self.u_fat, self.u_carb, self.u_pref = user_input
        self.meals = meals

        generated_diet = self.generateDiet(self, meals)

        output = [e.serialize() for e in generated_diet]

        return output
