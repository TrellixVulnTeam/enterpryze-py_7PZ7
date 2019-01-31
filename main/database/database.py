import pymongo

class Connection:

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["enterpryze"]
        self.users = self.db['users']
        print('Connected to EnterpRyze MongoDB (pymongo v' + pymongo.version + ')')

    def get_user(self, id):
        """Returns user from the database with their Discord user id. Creates and returns new user if nothing is found."""
        user = self.users.find({}, {"id": id})
        print(user)
        if user is None:
            user = self.users.insert_one({"id": id})
        return user
