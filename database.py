import json
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE_FOLDER = os.path.join(BASE_PATH, "database")


def load_database(filename):
    path = os.path.join(DATABASE_FOLDER, filename)

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return []


gpus = load_database("gpus.json")
cpus = load_database("cpus.json")
motherboards = load_database("motherboards.json")
rams = load_database("ram.json")