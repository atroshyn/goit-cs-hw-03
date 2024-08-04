from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

# Підключення до MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['cat_database']
collection = db['cats']

# Функція для виведення всіх записів із колекції
def read_all_cats():
    cats = collection.find()
    for cat in cats:
        pprint.pprint(cat)

# Функція для виведення інформації про кота за ім'ям
def read_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        pprint.pprint(cat)
    else:
        print(f"Cat with name {name} not found.")

# Функція для оновлення віку кота за ім'ям
def update_cat_age(name, new_age):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count:
        print(f"Updated age of {name} to {new_age}.")
    else:
        print(f"Cat with name {name} not found.")

# Функція для додавання нової характеристики до списку features кота за ім'ям
def add_feature_to_cat(name, feature):
    result = collection.update_one({"name": name}, {"$push": {"features": feature}})
    if result.matched_count:
        print(f"Added feature '{feature}' to {name}.")
    else:
        print(f"Cat with name {name} not found.")

# Функція для видалення запису з колекції за ім'ям тварини
def delete_cat_by_name(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"Deleted cat with name {name}.")
    else:
        print(f"Cat with name {name} not found.")

# Функція для видалення всіх записів із колекції
def delete_all_cats():
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} cats.")

# Демонстрація функціоналу
if __name__ == "__main__":
    # Додавання тестових даних
    collection.insert_many([
        {"name": "barsik", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]},
        {"name": "murzik", "age": 5, "features": ["грайливий", "чорний"]}
    ])

    print("All cats:")
    read_all_cats()
    print()

    print("Information about 'barsik':")
    read_cat_by_name("barsik")
    print()

    print("Updating age of 'barsik' to 4:")
    update_cat_age("barsik", 4)
    read_cat_by_name("barsik")
    print()

    print("Adding feature 'грайливий' to 'barsik':")
    add_feature_to_cat("barsik", "грайливий")
    read_cat_by_name("barsik")
    print()

    print("Deleting 'murzik':")
    delete_cat_by_name("murzik")
    read_all_cats()
    print()

    print("Deleting all cats:")
    delete_all_cats()
    read_all_cats()
