from app.src.stock.filter import *
from app.src.data_loader.csv_loader import *
from app.src.data_loader.telegram_loader import *
from collections import defaultdict


class FiliterAndLoad:
    def __init__(self):
        self.__csv_loader = CsvLoader()
        self.__all_tel_loader = TelegramLoader(token="1483369722:AAFQJOLnQeKZd5QjRD4wiI6pfAqoOu-m0Rk", id ="-444966767")
        self.__super_tel_loader =TelegramLoader(token="1370460089:AAHda25aodvumQO98eR50tnvVouohJ3_VlY", id="-412898183")
        self.__strong_tel_loader = TelegramLoader(token="1486040039:AAEDA2JVfpu14VbCWhYdV8mShlyYYoGHPrU", id="-408293635")
        self.__stock_name2last_sent_timestamp = {}
        self.__stock_name2last_sent_buy_sell_status = {}
        self.__MIN_SECOND_BETWEEN_SENTS = 30
        self.__stock2loader_list = {}



    def get_score (self, f:Filter, is_real, is_interval):
        ans = (f.human_buy_count(is_real, is_interval) + f.avg_buy_per_code(is_real, is_interval) + \
              2*f.buy_power_ratio(is_real, is_interval) + f.trade_price())/5
        return ans


    def get_score_level (slef, score):
        if score >= Filter.STRONG:
            return Filter.SUPER
        if score >= Filter.GOOD:
            return Filter.STRONG
        if score >= Filter.NORMAL:
            return Filter.GOOD
        if score >= Filter.WEAK:
            return Filter.NORMAL
        else:
            return Filter.WEAK


    def get_total_strength (self, f:Filter):
        score_list = [self.get_score(f,False, False),
        self.get_score(f, False, True),
        self.get_score(f, True, False),
        self.get_score(f, True, True)]
        max_score = max(score_list)
        score_level_list = [self.get_score_level(score) for score in score_list]
        max_score_level = max (score_level_list)
        avg_score_level = self.get_score_level (sum (score_list)/len (score_list))
        return max_score_level, avg_score_level, max_score



    def __get_loader_list(self, stock:Stock):
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
        f = Filter(stock)
        max_score_level, avg_score_level, max_score = self.get_total_strength(f)
        stock.score = max_score
        if max_score_level == Filter.SUPER:
            loader_list.append (self.__super_tel_loader)
        elif max_score_level == Filter.STRONG:
            loader_list.append(self.__strong_tel_loader)
        elif max_score_level == Filter.GOOD:
            loader_list.append(self.__all_tel_loader)
        loader_list.append(self.__csv_loader)
        self.__stock_name2last_sent_buy_sell_status[stock.name] = current_buy_sell_status
        self.__stock_name2last_sent_timestamp[stock.name] = time()
        return loader_list




    def update_loader (self, stock):
        loader_list = self.__get_loader_list(stock)
        self.__stock2loader_list [stock] = loader_list


    def load (self):
        loader2stock_list = defaultdict (list)
        for stock, loader_list in self.__stock2loader_list.items():
            for loader in loader_list:
                loader2stock_list [loader].append(stock)

        for loader, stock_list in loader2stock_list.items():
            stock_list.sort()
            for stock in stock_list:
                loader.load_stock(stock)

        self.__stock2loader_list = {}
