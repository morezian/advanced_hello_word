import requests
from app.src.loggers.file_logger import logger
from app.src.stock.stock import BuySellStatus
import time
from app.src.data_reader.trash_symbols import trash_symbols
from datetime import datetime

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
class Symbol:
    def __init__(self,name,latin_name,unique_id,current_buy_sell_status):
        self.name: str = name
        self.latin_name: str = latin_name
        self.unique_id: str = unique_id
        self.current_buy_sell_status:BuySellStatus = current_buy_sell_status

def get_today_market_opening_time():
    return int(datetime(year=datetime.now().year,
                                    month=datetime.now().month,
                                    day=datetime.now().day,
                                    hour=9, minute=0, second=0).timestamp())

def crawl_data ()->list:
        table , symbols_human_civil_trading_status = __load_tables()
        union_table = __get_union_of_two_tables(table,symbols_human_civil_trading_status)
        symbols_list = []
        for unique_id,content in union_table.items():

            current_buy_sell = __get_buy_sell_status(content)
            symbols_list.append(Symbol(unique_id=unique_id,
                                       latin_name=content[0],
                                       name=content[1],
                                       current_buy_sell_status=current_buy_sell
                                       )
                                )
        return symbols_list

def __load_tables():
    while True:
        try:
            watcher_table = requests.get('http://www.tsetmc.com/tsev2/data/MarketWatchPlus.aspx?h=0&r=0')
            symbols_human_civil_trading_status = requests.get('http://www.tsetmc.com/tsev2/data/ClientTypeAll.aspx')
            try:
                watcher_table = watcher_table.text.split('@@')[1].split(';')
            except:
                watcher_table = watcher_table.text.split('0.2%,')[1].split(';')
            symbols_human_civil_trading_status = symbols_human_civil_trading_status.text.split(';')
            break
        except Exception as e:
            logger.error(e)
    watcher_table = [x.split(',') for x in watcher_table]
    watcher_table = [i for i in watcher_table if i[0] not in trash_symbols]
    symbols_human_civil_trading_status = [str(x).split(',') for x in symbols_human_civil_trading_status]
    return watcher_table,symbols_human_civil_trading_status

def __get_union_of_two_tables(watcher_table: list,symbols_human_civil_trading_status: list)->dict:
    watcher_table_dict = {}
    for x in watcher_table:
        if x[1][0] == 'I':
            watcher_table_dict[x[0]] = x[1:]
    symbols_human_civil_trading_status_dict = {}
    [symbols_human_civil_trading_status_dict.update({str(x[0]): x[1:]}) for x in symbols_human_civil_trading_status if str(x[0]) in watcher_table_dict.keys()]
    for symbol in symbols_human_civil_trading_status_dict:
        symbols_human_civil_trading_status_dict[symbol] = watcher_table_dict[symbol] + symbols_human_civil_trading_status_dict[symbol]
    return symbols_human_civil_trading_status_dict


def __get_buy_sell_status(list_of_string_numbers) -> BuySellStatus:
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
                            min_day_price=int(list_of_string_numbers[names.get('min_valid_price')]),
                            max_day_price=int(list_of_string_numbers[names.get('max_valid_price')]),
                            start_time_stamp= get_today_market_opening_time(),
                            end_time_stamp= int(time.time())
                            )
    return new_bss