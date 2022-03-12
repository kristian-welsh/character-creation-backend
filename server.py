from flask import Flask, request
from flask_cors import CORS, cross_origin
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Mongo docker container IP
IP = "172.17.0.2"
PORT = 27017

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

print("server.py defining endpoint")
@app.route("/endpoint", methods=['POST'])
@cross_origin()
def endpoint():
    
    print("Endpoint reached.")
    req_dict = request.get_json()

    try:
        database = CallDatabase(IP, PORT, "/app")
        database.connect()
        print("Connected to database")
        print("QQQQQ Starting data query")
        id = database.store_data("character_name", req_dict["name"])
        print("Finishing data query here")
        print(id)
        database.disconnect()
        print("Disconnected from database")
    except:
        print("Couldn't connect to database")

    print("responding to request")
    return '{ "_id": "' + str(id) + '" }'
    #return '{ "_id": "1234567890" }'

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

    def disconnect(self):
        self.client.close()
