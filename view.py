from flask import Flask
from flask_restful import Resource, Api, request
from app.src.flask_interfaces.status_interface import *
from app.src.flask_interfaces.AngularAPI.stock_info import *

app = Flask(__name__)
api = Api(app)

#api.add_resource(StatusInterface, '/status')
api.add_resource(StockInfo, '/stockInfo')