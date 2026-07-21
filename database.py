import json
import os
import sys


def resource_path(relative_path):
    """
    Normal python ile çalışırken script'in bulunduğu klasörü,
    PyInstaller ile exe'ye çevrildiğinde ise exe'nin içine
    gömülen geçici klasörü (sys._MEIPASS) baz alır.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


DATABASE_FOLDER = resource_path("database")


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
