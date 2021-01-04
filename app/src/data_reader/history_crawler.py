from app.src.loggers.file_logger import logger
from requests import sessions
from app.src.interfaces.buysell_interface import BuySellStatus
import datetime
from app.src.interfaces.stock_history_interface import StockHistory
session = sessions.session()

class HistoryCrawler:
    def __init__(self,data):
        self.data = data

    def parse_history_data(self,raw_history: str,name,latin_name):
        raw_history = raw_history.split(';')
        buy_sell_status_list = StockHistory(name=name,latin_name=latin_name)
        raw_history = [i.split(',') for i in raw_history]
        [i.append(self.__get_timestamp(i[0])) for i in raw_history]
        for i in raw_history:
            buy_sell_status_list.append(BuySellStatus(human_buy_count=i[1],
                                                      civil_buy_count=i[2],
                                                      human_sell_count=i[3],
                                                      civil_sell_count=i[4],
                                                      human_buy_vol=i[5],
                                                      civil_buy_vol=i[6],
                                                      human_sell_vol=i[7],
                                                      civil_sell_vol=i[8],
                                                      final_price= round(int(i[9]) / int(i[5])),
                                                      trade_price= round(int(i[9]) / int(i[5])),
                                                      end_time_stamp = i[13]
                                                      )
                                        )
        return buy_sell_status_list

    def get_stock_name2history(self):
        histoed_buy_sell_status_dict = dict()
        for symbol in self.data:
            history_data = session.get(f"http://www.tsetmc.com/tsev2/data/clienttype.aspx?i={symbol.unique_id}",
                                        )
            histoed_buy_sell_status_dict[symbol.name] = self.parse_history_data(history_data.text,symbol.name,symbol.latin_name)
            logger.info(f"fetched {symbol.name}")
        return histoed_buy_sell_status_dict

    def __get_timestamp(self,input_date):
        return int(datetime.datetime(year=int(input_date[0:4]),
                                     month=int(input_date[4:6]),
                                     day=int(input_date[6:]),
                                     hour=20, minute=30, second=0, tzinfo=datetime.timezone.utc).timestamp()
                   )
