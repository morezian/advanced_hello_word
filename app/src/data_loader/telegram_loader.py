import requests
import urllib.parse

from app.src.stock.stock import *
from app.src.stock.filter import *
from collections import OrderedDict


class TelegramLoader:
    def __init__(self, token, id):
        self.__token = token
        self.__id = id


    def __gp (self, buy_sell_status:BuySellStatus):
        power_ratio = buy_sell_status.get_human_buy_ratio_power()
        power_ratio = format(power_ratio, ".2f")
        buy_per_code = buy_sell_status.get_average_buy_per_code_in_million_base()
        buy_per_code = f"{buy_per_code}M"
        buy_count = buy_sell_status.human_buy_count
        return f"[{power_ratio}, {buy_per_code}, {buy_count}]"

    def __get_string_stock (self, stock:Stock):
        buy_sell_status = stock.current_buy_sell_status_dict
        interval_buy_sell_status = stock.current_interval_buy_sell_status_dict
        em_red = "🟥"
        em_green = "🟩"
        em_blue = "🟦"
        em_up = "⤴️"
        em_down = "⤵️"
        trade_em = em_green
        f = Filter(stock)
        trade_price_filter = f.trade_price()
        if trade_price_filter == Filter.SUPER:
            trade_em = em_blue
        elif trade_price_filter == Filter.STRONG:
            trade_em = em_red
        trade_price = buy_sell_status["all"].trade_price_in_percent
        final_price = buy_sell_status["all"].final_price_in_percent
        final_em = em_up
        if final_price > trade_price:
            final_em = em_down

        rows = OrderedDict({
         "نام": f"#{stock.name}",
        "ح": self.__gp(buy_sell_status ["all"]),
        "لح": self.__gp(interval_buy_sell_status ["all"][-1]),
        "وح": self.__gp(buy_sell_status ["real"]),
        "لوح": self.__gp(interval_buy_sell_status ["real"][-1]),
        trade_em + "معامله": format(trade_price, "0.2f"),
        final_em + "پایانی": format(final_price, "0.2f"),
        "اولین": buy_sell_status["all"].first_trade
        })

        final_str = ""
        for key, value in rows.items():
            final_str +=  f"{key}: {value}\n"
        return final_str


    def load_stock (self, stock:Stock):
        string_stock = urllib.parse.quote(self.__get_string_stock(stock))
        url = f'https://api.telegram.org/bot' + str(self.__token) + '/sendMessage?text=' + string_stock + '&chat_id=' + str(self.__id)
        requests.get(url)







if __name__ == "__main__":
    tl = TelegramLoader (token="1483369722:AAFQJOLnQeKZd5QjRD4wiI6pfAqoOu-m0Rk", id =  "-444966767")
    tl.load_stock(None)