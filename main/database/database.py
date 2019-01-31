import pymongo

class Connection:

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = client["enterpryze"]
        print('Connected to EnterpRyze MongoDB (pymongo v' + pymongo.version + ')')