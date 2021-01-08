import json
import flask
from flask_restful import Resource, Api, request
from app.src.stock.stocks_manager import *
from app.src.data_reader.crawler import *
from app.src.data_loader.status_loader.telegram_loader import *

def get_file_path_list (time_list):
    return [f"app/data/csv3/{t}.csv" for t in time_list]


class StatusInterface (Resource):

    telegram_loader = TelegramLoader (token='1505119805:AAEX8qArYNbDzjKhCeGr0E3X_xIM_UIkRzk', id="-454149966")

    def post(self):
        input = request.data
        time_list = input.get ("time_list")
        persian_name = input.get ("persian_name")
        file_path_list = get_file_path_list(time_list)
        for file_path in file_path_list:
            crawler = DataCrawler(crawl_history=False, realtime=False,csv_file=file_path)
            data_list = self.__crawler.crawl_data()
            if len (data_list) == 0:
                return {"error": f"There is no data for {persian_name}"}
            stock_manager = StocksManager(crawler)
            stock = stock_manager.get_stock(data_list[0])
            self.telegram_loader.load_stock(stock, data_list)







