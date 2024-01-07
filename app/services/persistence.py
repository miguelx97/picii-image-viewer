import pickle
from os import path

class Persistence:
    def __init__(self, db_name:str, path:str = '.'):
        self.db_name = db_name
        self.path = path

    def save(self, data: dict):
        with open(path.join(self.path,self.db_name), 'wb') as pkl_file:
            pickle.dump(data, pkl_file)

    def load(self) -> dict:
        if not path.exists(path.join(self.path,self.db_name)):
            return None
        with open(path.join(self.path,self.db_name), 'rb') as pkl_file:
            loaded_data = pickle.load(pkl_file)
        return loaded_data