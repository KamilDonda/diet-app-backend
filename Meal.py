class Meal():
    def __init__(self, id, kcal, proteins, carbohydrates, fats, category, preferences, result):
        self.id = id
        self.kcal = kcal
        self.proteins = proteins
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.category = category
        self.preferences = preferences
        self.result = result

    def serialize(self):
        return {
            "id": self.id,
            "kcal": self.kcal,
            "proteins": self.proteins,
            "carbohydrates": self.carbohydrates,
            "fats": self.fats,
            "category": self.category,
            "preferences": self.preferences,
            "result": self.result
        }


def dictToMeal(dict):
    return Meal(
        dict['id'],
        dict['kcal'],
        dict['proteins'],
        dict['carbohydrates'],
        dict['fats'],
        dict['category'],
        dict['preferences'],
        dict['result']
    )


class Total():
    def __init__(self, kcal, proteins, carbohydrates, fats):
        self.kcal = kcal
        self.proteins = proteins
        self.carbohydrates = carbohydrates
        self.fats = fats

    def serialize(self):
        return {
            "kcal": self.kcal,
            "proteins": self.proteins,
            "carbohydrates": self.carbohydrates,
            "fats": self.fats,
        }


class DaySum():
    def __init__(self, breakfast, dinner, supper):
        kcal = breakfast.kcal + dinner.kcal + supper.kcal
        proteins = breakfast.proteins + dinner.proteins + supper.proteins
        carbohydrates = breakfast.carbohydrates + \
            dinner.carbohydrates + supper.carbohydrates
        fats = breakfast.fats + dinner.fats + supper.fats

        self.breakfast = breakfast
        self.dinner = dinner
        self.supper = supper
        self.total = Total(kcal, proteins, carbohydrates, fats)

    def serialize(self):
        return {
            "breakfast": self.breakfast.serialize(),
            "dinner": self.dinner.serialize(),
            "supper": self.supper.serialize(),
            "total": self.total.serialize()
        }
