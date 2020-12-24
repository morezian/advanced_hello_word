from collections import deque
from app.src.interfaces.buysell_interface import BuySellStatus


class Stock:
    def __init__(self, name, retrieve_interval_cps_list ,stock_history = None):
        self.name = name
        self.__interval_buy_sell_status_queue_max_length = max (retrieve_interval_cps_list)
        self.__interval_buy_sell_status_queue = deque()
        self.current_buy_sell_status = BuySellStatus()
        self.__retrieve_interval_cps_list = retrieve_interval_cps_list
        self.__retrieve_interval_buy_sell_status_list = [BuySellStatus()]*len (retrieve_interval_cps_list)
        self.stock_history = stock_history


    def set_current_buy_sell_status (self, current_buy_sell_status):
        if len (self.__interval_buy_sell_status_queue) >= self.__interval_buy_sell_status_queue_max_length:
            self.__interval_buy_sell_status_queue.popleft()

        currnet_inteval_buy_sell_status = current_buy_sell_status - self.current_buy_sell_status
        self.__interval_buy_sell_status_queue.append(currnet_inteval_buy_sell_status)
        self.current_buy_sell_status = current_buy_sell_status
        # self.__retrieve_interval_buy_sell_status_list = self.__retrieve_interval_buy_sell_status_list()


    def __retrieve_interval_buy_sell_status_list (self):
        cusum =  BuySellStatus()
        ans = []
        j = 0
        for i in range(len(self.__interval_buy_sell_status_queue)):
            cusum += self.__interval_buy_sell_status_queue [len (self.__interval_buy_sell_status_queue) - i - 1]
            if i+1 == self.__retrieve_interval_cps_list [j]:
                ans.append(cusum)
                j+=1
                if j == len (self.__retrieve_interval_cps_list):
                    break
        while (j<len (self.__retrieve_interval_cps_list)):
            ans.append(cusum)
            j += 1
        return ans


    def store_data(self):
        pass