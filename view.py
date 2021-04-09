from flask import Flask
from flask_restful import Resource, Api, request
from app.src.flask_interfaces.status_interface import *
from app.src.flask_interfaces.AngularAPI.signal import *
from app.src.flask_interfaces.AngularAPI.history import *
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

api = Api(app)

#api.add_resource(StatusInterface, '/status')
api.add_resource(Signal, '/signals')
api.add_resource(History, '/history')