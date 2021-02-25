import json
import flask
from flask_restful import Resource, Api, request
from app.src.stock.stocks_manager import *
from app.src.data_reader.crawler import *
from app.src.data_loader.status_loader.telegram_loader import *
from datetime import timedelta
def get_file_path_list (time_list):
    return [f"app/data/csv3/{t}.csv" for t in time_list]

def get_date_list(time_list):
    date_list = [datetime.strptime(t,"%d_%m_%Y") for t in time_list]
    return date_list



def get_stock_manager (crawl_history):
    crawler = DataCrawler(crawl_history=crawl_history,realtime=True)
    stock_manager = StocksManager(crawler, LoadData())
    stock_manager.update()
    return stock_manager

class StatusInterface (Resource):
    cfg = json.load(open("config"))
    crawl_history = cfg ["crawl_history"]
    telegram_loader = TelegramLoader (token='1505119805:AAEX8qArYNbDzjKhCeGr0E3X_xIM_UIkRzk', id="-454149966")
    stock_manager = get_stock_manager(crawl_history)
    def post(self):
        start_time = time()
        input = json.loads(request.data)
        time_list = input.get ("time_list")
        persian_name = input.get ("persian_name")
        persian_name = persian_name.replace ("#", "")
        persian_name = persian_name.replace("_", "")
        persian_name.strip()
        stock = self.stock_manager.get_stock(persian_name)
        if stock == None:
            flask.abort(404, f"There is no Share Called {persian_name}")
        file_path_list = get_file_path_list(time_list)
        date_list = get_date_list(time_list)
        for i,file_path in enumerate(file_path_list):
            stock.clear()
            crawler = DataCrawler(crawl_history=self.crawl_history, realtime=False,csv_file=file_path,stock_name=persian_name)
            data_list = crawler.crawl_data()#batch_size is 10000 and all of them came in one result
            self.telegram_loader.load_stock(stock, [data.current_buy_sell_status for data in data_list], date_list[i])
        print (f"{time() - start_time} seconds")






