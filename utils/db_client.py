
import pymongo
import certifi

class MongoDBClient:
    def __init__(self, uri, db_name, collection_name):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None

    def connect(self):
        self.client = pymongo.MongoClient(self.uri, tlsCAFile=certifi.where())

    def fetch_data(self):
        try:
            db = self.client[self.db_name]
            collection = db[self.collection_name]
            return list(collection.find())
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return []
