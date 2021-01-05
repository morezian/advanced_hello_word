from app.src.interfaces.buysell_interface import *

class StockHistory:
    def __init__(self,name,latin_name, buy_sell_status_list:[BuySellStatus]):
        self.name = name
        self.latin_name = latin_name
        self.__buy_sell_status_list = buy_sell_status_list
        self.__initialize_params()

    def __initialize_params (self):
        self.__set_median_human_buy_power_ratio()


    def __set_median_human_buy_power_ratio(self):
        last_days = 30
        last_days = min(last_days, len(self.__buy_sell_status_list))
        ratio_list = []
        for i in range(last_days):
            ratio_list.append(self.__buy_sell_status_list[i].get_human_buy_ratio_power())
        ratio_list.sort()
        mid = len(ratio_list) // 2
        ans = ratio_list[mid]
        self.__median_human_buy_power_ratio = ans

    @property
    def median_human_buy_power_ratio (self):
        return self.__median_human_buy_power_ratio


