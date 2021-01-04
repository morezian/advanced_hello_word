from app.src.interfaces.buysell_interface import *

class StockHistory:
    def __init__(self,name,latin_name, buy_sell_status_list:[BuySellStatus]):
        self.name = name
        self.latin_name = latin_name
        self.__buy_sell_status_list = buy_sell_status_list



    @property
    def get_median_human_buy_power_ratio(self):
        last_days = 30
        last_days = min (last_days, len (self.__buy_sell_status_list))
        ratio_list = []
        for i in range(last_days):
            ratio_list.append(self.__buy_sell_status_list[i].get_human_buy_ratio_power)
        mid = len (ratio_list)//2
        return ratio_list[mid]


