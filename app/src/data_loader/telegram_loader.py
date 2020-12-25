import requests
import urllib.parse

from app.src.stock.stock import *
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
        interval_buy_sell_status = stock.interval_list_dict
        em_red = "🟥"
        em_green = "🟩"
        em_blue = "🟦"
        em_up = "⤴️"
        em_down = "⤵️"
        trade_em = em_green
        trade_price = buy_sell_status["all"].trade_price
        if trade_price <= -0.3:

        rows = {
         "نام": f"#{stock.name}",
        "ح": self.__gp(buy_sell_status ["all"]),
        "لح": self.__gp(interval_buy_sell_status ["all"]),
        "وح": self.__gp(buy_sell_status ["real"]),
        "لوح": self.__gp(interval_buy_sell_status ["real"]),
        "معامله": buy_sell_status["all"].trade_price,
        "پایانی": buy_sell_status["all"].final_price,
        "اولین": buy_sell_status["all"].first_trade
        }


    def load_stock (self, stock:Stock):
        string_stock = urllib.parse.quote(self.__get_string_stock(stock))
        url = f'https://api.telegram.org/bot' + str(self.__token) + '/sendMessage?text=' + string_stock + '&chat_id=' + str(self.__id)
        resp = requests.get(url)







if __name__ == "__main__":
    tl = TelegramLoader (token="1483369722:AAFQJOLnQeKZd5QjRD4wiI6pfAqoOu-m0Rk", id =  "-444966767")
    tl.load_stock(None)