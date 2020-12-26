from app.src.stock.stock import *
from app.src.data_reader.crawler import crawl_data
from app.src.data_reader.history_crawler import get_stock_name2history
from app.src.data_loader.filter_and_load import *
from app.src.loggers.file_logger import *
from time import time, sleep
from datetime import datetime

TESTING = True


load_data = FiliterAndLoad()


stock_name2history = {}#get_stock_name2history()
stock_name2stock_obj = {}


while True:
    if not TESTING and datetime.now().hour != 9: continue
    while (datetime.now().hour != 13):
        start_time = time( )
        data_list = crawl_data()
        print (f"1read in {time () - start_time} seconds")
        #start_time = time ()
        for data in data_list:
            if data.name == "غزر":
                x = 2
            if data.name not in stock_name2stock_obj:
                stock = Stock(data.name, retrieve_prevois_second_list= [5*60], max_interval_list_length= 1000, stock_history=stock_name2history.get (data.name))
                stock_name2stock_obj[data.name] = stock
            stock = stock_name2stock_obj[data.name]
            stock.update(data.current_buy_sell_status)
            #print("updated")
            load_data.update_loader(stock)
            print ("2update")

        #print("loaded")
        load_data.load()
        print ("3load**************")
        #sleep(10)


    #print(f"processed {len(data_list)} records in {int (time() - start_time)} seconds")