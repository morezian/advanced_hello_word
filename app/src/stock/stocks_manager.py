from app.src.data_loader.trade_loader.load_data import *
from time import time
from app.src.data_reader.vip_stock_reader import *
from app.src.data_reader.crawler import DataCrawler


class StocksManager:
    def __init__(self, crawler: DataCrawler, loader):
        self.__load_data = loader
        self.__stock_name2stock_obj = {}
        self.__vip_stock_list = []
        self.__crawler = crawler

    def __get_stock(self, data):
        if data.name not in self.__stock_name2stock_obj:
            stock = Stock(data.name, latin_name=data.latin_name, retrieve_prevois_second_list=[5 * 60],
                          max_interval_list_length=1000, stock_history=self.__crawler.history.get(data.name))
            self.__stock_name2stock_obj[data.name] = stock
        stock = self.__stock_name2stock_obj[data.name]
        return stock

    def get_stock(self, persian_name):
        return self.__stock_name2stock_obj.get(persian_name)

    def update(self):
        start_time = time()
        data_list = self.__crawler.crawl_data()
        #print (f"read in {time () - start_time} seconds")
        for data in data_list:
            stock = self.__get_stock(data)
            stock.update(data.current_buy_sell_status)

    def load(self):
        stored_vip_stock_list = get_vip_stock_list(self.__stock_name2stock_obj)
        for vip_stock in stored_vip_stock_list:
            if vip_stock not in self.__vip_stock_list:
                self.__vip_stock_list.append(vip_stock)
        for _, stock in self.__stock_name2stock_obj.items():
            self.__load_data.update_loader(stock, self.__vip_stock_list)
        self.__load_data.load()
