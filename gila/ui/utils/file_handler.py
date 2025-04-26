import json
import os
import pickle
import sys


class FileHandler():

    @staticmethod
    def load_file(relative_path, mode="r", encoding=None):
        try:
            filename = os.path.basename(relative_path)
            if not (relative_path.endswith(".pk") or filename == "saved_settings.json"):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(".")
        except Exception:
            base_path = os.path.abspath(".")

        file_path = os.path.join(base_path, relative_path)
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File '{file_path}' not found.")

            with open(file_path, mode, encoding=encoding) as f:
                if file_path.endswith(".json"):
                    return json.load(f)
                elif file_path.endswith(".pk"):
                    return pickle.load(f)
                else:
                    return f.read()
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(f"An error occurred: {e}")
