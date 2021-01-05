from app.src.stock.stock import *
# from app.src.data_reader.crawler import crawl_data
# from app.src.data_reader.history_crawler import *
from app.src.data_loader.filter_and_load import *
from app.src.loggers.file_logger import *
from time import time, sleep
from datetime import datetime
from app.src.data_reader.vip_stock_reader import *
from app.src.data_reader.crawler import DataCrawler
TESTING = True

#crawler = DataCrawler(crawl_history = False,realtime=False,csv_file='app/data/data/1608974824.csv')
crawler = DataCrawler(crawl_history = True, realtime=True) # gets realtime data
print ("crawler created")
#get_stock_name2history()

sorted_history = [(y.get_median_human_buy_power_ratio, x) for x, y in crawler.history.items()]

sorted_history.sort(reverse=True)


while True:
    if not TESTING and datetime.now().hour != 9: continue
    #initialzie paramters
    load_data = FiliterAndLoad()
    stock_name2history = {}
    stock_name2stock_obj = {}
    cnt = 0
    while (datetime.now().hour != 13):
        start_time = time( )
        data_list = crawler.crawl_data()
        print (f"read in {time () - start_time} seconds")
        cnt += len (data_list)
        #print (f"read {cnt} in {time () - start_time} seconds")
        #start_time = time ()
        for data in data_list:
            if data.name not in stock_name2stock_obj:
                stock = Stock(data.name, latin_name = data.latin_name, retrieve_prevois_second_list= [5*60], max_interval_list_length= 1000, stock_history=data.histored_data)
                stock_name2stock_obj[data.name] = stock
            stock = stock_name2stock_obj[data.name]
            stock.update(data.current_buy_sell_status)
            #print("updated")
        vip_stock_list = get_vip_stock_list(stock_name2stock_obj)
        for _, stock in stock_name2stock_obj.items():
            load_data.update_loader(stock, vip_stock_list)
            #print ("2update")

        #print("loaded")
        load_data.load()