import mysql.connector
from app.src.interfaces.buysell_interface import BuySellStatus
from typing import *


class MysqlConnector:
    def __init__(self, host, username, password, database, port=3300):
        self.connector = mysql.connector.connect(host=f"{host}", user=username, password=password,
                                                 database=database
                                                 )

    def get_instance(self):
        return self.connector.cursor()


class TradeMysqlLoader:
    def __init__(self, host, username, password, database, port=3309, history_table="history_tbl"):
        self.curser = MysqlConnector(host=host, password=password, database=database, port=port,
                                     username=username).get_instance()
        self.history_tbl = history_table

    def insert_trade_list_to_db(self, datalist: Dict[str,BuySellStatus], batch_size=1000):
        datalist = self._extract_db_format_data(datalist)
        for items in range(0, len(datalist), batch_size):
            self.curser.executemany(f"""INSERT INTO {self.history_tbl} {tuple(history_table_schema.keys())}
                                      VALUES {tuple(history_table_schema.values())}""", datalist)

    def _extract_db_format_data(self, datalist: List[StockHistory]):
        extracted_data_list = []
        for symbol in datalist:
            ...
        return extracted_data_list

    def update_stock_history_list_in_db(self, datalist):
        ...


history_table_schema = {
    "id": "%s",
    "latin_name": "%s",
    "farsi_name": "%s",
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
    "min_price": "%d",
    "max_price": "%d",
    "max_touched_price": "%d",
    "min_touched_price": "%d",
    "first_price": "%d",
    "final_price": "%d",
    "last_price": "%d",
    "end_timestamp": "%d",
    "vol": "%d",
    "shares_count": "%d",
    "start_timestamp": "%d",
}
history_table_schema = {k: v for k, v in sorted(history_table_schema.items(), key=lambda item: item[0])}
a = HistoryMysqlLoader(host="168.119.202.175", port=3309, username='admin', password='5}w:3M6%Wtv5sDe(')