from app.src.interfaces.buysell_interface import *

class StockHistory:
    def __init__(self,name,latin_name, buy_sell_status_list:[BuySellStatus]):
        self.name = name
        self.latin_name = latin_name
        self.__buy_sell_status_list = buy_sell_status_list
        self.__initialize_params()

    def __initialize_params (self):
        self.__set_market_human_buy_power_ratio()


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

    def __set_market_human_buy_power_ratio(self):
        last_days = 50
        last_days = min(last_days, len(self.__buy_sell_status_list))
        ratio_list = []
        for i in range(last_days-1):
            x = self.__buy_sell_status_list[i].trade_price
            y = self.__buy_sell_status_list[i+1].trade_price
            if x == 0 or y == 0:
                continue
            diff =  (x-y) / y
            if diff <= 0 and diff >= -0.01:
                ratio_list.append(self.__buy_sell_status_list[i].get_human_buy_ratio_power())
        if len(ratio_list) == 0:
            ans = 1
        else:
            ratio_list.sort()
            mid = int(len(ratio_list) * 0.8)
            ans = ratio_list[mid]
        self.__median_human_buy_power_ratio = ans

    @property
    def market_human_buy_power_ratio (self):
        return self.__median_human_buy_power_ratio



