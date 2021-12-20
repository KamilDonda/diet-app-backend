class IngredientEntity:
    def __init__(self, id, name, kcal, carbohydrates, fats, proteins, tags):
        self.id = id
        self.name = name
        self.kcal = kcal
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.proteins = proteins
        self.tags = tags

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'kcal': self.kcal,
            'carbohydrates': self.carbohydrates,
            'fats': self.fats,
            'proteins': self.proteins,
            'tags': self.tags,
        }
