from .stock import *
from datetime import datetime
class Filter:
    BAD = 0
    WEAK = 1
    NORMAL = 2
    GOOD = 3
    STRONG = 4
    SUPER = 5
    def __init__(self, stock:Stock):
        self.__stock = stock


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
                return i
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
            cmp_list = [1, 5, 8, 15, 20]
        elif time_duration_minute <= 45:
            cmp_list = [5, 15, 20, 30, 50]
        elif time_duration_minute <= 120:
            cmp_list = [10, 30, 60, 125, 250]
        else:
            cmp_list = [20, 60, 120, 250, 500]
        ans = self.__filter_smaller(count, cmp_list)
        return ans



    def filter_event (self, is_real, is_interval):
        key = self.__get_key(is_real)
        interval_list = self.__stock.interval_list_dict [key]
        #TODO implement event detection on interval list.
        return 0