class MealIngredientEntity:
    def __init__(self, id, ingredient_id, meal_id, description, amount):
        self.id = id
        self.ingredient_id = ingredient_id
        self.meal_id = meal_id
        self.description = description
        self.amount = amount

    def serialize(self):
        return {
            'id': self.id,
            'ingredient_id': self.ingredient_id,
            'meal_id': self.meal_id,
            'description': self.description,
            'amount': self.amount
        }
