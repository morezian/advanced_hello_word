from datetime import datetime


class BuySellStatus:
    # human_buy_vol: int = 0
    # human_buy_count: int = 0
    # human_sell_vol: int = 0
    # human_sell_count: int = 0
    # civil_buy_vol: int = 0
    # civil_buy_count: int = 0
    # civil_sell_vol: int = 0
    # civil_sell_count: int = 0
    # trade_price: int = 0
    # vol : int = 0
    # final_price: int = 0
    # first_traded_price: int = 0
    #
    def __init__(self, trade_price=0, final_price=0, vol=0, human_buy_vol=0, human_buy_count=0, human_sell_vol=0, human_sell_count=0,
                 civil_buy_vol=0, civil_buy_count=0, civil_sell_vol=0, civil_sell_count=0, first_trade=0,
                 start_time_stamp=0, end_time_stamp=0, min_day_price=0, max_day_price=0, min_day_touched_price=0, max_day_touched_price=0):

        self.human_buy_vol = human_buy_vol
        self.human_buy_count = human_buy_count
        self.human_sell_vol = human_sell_vol
        self.human_sell_count = human_sell_count
        self.civil_buy_vol = civil_buy_vol
        self.civil_buy_count = civil_buy_count
        self.civil_sell_vol = civil_sell_vol
        self.civil_sell_count = civil_sell_count
        self.trade_price = trade_price
        self.vol = vol
        self.first_trade = first_trade
        self.final_price = final_price
        self.start_time_stamp = start_time_stamp
        self.end_time_stamp = end_time_stamp
        self.min_day_price = min_day_price
        self.max_day_price = max_day_price
        self.min_day_touched_price = min_day_touched_price
        self.max_day_touched_price = max_day_touched_price
        self.__MIL_RIAL = 10 ** 7

    def __get_moved_money_in_million_base(self):
        ans = self.vol * self.trade_price
        return ans // self.__MIL_RIAL

    def __get_average_money_per_code(self, vol, trade_price, count):
        if count <= 0:
            count = 1
        ans = (vol*trade_price)/(count)

        return ans

    def get_average_buy_per_code_in_million_base(self):
        ans = self.__get_average_money_per_code(
            self.human_buy_vol, self.trade_price, self.human_buy_count)
        return ans // self.__MIL_RIAL

    def get_human_buy_ratio_power(self):
        human_buy_power = self.__get_average_money_per_code(
            self.human_buy_vol, self.trade_price, self.human_buy_count)
        human_sell_power = self.__get_average_money_per_code(
            self.human_sell_vol, self.trade_price, self.human_sell_count)
        ans = human_buy_power/(human_sell_power + 0.0000001)
        MAX_POWER_RATIO = 1000
        ans = min(ans, MAX_POWER_RATIO)
        return ans

    def __get_price_in_percent(self, price):
        zero_price = (self.max_day_price + self.min_day_price) // 2
        # domain = (1 - (self.min_day_price / zero)) * 100 #4.98
        if zero_price == 0:
            return 0
        ans = price / zero_price - 1
        return ans * 100

    @property
    def trade_price_in_percent(self):
        return self.__get_price_in_percent(self.trade_price)

    @property
    def final_price_in_percent(self):
        return self.__get_price_in_percent(self.final_price)

    @property
    def max_day_price_in_percent(self):
        return self.__get_price_in_percent(self.max_day_price)

    @property
    def first_trade_in_percent(self):
        return self.__get_price_in_percent(self.first_trade)

    @property
    def max_day_touced_in_percent(self):
        return self.__get_price_in_percent(self.max_day_touched_price)

    @property
    def min_day_touced_in_percent(self):
        return self.__get_price_in_percent(self.min_day_touched_price)

    def __get_average_price(self, other):
        if self.vol + other.vol == 0:
            return 0
        return (self.trade_price*self.vol + other.trade_price*other.vol)//(self.vol + other.vol)

    def __sub__(self, other):
        if other.start_time_stamp == 0:
            return self
        if self.start_time_stamp == 0:
            return other
        human_buy_vol = self.human_buy_vol - other.human_buy_vol
        human_buy_count = self.human_buy_count - other.human_buy_count
        human_sell_vol = self.human_sell_vol - other.human_sell_vol
        human_sell_count = self.human_sell_count - other.human_sell_count
        civil_buy_vol = self.civil_buy_vol - other.civil_buy_vol
        civil_buy_count = self.civil_buy_count - other.civil_buy_count
        civil_sell_vol = self.civil_sell_vol - other. civil_sell_vol
        civil_sell_count = self.civil_sell_count - other.civil_sell_count
        vol = self.vol - other.vol
        trade_price = self.__get_average_price(other)
        final_price = max(self.final_price, other.final_price)
        first_trade = max(self.first_trade, other.first_trade)
        start_time_stamp = other.end_time_stamp
        end_time_stamp = self.end_time_stamp
        min_day_price = self.min_day_price
        max_day_price = self.max_day_price
        min_day_touched_price = self.min_day_touched_price
        max_day_touched_price = self.max_day_touched_price
        return BuySellStatus(trade_price, final_price, vol, human_buy_vol, human_buy_count, human_sell_vol, human_sell_count,
                             civil_buy_vol, civil_buy_count, civil_sell_vol, civil_sell_count, first_trade, start_time_stamp, end_time_stamp,
                             min_day_price, max_day_price, min_day_touched_price, max_day_touched_price)

    def __add__(self, other):
        if other.start_time_stamp == 0:
            return self
        if self.start_time_stamp == 0:
            return other
        human_buy_vol = self.human_buy_vol + other.human_buy_vol
        human_buy_count = self.human_buy_count + other.human_buy_count
        human_sell_vol = self.human_sell_vol + other.human_sell_vol
        human_sell_count = self.human_sell_count + other.human_sell_count
        civil_buy_vol = self.civil_buy_vol + other.civil_buy_vol
        civil_buy_count = self.civil_buy_count + other.civil_buy_count
        civil_sell_vol = self.civil_sell_vol + other. civil_sell_vol
        civil_sell_count = self.civil_sell_count + other.civil_sell_count
        vol = self.vol + other.vol
        trade_price = self.__get_average_price(other)
        final_price = max(self.final_price, other.final_price)
        first_trade = self.first_trade
        start_time_stamp = min(self.start_time_stamp, other.start_time_stamp)
        end_time_stamp = max(self.end_time_stamp, other.end_time_stamp)
        min_day_price = self.min_day_price
        max_day_price = self.max_day_price
        min_day_touched_price = self.min_day_touched_price
        max_day_touched_price = self.max_day_touched_price
        return BuySellStatus(trade_price, final_price, vol, human_buy_vol, human_buy_count, human_sell_vol, human_sell_count,
                             civil_buy_vol, civil_buy_count, civil_sell_vol, civil_sell_count, first_trade, start_time_stamp, end_time_stamp,
                             min_day_price, max_day_price, min_day_touched_price, max_day_touched_price)

    def is_significant(self):
        money_moved = self.__get_moved_money_in_million_base()
        if money_moved >= 50:  # larger tharn 50 million toman
            return True
        return False

    def is_real(self):
        if self.civil_sell_vol + self.civil_buy_vol > 0:
            return False
        return True

    def to_dict(self):
        ans = {
            "human_buy_vol": self.human_buy_vol, 
            "human_buy_count":self.human_buy_count,
            "human_sell_vol": self.human_sell_vol,
            "human_sell_count": self.human_sell_count,
            "civil_buy_vol": self.civil_buy_vol,
            "civil_buy_count": self.civil_buy_count,
            "civil_sell_vol": self.civil_sell_vol,
            "civil_sell_count": self.civil_sell_count,
            "trade_price": self.trade_price,
            "vol": self.vol,
            "first_trade": self.first_trade,
            "final_price": self.final_price,
            "start_time_stamp": self.start_time_stamp,
            "end_time_stamp": self.end_time_stamp,
            "min_day_price": self.min_day_price,
            "max_day_price": self.max_day_price,
            "min_day_touched_price": self.min_day_touched_price,
            "max_day_touched_price": self.max_day_touched_price
        }
        return ans

    # def to_list(self):
     #   pass
