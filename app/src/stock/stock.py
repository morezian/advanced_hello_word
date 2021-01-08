from app.src.interfaces.buysell_interface import BuySellStatus
from .interval_buy import *

class Stock:
    def __init__(self, name, latin_name ,retrieve_prevois_second_list, max_interval_list_length,stock_history = None):
        self.name = name
        self.stock_history = stock_history
        self.__retrieve_previous_second_list = retrieve_prevois_second_list
        self.__max_interval_list_length = max_interval_list_length
        self.__interval_buy = IntervalBuy(retrieve_prevois_second_list,max_interval_list_length)
        self.__is_significant = False
        self.latin_name = latin_name
        self.score = 0


    @property
    def current_buy_sell_status_dict (self):
        return self.__interval_buy.current_buy_sell_status_dict
    @property
    def current_interval_buy_sell_status_dict(self):
        return self.__interval_buy.retrieve_interval_buy_sell_status()

    @property
    def interval_list_dict (self):
        return self.__interval_buy.interval_buy_sell_status_queue_dict

    @property
    def is_significant (self):
        return self.__is_significant

    def last_second_buy_sell_status (self, is_real, last_second):
        return self.__interval_buy.retrieve_last_second_buy_sell_status(is_real, last_second)

    def update(self, current_buy_sell_status):
        is_significant = self.__interval_buy.set_current_buy_sell_status(current_buy_sell_status)
        self.__is_significant = is_significant


    def clear(self):
        self.__interval_buy = IntervalBuy(self.__retrieve_previous_second_list,self.__max_interval_list_length)
        self.score = 0


    def __lt__(self, other):
        return self.score < other.score

