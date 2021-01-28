import json
import flask
from flask_restful import Resource, Api, request
from app.src.stock.stocks_manager import *
from app.src.data_reader.crawler import *
from app.src.data_loader.status_loader.telegram_loader import *
from datetime import timedelta

class StockInfo(Resource):

    def post(self):
        start_time = time()
        input = json.loads(request.data)