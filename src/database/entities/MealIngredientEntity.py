class MealIngredientEntity:
    def __init__(self, id, meal_id, ingredient_name, description, amount):
        self.id = id
        self.meal_id = meal_id
        self.ingredient_name = ingredient_name
        self.description = description
        self.amount = amount
