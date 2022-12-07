from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import json_util

MONGO_PORT = 27017

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/endpoint", methods=['GET', 'POST'])
@cross_origin()
def endpoint():
    if request.method == 'POST':
        print("--------------------------------")
        print("Post character endpoint reached.")
        print("--------------------------------")

        req = request.get_json()

        try:
            database = CallDatabase('localhost', MONGO_PORT, "/app")
            database.connect()
            print("- Connected to database")
            print(req)
            id = database.store_data("character_details", req)
            print("- Finished data query")
            print(id)
            database.disconnect()
            print("- Disconnected from database")
            response = {
                "_id": str(id)
            }
            return jsonify(response)
        except:
            print("- Database connection failed somewhere")
            return "Database connection failed somewhere"

    if request.method == 'GET':
        print("------------------------------------")
        print("Get all characters endpoint reached.")
        print("------------------------------------")

        try:
            database = CallDatabase('localhost', MONGO_PORT, "/app")
            database.connect()
            print("- Connected to database")
            all_contents = database.log_all_data()
            database.disconnect()
            print("- Disconnected from database")
            print(all_contents)
            return all_contents
        except:
            print("- Database connection failed somewhere")
            return "Database connection failed somewhere"


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
            return new_cl.insert_one({key: value}).inserted_id
        except Exception as e:
            print(e)
            print("Failed to add data to the collection.")
        return -1

    def log_all_data(self):
        new_cl = self.db["character_sheets"]
        try:
            results = [doc for doc in new_cl.find()]
            return json_util.dumps({'characterSheets': results})
        except Exception as e:
            print(e)
            print("Failed to find data from the collection.")
        return -1

    def disconnect(self):
        self.client.close()
