import json
import pickle
import os


class FileHandler():

    @staticmethod
    def load_file(file_path, mode="r", encoding=None):
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
            FileHandler.file_not_found_to_controller.emit(file_path)
        except Exception as e:
            print(f"An error occurred: {e}")
