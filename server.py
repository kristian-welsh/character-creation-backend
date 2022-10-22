from flask import Flask, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_PORT = 27017

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/endpoint", methods=['POST'])
@cross_origin()
def endpoint():

    print("---------------------------")
    print("Character endpoint reached.")
    print("---------------------------")

    req = request.get_json()

    try:
        database = CallDatabase('localhost', MONGO_PORT, "/app")
        database.connect()
        print("Connected to database")
        print("-- Starting data query --")
        id = database.store_data("character_details", req)
        print("-- Finishing data query here --")
        print(id)
        all_contents = database.temp_all_contents()
        database.disconnect()
        print("Disconnected from database")
    except:
        print("Couldn't connect to database")

    print("responding to request")
    return '{ "_id": "' + str(id) + '", "db_contents": "' + str(all_contents) + '" }'


class CallDatabase:

    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name

    def connect(self):
        print("connecting to database")
        self.client = MongoClient(self.host, self.port)
        self.check_connection()
        self.db = self.client.app
        print(self.db)

    def check_connection(self):
        try:
            # Blocks until connection established
            self.client.admin.command('ping')
            print("Database avaliable")
        except ConnectionFailure:
            print("Database not avaliable")

    def store_data(self, key, value):
        new_cl = self.db["character_sheets"]
        try:
            result = new_cl.insert_one({
                key: value
            })
            return result.inserted_id
        except Exception as e:
            print(e)
            print("Failed to add data to the collection.")
        return -1

    def temp_all_contents(self):
        new_cl = self.db["character_sheets"]
        try:
            results = []
            for i in new_cl.find():
                results.append(i)
            return results
        except Exception as e:
            print(e)
            print("Failed to find data from the collection.")
        return -1

    def disconnect(self):
        self.client.close()
