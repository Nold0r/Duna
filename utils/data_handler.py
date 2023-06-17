import json


class DataHandler:
    @staticmethod
    def load_data():
        with open("./data/data.json", "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def save_data(data):
        with open("./data/data.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=1)
