from dataclasses import dataclass

@dataclass
class BuySellStatus:
    human_buy_vol: int = 0
    human_buy_count: int = 0
    human_sell_vol: int = 0
    human_sell_count: int = 0
    civil_buy_vol: int = 0
    civil_buy_count: int = 0
    civil_sell_vol: int = 0
    civil_sell_count: int = 0
    trade_price: int = 0
    vol : int = 0
    final_price: int = 0
    first_traded_price: int = 0

    def __get_power_per_code (self, vol, count):
        return vol/(count + 0.00000000001)


    def get_human_buy_ratio_power(self):
        human_buy_power = self.__get_power_per_code(self.human_buy_vol, self.human_buy_count)
        human_sell_power = self.__get_power_per_code(self.human_sell_vol, self.human_buy_count)
        return human_buy_power/human_sell_power


    def __get_average_price (self, other):
        if self.vol +other.vol == 0:
            return 0
        return (self.trade_price*self.vol + other.trade_price*other.vol)//(self.vol + other.vol)


    def __sub__(self, other):
        human_buy_vol = self.human_buy_vol - other.human_buy_vol
        human_buy_count = self.human_buy_count - other.human_buy_count
        human_sell_vol = self.human_sell_vol - other.human_sell_vol
        human_sell_count = self.human_sell_count -other.human_sell_count
        civil_buy_vol=self.civil_buy_vol - other.civil_buy_vol
        civil_buy_count=self.civil_buy_count -other.civil_buy_count
        civil_sell_vol=self.civil_sell_vol - other. civil_sell_vol
        civil_sell_count=self.civil_sell_count - other.civil_sell_count
        vol = self.vol - other.vol
        trade_price = self.__get_average_price(other)
        final_price = max (self.final_price, other.final_price)
        return BuySellStatus(trade_price, final_price, vol, human_buy_vol,human_buy_count, human_sell_vol, human_sell_count,
                 civil_buy_vol, civil_buy_count, civil_sell_vol, civil_sell_count)


    def __add__ (self, other):
        human_buy_vol = self.human_buy_vol + other.human_buy_vol
        human_buy_count = self.human_buy_count + other.human_buy_count
        human_sell_vol = self.human_sell_vol + other.human_sell_vol
        human_sell_count = self.human_sell_count + other.human_sell_count
        civil_buy_vol=self.civil_buy_vol + other.civil_buy_vol
        civil_buy_count=self.civil_buy_count + other.civil_buy_count
        civil_sell_vol=self.civil_sell_vol + other. civil_sell_vol
        civil_sell_count=self.civil_sell_count + other.civil_sell_count
        vol = self.vol - other.vol
        trade_price = self.__get_average_price(other)
        final_price = max (self.final_price, other.final_price)
        return BuySellStatus(trade_price, final_price, vol, human_buy_vol,human_buy_count, human_sell_vol, human_sell_count,
                 civil_buy_vol, civil_buy_count, civil_sell_vol, civil_sell_count)

