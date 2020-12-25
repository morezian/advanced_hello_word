from .stock import *
from datetime import datetime
class Filter:
    BAD = -20
    WEAK = -3
    NORMAL = 0
    GOOD = 2
    STRONG = 4
    SUPER = 7
    def __init__(self, stock:Stock):
        self.__stock = stock
        self.__filter_name = [Filter.BAD, Filter.WEAK, Filter.NORMAL, Filter.GOOD, Filter.STRONG, Filter.SUPER]

    def __get_key (self, is_real):
        if is_real == True:
            return "real"
        return "all"

    def __get_buy_sell_status (self, is_real, is_interval):
        key = self.__get_key(is_real)
        if is_interval == True:
            buy_sell_status = self.__stock.current_interval_buy_sell_status_dict[key][-1]  # 5mins
        else:
            buy_sell_status = self.__stock.current_buy_sell_status_dict[key]
        return buy_sell_status



    def __filter_smaller (self, input, cmp_list):
        for i in range (len (cmp_list)):
            if input < cmp_list [i]:
                return self.__filter_name[i]
        return len (cmp_list)


    def buy_power_ratio (self, is_real, is_interval):
        buy_sell_status =  self.__get_buy_sell_status(is_real, is_interval)
        ratio = buy_sell_status.get_human_buy_ratio_power()
        cmp_list = [0.6, 0.9, 1.2, 1.5, 1.8]
        ans = self.__filter_smaller(ratio, cmp_list)
        return ans


    def avg_buy_per_code (self, is_real, is_interval):
        buy_sell_status =  self.__get_buy_sell_status(is_real, is_interval)
        per_code = buy_sell_status.get_average_buy_per_code_in_million_base()
        cmp_list = [10, 15, 20, 25, 30]
        ans = self.__filter_smaller(per_code, cmp_list)
        return ans


    def human_buy_count (self, is_real, is_interval):
        buy_sell_status =  self.__get_buy_sell_status(is_real, is_interval)
        count = buy_sell_status.human_buy_count
        time_duration_second = buy_sell_status.end_time_stamp - buy_sell_status.start_time_stamp
        time_duration_minute = time_duration_second // 60
        if time_duration_minute <= 10:
            cmp_list = [1, 5, 10, 16, 25]
        elif time_duration_minute <= 45:
            cmp_list = [5, 15, 30, 70, 150]
        elif time_duration_minute <= 120:
            cmp_list = [20, 60, 120, 280, 600]
        else:
            cmp_list = [40, 90, 200, 450, 1000]
        ans = self.__filter_smaller(count, cmp_list)
        return ans


    def trade_price (self):
        buy_sell_status =  self.__get_buy_sell_status(False, False)
        price_in_percent = buy_sell_status.trade_price_in_percent
        price_in_rial = buy_sell_status.trade_price
        if price_in_rial == buy_sell_status.max_day_price:
            return -100000
        domain = buy_sell_status.max_day_price_in_percent
        if price_in_percent + domain <=1:
            return Filter.SUPER
        elif price_in_percent + domain <=3:
            return Filter.STRONG
        elif price_in_percent + domain <=5:
            return Filter.GOOD
        elif price_in_percent + domain <=7:
            return Filter.NORMAL
        else:
            return Filter.WEAK

    def filter_event (self, is_real, is_interval):
        key = self.__get_key(is_real)
        interval_list = self.__stock.interval_list_dict [key]
        #TODO implement event detection on interval list.
        return 0