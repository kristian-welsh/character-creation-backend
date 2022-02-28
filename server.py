from flask import Flask, request
from flask_cors import CORS, cross_origin
import pymongo
from pymongo import MongoClient

IP = "127.0.0.1"
PORT = 27017

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/endpoint", methods=['POST'])
@cross_origin()
def endpoint():
    
    print("Endpoint reached.")
    req_dict = request.get_json()

    database = CallDatabase(IP, PORT, "/app")
    database.connect()
    id = database.store_data("character_name", req_dict["name"])
    print(id)
    database.disconnect()

    return '{ "_id": "' + str(id) + '" }'

class CallDatabase:

    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
    def connect(self):
        self.client = MongoClient(self.host, self.port)
        self.db = self.client.app

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
