from app.src.interfaces.buysell_interface import BuySellStatus
from .interval_buy import *

class Stock:
    def __init__(self, name, retrieve_prevois_second_list, max_interval_list_length,stock_history = None):
        self.name = name
        self.stock_history = stock_history
        self.__interval_buy = IntervalBuy(retrieve_prevois_second_list,max_interval_list_length)

    @property
    def current_buy_sell_status_dict (self):
        return self.__interval_buy.current_buy_sell_status_dict
    @property
    def current_interval_buy_sell_status_dict(self):
        return self.__interval_buy.retrieve_interval_buy_sell_status()

    @property
    def interval_list_dict (self):
        return self.__interval_buy.interval_buy_sell_status_queue_dict


    def update(self, current_buy_sell_status):
        self.__interval_buy.set_current_buy_sell_status(current_buy_sell_status)


    def filter(self):

    def load (self):
