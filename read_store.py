from app.src.stock.stock import *
from app.src.data_reader.crawler import crawl_data
from app.src.data_reader.history_crawler import get_stock_name2history
from app.src.data_loader.filter_and_load import *

load_data = FiliterAndLoad()


stock_name2history = {}#get_stock_name2history()
stock_name2stock_obj = {}



while True:

    data_list = crawl_data()
    for data in data_list:
        if data.name not in stock_name2stock_obj:
            stock = Stock(data.name, retrieve_prevois_second_list= [5*60], max_interval_list_length= 1000, stock_history=stock_name2history.get (data.name))
            stock_name2stock_obj[data.name] = stock
        stock = stock_name2stock_obj[data.name]
        stock.update(data.current_buy_sell_status)
        load_data.run(stock)