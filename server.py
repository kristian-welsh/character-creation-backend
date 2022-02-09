from flask import Flask, request
from flask_cors import CORS, cross_origin
import pymongo
from pymongo import MongoClient


app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/endpoint", methods=['POST'])
@cross_origin()
def endpoint():
    print(str(request.data))

    print("json")
    print(str(request.get_json()))
    print(str(request.get_json()["name"]))
    req_dict = str(request.get_json())

    database = CallDatabase("127.0.0.1", "27017", "/app")
    database.connect()
    database.store_data("character_name", req_dict["name"])
    database.disconnect()

    name = req_dict["name"]

    return '{ "message": "its really actually worked" }'

class CallDatabase:

    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
    def connect(self):
        client = MongoClient(self.host, self.port)
        db = client.app

    def store_data(self, key, value):
        pass

    def disconnect(self):
        pass
