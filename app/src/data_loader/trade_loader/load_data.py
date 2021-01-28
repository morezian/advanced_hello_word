from app.src.data_loader.trade_loader.csv_loader import *
from app.src.data_loader.trade_loader.telegram_loader import *
from collections import defaultdict


class LoadData:
    def __init__(self):
        self.__csv_loader = CsvLoader()
        self.__all_tel_loader = TelegramLoader(token="1483369722:AAFQJOLnQeKZd5QjRD4wiI6pfAqoOu-m0Rk", id ="-444966767")
        self.__super_tel_loader =TelegramLoader(token="1370460089:AAHda25aodvumQO98eR50tnvVouohJ3_VlY", id="-412898183", is_special = True)
        self.__strong_tel_loader = TelegramLoader(token="1486040039:AAEDA2JVfpu14VbCWhYdV8mShlyYYoGHPrU", id="-408293635", is_special = True)
        self.__vip_loader = TelegramLoader (token="1433676948:AAGJuVmoDH9jsdPYJ1-iEi3JK3Bivl3HhzM", id="-348825048", is_special=True)
        self.__stock_name2last_sent_timestamp = {}
        self.__stock_name2last_sent_buy_sell_status = {}
        cfg = json.load(open("config"))
        realtime = cfg ["realtime"]
        if realtime == True:
            self.__MIN_SECOND_BETWEEN_SENTS = 30
        else: #reading from csv
            self.__MIN_SECOND_BETWEEN_SENTS = 0
        self.__stock2loader_list = {}


    def __get_loader_list(self, stock:Stock, vip_stock_list):
        loader_list = []
        current_buy_sell_status = stock.current_buy_sell_status_dict["all"]
        last_buy_sell_status = self.__stock_name2last_sent_buy_sell_status.get(stock.name)
        if last_buy_sell_status:
            interval_stock = current_buy_sell_status - last_buy_sell_status
        else:
            interval_stock = current_buy_sell_status
        if interval_stock.is_significant() == False:
            return []
        last_time_stamp = self.__stock_name2last_sent_timestamp.get (stock.name)
        if last_time_stamp:
            if time() - last_time_stamp < self.__MIN_SECOND_BETWEEN_SENTS:
                return []
        score_level = stock.score_level
        if score_level == Filter.SUPER:
            loader_list.append (self.__super_tel_loader)
            if stock not in vip_stock_list:
                vip_stock_list.append (stock)
        elif score_level == Filter.STRONG:
            loader_list.append(self.__strong_tel_loader)
        elif score_level >= Filter.GOOD:
            loader_list.append(self.__all_tel_loader)
        loader_list.append(self.__csv_loader)
        if stock in vip_stock_list:
            loader_list.append(self.__vip_loader)
        self.__stock_name2last_sent_buy_sell_status[stock.name] = current_buy_sell_status
        self.__stock_name2last_sent_timestamp[stock.name] = time()
        return loader_list




    def update_loader (self, stock, vip_stock_list):
        loader_list = self.__get_loader_list(stock, vip_stock_list)
        self.__stock2loader_list [stock] = loader_list


    def load (self):
        loader2stock_list = defaultdict (list)
        for stock, loader_list in self.__stock2loader_list.items():
            for loader in loader_list:
                loader2stock_list [loader].append(stock)

        for loader, stock_list in loader2stock_list.items():
            stock_list.sort()
            print (len (stock_list))
            Factor = 10
            for i in range (len (stock_list)//Factor +1):
                tmp_list = stock_list[i*Factor:min((i+1)*Factor, len(stock_list))]
                if len (tmp_list):
                    loader.load_stock_list (tmp_list)
                #for stock in stock_list:
                #    loader.load_stock(stock)

        self.__stock2loader_list = {}
