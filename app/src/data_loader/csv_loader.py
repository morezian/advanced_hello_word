import csv
from app.src.stock.stock import *
import os

class CsvLoader:
    def __init__(self):
        file_path = str(int(time()))
        dir_path = "app/data/csv"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        in_file = open(f'{dir_path}/{file_path}.csv', 'wt')
        self._writer = csv.writer(in_file)
        col_name_list = ["name", "time_stamp", "trade_price", "final_price", "human_buy_count", "human_buy_vol","human_sell_count", "human_sell_vol" ,
                         "civil_buy_count", "civil_buy_vol", "civil_sell_count", "civil_sell_vol", "first_trade", "min_day_price", "max_day_price"
                         ,"min_day_touched_price", "max_day_touched_price", "vol"]
        self._writer.writerow(col_name_list)


    def __get_values(self, stock:Stock):
        buy_sell_status = stock.current_buy_sell_status_dict["all"]
        name = stock.name
        time_stamp = buy_sell_status.end_time_stamp
        trade_price = buy_sell_status.trade_price
        final_price = buy_sell_status.final_price
        human_buy_count = buy_sell_status.human_buy_count
        human_buy_vol = buy_sell_status.human_buy_vol
        human_sell_count = buy_sell_status.human_sell_count
        human_sell_vol = buy_sell_status.human_sell_vol
        civil_buy_count = buy_sell_status.civil_buy_count
        civil_buy_vol = buy_sell_status.civil_buy_vol
        civil_sell_count = buy_sell_status.civil_sell_count
        civi_sell_vol = buy_sell_status.civil_sell_vol
        first_trade = buy_sell_status.first_trade
        min_day_price = buy_sell_status.min_day_price
        max_day_price = buy_sell_status.max_day_price
        min_day_touched_price = buy_sell_status.min_day_touced_in_percent
        max_day_touched_price = buy_sell_status.max_day_touched_price
        vol = buy_sell_status.vol
        return [name, time_stamp, trade_price, final_price, human_buy_count, human_buy_vol, human_sell_count, human_sell_vol,
                civil_buy_count, civil_buy_vol, civil_sell_count, civi_sell_vol, first_trade, min_day_price, max_day_price,
                min_day_touched_price, max_day_touched_price, vol]

    def load_stock_list (self, stock_list):
        for stock in stock_list:
            values = self.__get_values(stock)
            self._writer.writerow (values)
