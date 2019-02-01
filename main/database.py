import pymongo

class Connection:
    """Connection to the EnterpRyze database"""

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["enterpryze"]
        self.users = self.db['users']
        self.servers = self.db['servers']
        # Debugging
        print('Connected to EnterpRyze MongoDB (pymongo v' + pymongo.version + ')')
        collection_list = self.db.list_collection_names()
        if "users" in collection_list:
            print('Users collection found.')
        if "servers" in collection_list:
            print('Servers collection found.')

    # User functions
    def get_user(self, discord_id):
        """Returns user from the database with their Discord user id. Creates and returns new user if nothing is found."""
        user = self.users.find_one({"id": discord_id})
        if user is None:
            print('[DATABASE]: User', discord_id, 'not found. Creating new user.')
            user = self.users.find_one({"_id": self.new_user(discord_id)})
        # else:
        #     print('[DATABASE]: User', discord_id, 'found.')
        return user

    def new_user(self, discord_id):
        """Creates a new user with their Discord user id and default settings."""
        return self.users.insert_one({"id": discord_id, "xp": 0})
        print('[DATABASE]: User', discord_id, 'updated.')

    def update_user(self, discord_id, key, value, operation="set"):
        self.users.update_one({"id": discord_id}, {"$"+operation: {key: value}})

    # Server functions
    def get_server(self, server_id):
        """Returns server from the database with its server id. Creates and returns new server if nothing is found."""
        server = self.servers.find_one({"id": server_id})
        if server is None:
            print('[DATABASE]: Server', server_id, 'not found. Creating new server.')
            server = self.servers.find_one({"_id": self.new_server(server_id).inserted_id})
        # else:
        #     print('[DATABASE]: Server', server_id, 'found.')
        return server

    def new_server(self, server_id):
        """Creates a new server with its server id and default settings."""
        return self.servers.insert_one({"id": server_id, "welcome_channel": None, "bot_channel": None, "admins": []})

    def update_server(self, server_id, key, value, operation="set"):
        self.servers.update_one({"id": server_id}, {"$"+operation: {key: value}})
        print('[DATABASE]: Server', server_id, 'updated.')

    