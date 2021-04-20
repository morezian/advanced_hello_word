import mysql.connector as connector
from app.src.interfaces.stock_history_interface import StockHistory
from typing import *

def connection(**config):
    try:
        c = connector.connect(**config)
        return c
    except Exception as e:
        print (e)
        exit(1)

def _extract_db_format_data(datalist: Dict[str, StockHistory]):
    extracted_data_list = []
    for symbol in datalist.values():
        symbol_dict = OrderedDict()
        buy_sells = {}
        for key in history_table_schema.keys():
            try:
                symbol_dict[key] = symbol[key]
            except AttributeError:
                buy_sells = {**buy_sells, **{key: item[key] for item in symbol.buy_sell_status_list}}
        extracted_data_list.append({**symbol_dict, **buy_sells})
    return extracted_data_list


class HistoryMysqlLoader:
    def __init__(self, host, username, password, database, port=3306, history_table="history_tbl"):
        self.connection = connection(host=host, password=password, database=database, port=port,
                                     user=username)
        self.history_tbl = history_table
    def insert_stock_history_list_to_db(self, datalist: Dict[str, StockHistory], batch_size=1000):
        datalist = _extract_db_format_data(datalist)
        row = []
        curser = self.connection.cursor()
        for items in range(0, len(datalist), batch_size):
            query = f"""INSERT INTO history_tbl (`civil_buy_count`, `civil_buy_price`, `civil_buy_vol`, `civil_sell_count`, `civil_sell_price`, `civil_sell_vol`,`end_time_stamp`, `final_price`, `first_trade`, `human_buy_count`, `human_buy_vol`, `human_sell_count`, `human_sell_price`, `human_sell_vol`, `latin_name`, `market_cap`, `max_day_price`, `max_day_touched_price`, `min_day_price`, `min_day_touched_price`, `name`, `shares_count`, `start_time_stamp`, `trade_price`, `vol`)
                                      value (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            for i in datalist:
                d = {k: v for k, v in sorted(i.items(), key=lambda item: item[0])}
                row.append(tuple(d.values()))
            curser.executemany(query, row)
            self.connection.commit()

    def __del__(self):
        self.connection.close()

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
    "end_time_stamp": "%s",
    "vol": "%d",
    "shares_count": "%d",
    "start_time_stamp": "%s",
}
history_table_schema = {k: v for k, v in sorted(history_table_schema.items(), key=lambda item: item[0])}
