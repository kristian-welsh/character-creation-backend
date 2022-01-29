from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/endpoint", methods=['POST'])
@cross_origin()
def endpoint():
    print(str(request))
    return '{ "message": "its really actually worked" }'

