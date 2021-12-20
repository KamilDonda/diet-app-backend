DROP TABLE IF EXISTS ingredient;

CREATE TABLE ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    kcal REAL,
    carbohydrates REAL,
    fats REAL,
    proteins REAL,
    tags TEXT
);

DROP TABLE IF EXISTS meal;

CREATE TABLE meal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    category TEXT,
    classification INTEGER
);

DROP TABLE IF EXISTS diet;

CREATE TABLE diet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    nr_of_meals INTEGER
);

DROP TABLE IF EXISTS meal_ingredient;

CREATE TABLE meal_ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER NOT NULL,
    meal_id INTEGER NOT NULL,
    description TEXT,
    amount REAL,
    FOREIGN KEY (ingredient_id) REFERENCES ingredient (id),
    FOREIGN KEY (meal_id) REFERENCES meal (id)
);

DROP TABLE IF EXISTS diet_meal;

CREATE TABLE diet_meal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id INTEGER NOT NULL,
    diet_id INTEGER NOT NULL,
    FOREIGN KEY (meal_id) REFERENCES meal (id),
    FOREIGN KEY (diet_id) REFERENCES ingredient (id)
);