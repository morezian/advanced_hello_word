# from app.src.data_reader.crawler import crawl_data
# from app.src.data_reader.history_crawler import *
from app.src.data_loader.trade_loader.filter_and_load import *
from time import time
from datetime import datetime
from app.src.data_reader.vip_stock_reader import *
from app.src.data_reader.crawler import DataCrawler
import json
#crawler = DataCrawler(crawl_history = False,realtime=False,csv_file='app/data/Saved_CSV/1609142400.csv')
#crawler = DataCrawler(crawl_history = True, realtime=True) # gets realtime data
#print ("crawler created")
#get_stock_name2history()

#sorted_history = [(y.market_human_buy_power_ratio, x) for x, y in crawler.history.items()]

#sorted_history.sort(reverse=True)

START_BAZAR_HOUR = 9
END_BAZAR_HOUR = 13
CRAWLING_HOUR = 3

def is_in_bazar_time():
    now_hour = datetime.now().hour
    if now_hour >=START_BAZAR_HOUR and now_hour <=END_BAZAR_HOUR:
        return True
    return False


cfg = json.load(open("config"))
TESTING = cfg ["TESTING"]
crawl_history = cfg ["crawl_history"]
real_time = cfg ["realtime"]



def pause_until_hour (hour):
    while True:
        if datetime.now().hour != hour: continue


while True:
    if not is_in_bazar_time() and not TESTING:
        pause_until_hour(CRAWLING_HOUR)
    crawler = DataCrawler(crawl_history=crawl_history, realtime=real_time)  # gets realtime data
    print("crawler created")
    if not is_in_bazar_time() and not TESTING:
        pause_until_hour(START_BAZAR_HOUR)
    #initialzie paramters
    load_data = FiliterAndLoad()
    stock_name2history = {}
    stock_name2stock_obj = {}
    cnt = 0
    vip_stock_list = []
    while (datetime.now().hour != END_BAZAR_HOUR):
        start_time = time( )
        data_list = crawler.crawl_data()
        print (f"read in {time () - start_time} seconds")
        cnt += len (data_list)
        for data in data_list:
            if data.name not in stock_name2stock_obj:
                stock = Stock(data.name, latin_name = data.latin_name, retrieve_prevois_second_list= [5*60], max_interval_list_length= 1000, stock_history=crawler.history.get(data.name))
                stock_name2stock_obj[data.name] = stock
            stock = stock_name2stock_obj[data.name]
            stock.update(data.current_buy_sell_status)
            #print("updated")
        stored_vip_stock_list = get_vip_stock_list(stock_name2stock_obj)
        for vip_stock in stored_vip_stock_list:
            if vip_stock not in vip_stock_list:
                vip_stock_list.append(vip_stock)
        for _, stock in stock_name2stock_obj.items():
            load_data.update_loader(stock, vip_stock_list)
            #print ("2update")

        #print("loaded")
        load_data.load()