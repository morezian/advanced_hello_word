import requests
import urllib.parse
from requests_futures.sessions import FuturesSession
from app.src.stock.stock import *
from app.src.stock.filter import *
from collections import OrderedDict
from time import sleep
from datetime import datetime


class TelegramLoader:
    def __init__(self, token, id, is_special=False):
        self.__token = token
        self.__id = id
        self.__session = FuturesSession()
        self.is_special = is_special

    def __gp(self, buy_sell_status: BuySellStatus):
        power_ratio = buy_sell_status.get_human_buy_ratio_power()
        power_ratio = format(power_ratio, ".2f")
        buy_per_code = buy_sell_status.get_average_buy_per_code_in_million_base()
        buy_per_code = f"{int(buy_per_code)}M"
        buy_count = buy_sell_status.human_buy_count
        return f"[{power_ratio}, {buy_per_code}, {buy_count}]"

    def __get_string_stock(self, stock: Stock):
        buy_sell_status = stock.current_buy_sell_status_dict
        interval_buy_sell_status = stock.current_interval_buy_sell_status_dict
        em_red = "🟥"
        em_green = "🟩"
        em_blue = "🟦"
        em_up = "⤴️"
        em_down = "⤵️"
        trade_em = em_green
        trade_price_filter = stock.filter.trade_price()
        if trade_price_filter >= Filter.STRONG:
            trade_em = em_blue
        elif trade_price_filter >= Filter.GOOD:
            trade_em = em_red
        trade_price = buy_sell_status["all"].trade_price_in_percent
        final_price = buy_sell_status["all"].final_price_in_percent
        final_em = em_up
        if final_price > trade_price:
            final_em = em_down

        min_touched_price = buy_sell_status["all"].min_day_touced_in_percent
        max_touched_price = buy_sell_status["all"].max_day_touced_in_percent

        namad_emoji = "🏭"

        history_avg_buy_power_ratio = 0
        if stock.stock_history:
            history_avg_buy_power_ratio = stock.stock_history.market_human_buy_power_ratio

        rows = OrderedDict({
            namad_emoji + "name": f"#_{stock.name}",
            "board": self.__gp(buy_sell_status["all"]),
            "recent": self.__gp(interval_buy_sell_status["all"][-1]),
            "now": self.__gp(stock.last_second_buy_sell_status(is_real=False, last_second=30)),
            "history_buy_power": format(history_avg_buy_power_ratio, "0.2f"),
            # "real": self.__gp(buy_sell_status ["real"]),
            # "rrecent": self.__gp(interval_buy_sell_status ["real"][-1]),
            trade_em + "trade": format(trade_price, "0.2f"),
            final_em + "final": format(final_price, "0.2f"),
            "range": f"[{format(min_touched_price, '0.2f')}, {format(max_touched_price, '0.2f')}]",
            "opening": format(buy_sell_status["all"].first_trade_in_percent, "0.2f"),
            "time": (datetime.fromtimestamp(buy_sell_status["all"].end_time_stamp)).strftime("%H:%M:%S"),
            "link": f"https://mobile.emofid.com/stock-details/{stock.latin_name}",
            "SCORE": format(stock.score, "0.1f"),
        })

        final_str = ""
        for key, value in rows.items():
            final_str += f"{key}: {value}\n"
        return final_str

    def __get_string_stock_list(self, stock_list):
        ans = [urllib.parse.quote(self.__get_string_stock(stock))
               for stock in stock_list]
        return "\n".join(ans)

    def load_stock_list(self, stock_list):
        # urllib.parse.quote(self.__get_string_stock(stock))
        string_stock = self.__get_string_stock_list(stock_list)
        url = f'https://api.telegram.org/bot' + \
            str(self.__token) + '/sendMessage?text=' + \
            string_stock + '&chat_id=' + str(self.__id)
        # requests.get(url)
        #self.__session = FuturesSession()
        if self.is_special == False and 1 == 2:
            self.__session.get(url, hooks={'response': self.response_hook})
            # sleep(1)
        else:
            resp = requests.get(url)
            #print (resp)
        # requests.get(url)

    def response_hook(self, resp, *args, **kwargs):
        # parse the json storing the result on the response object
        resp.data = resp.json()
        print(str(resp.data))


if __name__ == "__main__":
    tl = TelegramLoader(
        token="1483369722:AAFQJOLnQeKZd5QjRD4wiI6pfAqoOu-m0Rk", id="-444966767")
    tl.load_stock(None)
