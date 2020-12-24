from app.src.stock.stock import *
from app.src.DataReader.crawler import crawl_data
from app.src.DataReader.history_crawler import get_stock_name2history

stock_name2history = get_stock_name2history()
stock_name2stock_obj = {}



while True:

    data_list = crawl_data()
    for data in data_list:
        if data.name not in stock_name2stock_obj:
            stock = Stock(data.name, retrieve_interval_cps_list=[1, 5, 15, 30],stock_history=stock_name2history.get (data.name))
            stock_name2stock_obj[data.name] = stock
        stock = stock_name2stock_obj[data.name]
        stock.set_current_buy_sell_status(data.current_buy_sell_status)
        stock.store_data()