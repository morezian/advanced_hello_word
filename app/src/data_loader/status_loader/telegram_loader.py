import requests
import urllib.parse
from requests_futures.sessions import FuturesSession
from app.src.stock.stock import *
from app.src.stock.filter import *
from collections import OrderedDict
from time import sleep
from datetime import datetime
from io import BytesIO, BufferedReader
import matplotlib.pyplot as plt
import matplotlib
import telepot
from datetime import timedelta

class TelegramLoader:
    def __init__(self, token, id, is_special = False):
        self.__token = token
        self.__id = id
        self.__session = FuturesSession()
        self.is_special = is_special
        self.__bot = telepot.Bot(token)


    def __gp (self, buy_sell_status:BuySellStatus):
        power_ratio = buy_sell_status.get_human_buy_ratio_power()
        power_ratio = format(power_ratio, ".2f")
        buy_per_code = buy_sell_status.get_average_buy_per_code_in_million_base()
        buy_per_code = f"{int(buy_per_code)}M"
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
        "board": self.__gp(buy_sell_status ["all"]),
        "recent": self.__gp(interval_buy_sell_status ["all"][-1]),
        "now": self.__gp(stock.last_second_buy_sell_status(is_real=False,last_second=30)),
        "history_buy_power": format(history_avg_buy_power_ratio, "0.2f"),
        trade_em + "trade": format(trade_price, "0.2f"),
        final_em + "final": format(final_price, "0.2f"),
        "vol": f'{format(buy_sell_status["all"].vol/1000000, "0.2f")}M',
        "range": f"[{format(min_touched_price, '0.2f')}, {format(max_touched_price, '0.2f')}]",
        #"opening": format(buy_sell_status["all"].first_trade_in_percent, "0.2f"),
        "time": (datetime.fromtimestamp(buy_sell_status ["all"].end_time_stamp)).strftime("%H:%M:%S"),
        "link": f"https://mobile.emofid.com/stock-details/{stock.latin_name}",
        "SCORE": format(stock.score, "0.1f"),
        })

        final_str = ""
        for key, value in rows.items():
            final_str +=  f"{key}: {value}\n"
        return final_str


    def __scale (self, value, old_max, old_min, new_max, new_min):
        value = max (value, old_min)
        value = min (value, old_max)
        old_range = (old_max - old_min)
        new_range = (new_max - new_min)
        new_value = (((value - old_min) * new_range) / old_range) + new_min
        return new_value

    def __normal_buy_power_ratio(self, buy_sell_stauts):
        value = buy_sell_stauts.get_human_buy_ratio_power()
        if value < 1:
            ans = self.__scale(value, 1, 0, 0, -5)
        else:
            ans = self.__scale(value, 3, 1, 5, 0)

        return ans

    def __normal_score(self, score):
        ans = self.__scale(score, 5, -5, 5, -5)
        return ans

    def __normal_price(self, buy_sell_status:BuySellStatus):
        domain = buy_sell_status.max_day_price_in_percent
        ans = self.__scale(buy_sell_status.trade_price_in_percent,domain, -domain, 5, -5)
        return ans

    def __simple_plot(self, x_list, y_list_list, y_label_list, title):
        plt.style.use("fivethirtyeight")
        plt.figure()
        for i, y_list in enumerate(y_list_list):
            plt.plot(x_list, y_list, label=y_label_list[i])
        plt.title(title)
        plt.legend()
        plt.ylim(-5, 5)
        #plt.show()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf#buf.read()

    def __send_img(self, caption, photo):
        self.__bot.sendPhoto(chat_id=self.__id, photo=photo, caption=caption)

    def load_stock (self, stock, buy_sell_status_list, date):
        if len(buy_sell_status_list) == 0:
            text = "There is no Transaction for requested stock"
            url = f'https://api.telegram.org/bot' + str(
                self.__token) + '/sendMessage?text=' + text + '&chat_id=' + str(self.__id)
            requests.get(url)

        week_day = date.strftime('%A')
        date_string = f"{week_day}, {date.strftime('%d-%m-%Y')}"
        score_list = []
        buy_power_list = []
        price_list = []
        time_list = []
        max_day_score = -100000
        for buy_sell in buy_sell_status_list:
            stock.update(buy_sell)
            f = Filter(stock)
            score, score_level = f.get_total_strength()
            max_day_score = max (max_day_score,score)
            score_list.append(self.__normal_score(stock.score))
            buy_power_list.append(self.__normal_buy_power_ratio(buy_sell))
            price_list.append(self.__normal_price(buy_sell))
            time_list.append((datetime.fromtimestamp(buy_sell.end_time_stamp)))
        buf = self.__simple_plot(time_list, [score_list, buy_power_list, price_list], ["score", "buy_power", "price"], date_string)
        text = self.__get_string_stock(stock)
        self.__send_img(text, ('z.png', buf))
