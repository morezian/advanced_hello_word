from app.src.loggers.file_logger import logger
from requests import sessions
from app.src.interfaces.buysell_interface import BuySellStatus
import datetime
from app.src.interfaces.stock_history_interface import StockHistory
session = sessions.session()
import concurrent.futures

xxx =0
class HistoryCrawler:
    def __init__(self,data):
        self.data = data

    def parse_history_data(self,raw_history: str,name,latin_name):
        raw_history = raw_history.split(';')[:50]

        raw_history = [i.split(',') for i in raw_history]
        [i.append(self.__get_timestamp(i[0])) for i in raw_history]
        buy_sell_status_list = []
        for i in raw_history:
            trade_price = 0
            if int(i[5]) != 0:
                trade_price = int(i[9]) // int(i[5])
            buy_sell_status_list.append(BuySellStatus(human_buy_count=int(i[1]),
                                                      civil_buy_count=int(i[2]),
                                                      human_sell_count=int(i[3]),
                                                      civil_sell_count=int(i[4]),
                                                      human_buy_vol=int(i[5]),
                                                      civil_buy_vol=int(i[6]),
                                                      human_sell_vol=int(i[7]),
                                                      civil_sell_vol=int(i[8]),
                                                      final_price= trade_price,
                                                      trade_price= trade_price,
                                                      end_time_stamp = int(i[13])
                                                      )
                                        )
        history = StockHistory(name=name, latin_name=latin_name, buy_sell_status_list=buy_sell_status_list)
        r = history.get_median_human_buy_power_ratio
        return history



    def __crawl_signle_history_data(self, url):
        global xxx
        history_data = session.get(url)
        print (f"feteched {xxx}")
        xxx += 1
        return history_data

    def __get_history_data_list(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            x = [f"http://www.tsetmc.com/tsev2/data/clienttype.aspx?i={symbol.unique_id}" for symbol in self.data]
            results = executor.map(self.__crawl_signle_history_data, x)
        return list(results)

    def get_stock_name2history(self):
        self.data = self.data[:300]
        histoed_buy_sell_status_dict = dict()
        history_data_list = self.__get_history_data_list()
        for i in range (len (self.data)):
            symbol = self.data[i]
            history_data = history_data_list[i]
            histoed_buy_sell_status_dict[symbol.name] = self.parse_history_data(history_data.text, symbol.name,
                                                                                symbol.latin_name)
        # for symbol in self.data:
        #     history_data = session.get(f"http://www.tsetmc.com/tsev2/data/clienttype.aspx?i={symbol.unique_id}"
        #                                 )
        #     histoed_buy_sell_status_dict[symbol.name] = self.parse_history_data(history_data.text,symbol.name,symbol.latin_name)
        #     print (f"added {len (histoed_buy_sell_status_dict)}")
        #     logger.info(f"fetched {symbol.name}")
        return histoed_buy_sell_status_dict

    def __get_timestamp(self,input_date):
        return int(datetime.datetime(year=int(input_date[0:4]),
                                     month=int(input_date[4:6]),
                                     day=int(input_date[6:]),
                                     hour=20, minute=30, second=0, tzinfo=datetime.timezone.utc).timestamp()
                   )
