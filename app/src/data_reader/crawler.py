import requests
from app.src.loggers.file_logger import logger
from app.src.stock.stock import BuySellStatus
from requests_futures.sessions import FuturesSession
import time
from app.src.data_reader.trash_symbols import trash_symbols
from datetime import datetime
from app.src.utils.time_helpers import get_today_market_opening_time
from app.src.interfaces.symbol import Symbol
from app.src.data_reader.csv_reader import CsvReader
from app.src.data_reader.history_crawler import HistoryCrawler
from app.src.data_loader.history_loader.database_loader import HistoryMysqlLoader
session = FuturesSession()
names = {'UNK':  3,
         'first_price': 4 ,
         'closed_price': 5 ,
         'latest_traded_price': 6 ,
         'count':7  ,
         'vol':8  ,
         'traded_value':9  ,
         'min_traded_price': 10 ,
         'max_traded_price':  11,
         'yesterday_price': 12 ,
         'UNK2': 13 ,
         'base_vol':14  ,
         'UNK3': 15 ,
         'UNK4': 16 ,
         'UNK5': 17 ,
         'max_valid_price': 18 ,
         'min_valid_price': 19 ,
         'lot': 20 ,
         'UNK6':  21,
         'human_buy_count': 22 ,
         'civil_buy_count':  23,
         'human_buy_vol': 24 ,
         'civil_buy_vol': 25 ,
         'human_sell_count': 26 ,
         'civil_sell_count': 27 ,
         'human_sell_vol': 28 ,
         'civil_sell_vol':29}
history_data = dict()

class DataCrawler:
    def __init__(self,crawl_history = False,realtime=True,csv_file=None,stock_name=None):
        global history_data
        self.history = history_data
        if crawl_history == True:
            data = self.__get_realtime_date()
            history_data = HistoryCrawler(data).get_stock_name2history()
            loader = HistoryMysqlLoader(host="79.175.176.165",port=3306,username='admin',password='vwB75K',database='trade_db')
            loader.insert_stock_history_list_to_db(history_data)
        self.realtime = realtime
        if not self.realtime :
            self.csv_generator = CsvReader(file=csv_file,history=self.history,stock_name=stock_name)

    def crawl_data (self)->list:
        if self.realtime:
            return self.__get_realtime_date()
        else:
            return self.csv_generator.read_next_batch()

    def __get_realtime_date(self):
        table, symbols_human_civil_trading_status = self.__load_tables()
        union_table = self.__get_union_of_two_tables(table, symbols_human_civil_trading_status)
        symbols_list = []
        for unique_id, content in union_table.items():
            current_buy_sell = self.__get_buy_sell_status(content)
            symbols_list.append(Symbol(unique_id=unique_id,
                                       latin_name=content[0],
                                       name=content[1],
                                       current_buy_sell_status=current_buy_sell,
                                       history=self.history.get(content[0])
                                       )
                                )
        return symbols_list

    def __load_tables(self):
        while True:
            try:
                watcher_table = session.get('http://www.tsetmc.com/tsev2/data/MarketWatchPlus.aspx?h=0&r=0',timeout=10)
                symbols_human_civil_trading_status = session.get('http://www.tsetmc.com/tsev2/data/ClientTypeAll.aspx',timeout = 10)
                watcher_table = watcher_table.result()
                symbols_human_civil_trading_status = symbols_human_civil_trading_status.result()
                try:
                    watcher_table = watcher_table.text.split('@@')[1].split(';')
                except:
                    try:
                        watcher_table = watcher_table.text.split('0.2%,')[1].split(';')
                    except:
                        watcher_table = watcher_table.text.split('@')[2].split(';')
                symbols_human_civil_trading_status = symbols_human_civil_trading_status.text.split(';')
                break
            except Exception as e:
                logger.error(e)
        watcher_table = [x.split(',') for x in watcher_table]
        watcher_table = [i for i in watcher_table if i[0] not in trash_symbols]
        symbols_human_civil_trading_status = [str(x).split(',') for x in symbols_human_civil_trading_status]
        return watcher_table,symbols_human_civil_trading_status

    def __get_union_of_two_tables(self,watcher_table: list,symbols_human_civil_trading_status: list)->dict:
        watcher_table_dict = {}
        for x in watcher_table:
            if x[1][0] == 'I':
                watcher_table_dict[x[0]] = x[1:]
        symbols_human_civil_trading_status_dict = {}
        [symbols_human_civil_trading_status_dict.update({str(x[0]): x[1:]}) for x in symbols_human_civil_trading_status if str(x[0]) in watcher_table_dict.keys()]
        for symbol in symbols_human_civil_trading_status_dict:
            symbols_human_civil_trading_status_dict[symbol] = watcher_table_dict[symbol] + symbols_human_civil_trading_status_dict[symbol]
        return symbols_human_civil_trading_status_dict


    def __get_buy_sell_status(self,list_of_string_numbers) -> BuySellStatus:
        new_bss = BuySellStatus(human_buy_vol= int(list_of_string_numbers[names.get('human_buy_vol')]),
                                human_buy_count= int(list_of_string_numbers[names.get('human_buy_count')]),
                                human_sell_vol= int(list_of_string_numbers[names.get('human_sell_vol')]),
                                human_sell_count= int(list_of_string_numbers[names.get('human_sell_count')]),
                                civil_buy_vol= int(list_of_string_numbers[names.get('civil_buy_vol')]),
                                civil_buy_count= int(list_of_string_numbers[names.get('civil_buy_count')]),
                                civil_sell_vol= int(list_of_string_numbers[names.get('civil_sell_vol')]),
                                civil_sell_count= int(list_of_string_numbers[names.get('civil_sell_count')]),
                                trade_price= int(list_of_string_numbers[names.get('latest_traded_price')]),
                                vol= int(list_of_string_numbers[names.get('vol')]),
                                final_price= int(list_of_string_numbers[names.get('closed_price')]),
                                first_trade= int(list_of_string_numbers[names.get('first_price')]),
                                min_day_price=float(list_of_string_numbers[names.get('min_valid_price')]),
                                max_day_price=float(list_of_string_numbers[names.get('max_valid_price')]),
                                start_time_stamp= get_today_market_opening_time(),
                                max_day_touched_price= int(list_of_string_numbers[names.get('max_traded_price')]),
                                min_day_touched_price= int(list_of_string_numbers[names.get('min_traded_price')]),
                                end_time_stamp= int(time.time())
                                )
        return new_bss