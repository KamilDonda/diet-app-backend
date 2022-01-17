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

        output = [e.get_ids() for e in generated_diet]

        # output = [e.serialize() for e in generated_diet]

        # kcal = 0
        # proteins = 0
        # carbohydrates = 0
        # fats = 0
        # for day in generated_diet:
        #     kcal += day.total.kcal
        #     proteins += day.total.proteins
        #     carbohydrates += day.total.carbohydrates
        #     fats += day.total.fats

        # total = {
        #     "kcal": kcal,
        #     "proteins": proteins,
        #     "carbohydrates": carbohydrates,
        #     "fats": fats
        # }

        # user_i = {
        #     "kcal": user_input[0] * 7,
        #     "proteins": user_input[1] * 7,
        #     "carbohydrates": user_input[3] * 7,
        #     "fats": user_input[2] * 7
        # }

        # print(total)
        # print(user_i)


        return output
