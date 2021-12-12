from src.diet_calculator.calc import get_user_classification
import random


class DietGeneration():

    def setup_allowed_goals(self):
        allowed_goals = [-1, 0, 1]
        u_goal = get_user_classification(self.u_cal)
        if u_goal == -1:
            allowed_goals.remove(1)
        if u_goal == 1:
            allowed_goals.remove(-1)
        return allowed_goals

    def get_meal_from_list(self, items):
        item = random.choice(items)
        items.remove(item)
        return item

    def __new__(self, user_input, meals):
        self.u_cal, self.u_prot, self.u_fat, self.u_carb, self.u_pref = user_input
        self.meals = meals

        breakfasts = []
        dinners = []
        suppers = []

        allowed_goals = self.setup_allowed_goals(self)

        for m in meals:
            if not m['result'] in allowed_goals:
                continue

            if [pref for pref in m['preferences'] if pref in self.u_pref]:
                continue
            if m['category'] == 'śniadanie':
                breakfasts.append(m)
            elif m['category'] == 'obiad':
                dinners.append(m)
            else:
                suppers.append(m)

        diet = []

        breakfast = self.get_meal_from_list(self, breakfasts)
        dinner = self.get_meal_from_list(self, dinners)
        supper = self.get_meal_from_list(self, suppers)
        diet.append({
            'breakfast': breakfast,
            'dinner': dinner,
            'supper': supper
        })

        foo = []
        res = ''
        for d in diet:
            kcal = 0
            prot = 0
            carb = 0
            fat = 0
            for k,v in d.items():
                # print(k, v)
                res += str(k) + ' ' + str(v) + '\n'
                foo.append({k: v})
                kcal += v['cal']
                prot += v['proteins']
                carb += v['carbohydrates']
                fat  += v['fat']
            res += str(kcal) + 'kcal ' + str(prot) + 'g ' +  str(carb) + 'g ' +  str(fat) + 'g'
            foo.append({'kcal': kcal, 'proteins': prot, 'carbohydrates': carb, 'fat': fat})
            # print(kcal, prot, carb, fat)
        return foo
        # print(diet[0])

        # for b in breakfasts:
        # print(b)
        # print()
        # for d in dinners:
        # print(d)
        # print()
        # for s in suppers:
        # print(s)
