from app.src.interfaces.buysell_interface import BuySellStatus


class Stock:
    def __init__(self, name, retrieve_interval_cps_list ,stock_history = None):
        self.name = name
        self.current_buy_sell_status = BuySellStatus()
        self.__retrieve_interval_cps_list = retrieve_interval_cps_list
        self.__retrieve_interval_buy_sell_status_list = [BuySellStatus()]*len (retrieve_interval_cps_list)
        self.stock_history = stock_history





    def store_data(self):
        pass