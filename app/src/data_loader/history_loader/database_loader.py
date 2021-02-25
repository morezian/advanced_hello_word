import mysql.connector
from app.src.interfaces.stock_history_interface import StockHistory
from typing import *


class MysqlConnector:
    def __init__(self, host, username, password, database, port=3306):
        self.connector = mysql.connector.connect(host=f"{host}", user=username, password=password, database=database
                                                 )

    def get_instance(self):
        return self.connector.cursor()


def _extract_db_format_data(datalist: Dict[str, StockHistory]):
    extracted_data_list = []
    for symbol in datalist.values():
        symbol_dict = OrderedDict()
        buy_sells = {}
        for key in history_table_schema.keys():
            try:
                symbol_dict[key] = symbol[key]
            except KeyError:
                buy_sells = {**buy_sells, **{key: item[key] for item in symbol.buy_sell_status_list}}
        for day in buy_sells:
            extracted_data_list.append({**symbol_dict, **day})
    # extracted_data_list += [{**symbol_dict, **row} for row in buy_sells]
    return extracted_data_list


class HistoryMysqlLoader:
    def __init__(self, host, username, password, database, port=3306, history_table="history_tbl"):
        self.curser = MysqlConnector(host=host, password=password, database=database, port=port,
                                     username=username).get_instance()
        self.history_tbl = history_table

    def insert_stock_history_list_to_db(self, datalist: Dict[str, StockHistory], batch_size=1000):
        datalist = _extract_db_format_data(datalist)
        for items in range(0, len(datalist), batch_size):
            self.curser.executemany(f"""INSERT INTO {self.history_tbl} {tuple(history_table_schema.keys())}
                                      VALUES {tuple(history_table_schema.values())}""", datalist)

    def update_stock_history_list_in_db(self, datalist):
        ...


history_table_schema = {
    # "id"  : "%s",
    "latin_name": "%s",
    "name": "%s",
    "market_cap": "%d",
    "human_buy_count": "%d",
    "human_sell_count": "%d",
    "human_buy_vol": "%d",
    "human_sell_vol": "%d",
    "civil_buy_count": "%d",
    "civil_sell_count": "%d",
    "civil_buy_vol": "%d",
    "civil_sell_vol": "%d",
    "civil_buy_price": "%d",
    "human_sell_price": "%d",
    "civil_sell_price": "%d",
    "min_day_price": "%d",
    "max_day_price": "%d",
    "max_day_touched_price": "%d",
    "min_day_touched_price": "%d",
    "first_trade": "%d",
    "final_price": "%d",
    "trade_price": "%d",
    "end_time_stamp": "%d",
    "vol": "%d",
    "shares_count": "%d",
    "start_time_stamp": "%d",
}
history_table_schema = {k: v for k, v in sorted(history_table_schema.items(), key=lambda item: item[0])}
# a = HistoryMysqlLoader(host="168.119.202.175",port=3309,username='admin',password='5}w:3M6%Wtv5sDe(')
