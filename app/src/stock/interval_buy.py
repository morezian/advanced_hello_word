from app.src.interfaces.buysell_interface import *
from collections import deque
from time import time

class IntervalBuy:

    def __init__(self, retrieve_previous_seconds_list, max_list_length):
        self.__interval_buy_sell_status_queue_max_length = max_list_length
        self.__retrieve_previous_seconds_list = retrieve_previous_seconds_list

        self.__max_previous_second = max (self.__retrieve_previous_seconds_list)
        self.current_buy_sell_status_dict = {"real": BuySellStatus(), "all": BuySellStatus()}
        self.interval_buy_sell_status_queue_dict = {"real": deque(), "all": deque()}




    def __add_current_buy_sell_status (self, current_buy_sell_status, is_real):
        if is_real == True:
            key = "real"
        else:
            key = "all"

        if len (self.interval_buy_sell_status_queue_dict [key]) > 0:
            if len (self.interval_buy_sell_status_queue_dict [key]) >= self.__interval_buy_sell_status_queue_max_length or \
                self.interval_buy_sell_status_queue_dict [key] [0].end_time + self.__max_previous_second < current_buy_sell_status.end_time:
                self.interval_buy_sell_status_queue_dict[key].popleft()

        currnet_inteval_buy_sell_status = current_buy_sell_status - self.current_buy_sell_status_dict [key]
        is_significant = current_buy_sell_status.is_significant()
        if is_significant:
            if (not is_real) or current_buy_sell_status.is_real():
                self.interval_buy_sell_status_queue_dict [key].append(currnet_inteval_buy_sell_status)
                self.current_buy_sell_status_dict [key] = current_buy_sell_status
        return is_significant


    def set_current_buy_sell_status (self, current_buy_sell_status):
        self.__add_current_buy_sell_status(current_buy_sell_status, True)
        is_signigicant = self.__add_current_buy_sell_status(current_buy_sell_status, False)
        return is_signigicant



    def __retrieve_interval_buy_sell_status_list (self, is_real):
        if is_real == True:
            key = "real"
        else:
            key = "all"

        cusum =  BuySellStatus()
        ans = []
        j = 0
        n = len(self.interval_buy_sell_status_queue_dict [key])
        for i in range(n):
            current = self.interval_buy_sell_status_queue_dict[key][n - i - 1]
            cusum += current
            if current.start_time_stamp + self.__retrieve_previous_seconds_list [j] < time():
                ans.append(cusum)
                j+=1
                if j == len (self.__retrieve_previous_seconds_list):
                    break
        while (j<len (self.__retrieve_previous_seconds_list)):
            ans.append(cusum)
            j += 1
        return ans

    def retrieve_interval_buy_sell_status (self):
        ans = {
            "real": self.__retrieve_interval_buy_sell_status_list(True),
            "all": self.__retrieve_interval_buy_sell_status_list(False)
        }
        return ans