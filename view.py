from flask import Flask
from flask_restful import Resource, Api, request
from app.src.flask_interfaces.status_interface import *
from app.src.flask_interfaces.AngularAPI.stock_info import *
from flask_cors import CORS

app = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})


cors = CORS(app, resources={r"/*": {"origins":["http://localhost:4200"]}},supports_credentials=True)

api = Api(app)

#api.add_resource(StatusInterface, '/status')
api.add_resource(StockInfo, '/stockInfo')

"""@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response"""