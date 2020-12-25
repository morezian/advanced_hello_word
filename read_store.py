from app.src.stock.stock import *
from app.src.data_reader.crawler import crawl_data
from app.src.data_reader.history_crawler import get_stock_name2history
from app.src.data_loader.filter_and_load import *
from app.src.loggers.file_logger import *
from time import time
from datetime import datetime

load_data = FiliterAndLoad()


stock_name2history = {}#get_stock_name2history()
stock_name2stock_obj = {}


while True:
    if datetime.now().hour != 9: continue
    while (datetime.now().hour != 13):
        data_list = crawl_data()
        #start_time = time ()
        for data in data_list:
            if data.name not in stock_name2stock_obj:
                stock = Stock(data.name, retrieve_prevois_second_list= [5*60], max_interval_list_length= 1000, stock_history=stock_name2history.get (data.name))
                stock_name2stock_obj[data.name] = stock
            stock = stock_name2stock_obj[data.name]
            stock.update(data.current_buy_sell_status)
            #print("updated")
            load_data.run(stock)
        #print("loaded")


    #print(f"processed {len(data_list)} records in {int (time() - start_time)} seconds")