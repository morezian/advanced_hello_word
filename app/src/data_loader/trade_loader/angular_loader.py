from app.src.data_loader.trade_loader.server import *

import asyncio
import websockets
import threading
import pymysql
from datetime import datetime
from app.src.data_loader.trade_loader.websocket_utility import *


class AngularLoader():
    def __init__(self, signal_type):
        self.__signal_detected = False
        self.__signal = None
        self.__signal_type = signal_type
        self.__signal_count = 0
        print('Server Started')
        
    def get_signal_count(self):
        return self.__signal_count
    
    def __to_string_date(self, ts):
        return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    def __insert_into_db(self, connection, stock_dict):
        #with self.connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = """INSERT INTO daily_trades ( latinName, name, score,
            score_level,
            5m_human_buy_vol,
            5m_human_buy_count,
            5m_human_sell_vol,
            5m_human_sell_count,
            5m_civil_buy_vol,
            5m_civil_buy_count,
            5m_civil_sell_vol,
            5m_civil_sell_count,
            5m_trade_price,
            5m_vol,
            5m_first_trade,
            5m_final_price,
            5m_start_time_stamp,
            5m_end_time_stamp,
            5m_min_day_price,
            5m_max_day_price,
            5m_min_day_touched_price,
            5m_max_day_touched_price,
            5m_get_average_buy_per_code_in_million_base,
            5m_get_human_buy_ratio_power,
            5m_trade_price_in_percent,
            5m_final_price_in_percent,
            5m_max_day_price_in_percent,
            5m_first_trade_in_percent,
            5m_max_day_touched_in_percent,
            5m_min_day_touched_in_percent,
            30s_human_buy_vol,
            30s_human_buy_count,
            30s_human_sell_vol,
            30s_human_sell_count,
            30s_civil_buy_vol,
            30s_civil_buy_count,
            30s_civil_sell_vol,
            30s_civil_sell_count,
            30s_trade_price,
            30s_vol,
            30s_first_trade,
            30s_final_price,
            30s_start_time_stamp,
            30s_end_time_stamp,
            30s_min_day_price,
            30s_max_day_price,
            30s_min_day_touched_price,
            30s_max_day_touched_price,
            30s_get_average_buy_per_code_in_million_base,
            30s_get_human_buy_ratio_power,
            30s_trade_price_in_percent,
            30s_final_price_in_percent,
            30s_max_day_price_in_percent,
            30s_first_trade_in_percent,
            30s_max_day_touched_in_percent,
            30s_min_day_touched_in_percent,
            board_human_buy_vol,
            board_human_buy_count,
            board_human_sell_vol,
            board_human_sell_count,
            board_civil_buy_vol,
            board_civil_buy_count,
            board_civil_sell_vol,
            board_civil_sell_count,
            board_trade_price,
            board_vol,
            board_first_trade,
            board_final_price,
            board_start_time_stamp,
            board_end_time_stamp,
            board_min_day_price,
            board_max_day_price,
            board_min_day_touched_price,
            board_max_day_touched_price,
            board_get_average_buy_per_code_in_million_base,
            board_get_human_buy_ratio_power,
            board_trade_price_in_percent,
            board_final_price_in_percent,
            board_max_day_price_in_percent,
            board_first_trade_in_percent,
            board_max_day_touched_in_percent,
            board_min_day_touched_in_percent
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            
            print('name ', stock_dict["name"])
            cursor.execute(sql, (stock_dict["latin_name"], stock_dict["name"], stock_dict["score"], 
                                 stock_dict["score_level"],
                                 stock_dict["5m_buy_sell_status"]["human_buy_vol"],
                                 stock_dict["5m_buy_sell_status"]["human_buy_count"],
                                 stock_dict["5m_buy_sell_status"]["human_sell_vol"],
                                 stock_dict["5m_buy_sell_status"]["human_sell_count"],
                                 stock_dict["5m_buy_sell_status"]["civil_buy_vol"],
                                 stock_dict["5m_buy_sell_status"]["civil_buy_count"],
                                 stock_dict["5m_buy_sell_status"]["civil_sell_vol"],
                                 stock_dict["5m_buy_sell_status"]["civil_sell_count"],
                                 stock_dict["5m_buy_sell_status"]["trade_price"],
                                 int(stock_dict["5m_buy_sell_status"]["vol"]),stock_dict["5m_buy_sell_status"]["first_trade"],
                                 stock_dict["5m_buy_sell_status"]["final_price"],
                                 self.__to_string_date(stock_dict["5m_buy_sell_status"]["start_time_stamp"]),
                                 self.__to_string_date(stock_dict["5m_buy_sell_status"]["end_time_stamp"]),
                                 stock_dict["5m_buy_sell_status"]["min_day_price"],stock_dict["5m_buy_sell_status"]["max_day_price"],
                                 stock_dict["5m_buy_sell_status"]["min_day_touched_price"],stock_dict["5m_buy_sell_status"]["max_day_touched_price"],
                                 stock_dict["5m_buy_sell_status"]["get_average_buy_per_code_in_million_base"],
                                 stock_dict["5m_buy_sell_status"]["get_human_buy_ratio_power"],stock_dict["5m_buy_sell_status"]["trade_price_in_percent"],
                                 stock_dict["5m_buy_sell_status"]["final_price_in_percent"],stock_dict["5m_buy_sell_status"]["max_day_price_in_percent"],
                                 stock_dict["5m_buy_sell_status"]["first_trade_in_percent"],stock_dict["5m_buy_sell_status"]["max_day_touched_in_percent"],
                                 stock_dict["5m_buy_sell_status"]["min_day_touched_in_percent"],
                                 stock_dict["30s_buy_sell_status"]["human_buy_vol"],
                                 stock_dict["30s_buy_sell_status"]["human_buy_count"],stock_dict["30s_buy_sell_status"]["human_sell_vol"],
                                 stock_dict["30s_buy_sell_status"]["human_sell_count"],stock_dict["30s_buy_sell_status"]["civil_buy_vol"],
                                 stock_dict["30s_buy_sell_status"]["civil_buy_count"],stock_dict["30s_buy_sell_status"]["civil_sell_vol"],
                                 stock_dict["30s_buy_sell_status"]["civil_sell_count"],stock_dict["30s_buy_sell_status"]["trade_price"],
                                 int(stock_dict["30s_buy_sell_status"]["vol"]),stock_dict["30s_buy_sell_status"]["first_trade"],
                                 stock_dict["30s_buy_sell_status"]["final_price"],
                                 self.__to_string_date(stock_dict["30s_buy_sell_status"]["start_time_stamp"]),
                                 self.__to_string_date(stock_dict["30s_buy_sell_status"]["end_time_stamp"]),
                                 stock_dict["30s_buy_sell_status"]["min_day_price"],
                                 stock_dict["30s_buy_sell_status"]["max_day_price"],stock_dict["30s_buy_sell_status"]["min_day_touched_price"],
                                 stock_dict["30s_buy_sell_status"]["max_day_touched_price"],
                                 stock_dict["30s_buy_sell_status"]["get_average_buy_per_code_in_million_base"],
                                 stock_dict["30s_buy_sell_status"]["get_human_buy_ratio_power"],
                                 stock_dict["30s_buy_sell_status"]["trade_price_in_percent"],stock_dict["30s_buy_sell_status"]["final_price_in_percent"],
                                 stock_dict["30s_buy_sell_status"]["max_day_price_in_percent"],stock_dict["30s_buy_sell_status"]["first_trade_in_percent"],
                                 stock_dict["30s_buy_sell_status"]["max_day_touched_in_percent"],stock_dict["30s_buy_sell_status"]["min_day_touched_in_percent"],
                                 stock_dict["board_buy_sell_status"]["human_buy_vol"],stock_dict["board_buy_sell_status"]["human_buy_count"],
                                 stock_dict["board_buy_sell_status"]["human_sell_vol"],stock_dict["board_buy_sell_status"]["human_sell_count"],
                                 stock_dict["board_buy_sell_status"]["civil_buy_vol"],stock_dict["board_buy_sell_status"]["civil_buy_count"],
                                 stock_dict["board_buy_sell_status"]["civil_sell_vol"],stock_dict["board_buy_sell_status"]["civil_sell_count"],
                                 stock_dict["board_buy_sell_status"]["trade_price"],int(stock_dict["board_buy_sell_status"]["vol"]),
                                 stock_dict["board_buy_sell_status"]["first_trade"],stock_dict["board_buy_sell_status"]["final_price"],
                                 self.__to_string_date(stock_dict["board_buy_sell_status"]["start_time_stamp"]),
                                 self.__to_string_date(stock_dict["board_buy_sell_status"]["end_time_stamp"]),
                                 stock_dict["board_buy_sell_status"]["min_day_price"],stock_dict["board_buy_sell_status"]["max_day_price"],
                                 stock_dict["board_buy_sell_status"]["min_day_touched_price"],stock_dict["board_buy_sell_status"]["max_day_touched_price"],
                                 stock_dict["board_buy_sell_status"]["get_average_buy_per_code_in_million_base"],
                                 stock_dict["board_buy_sell_status"]["get_human_buy_ratio_power"],stock_dict["board_buy_sell_status"]["trade_price_in_percent"],
                                 stock_dict["board_buy_sell_status"]["final_price_in_percent"],stock_dict["board_buy_sell_status"]["max_day_price_in_percent"],
                                 stock_dict["board_buy_sell_status"]["first_trade_in_percent"],stock_dict["board_buy_sell_status"]["max_day_touched_in_percent"],
                                 stock_dict["board_buy_sell_status"]["min_day_touched_in_percent"]))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            print("inserted")
            connection.commit()

    def load_stock_list(self, stock_list):
        print(stock_list)
        self.__signal_count += len(stock_list)
        res_dict = []
        connection = pymysql.connect(host='79.175.176.165', #79.175.176.165
                             user='admin',
                             password='vwB75K',
                             database='trade_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        with connection:
            for stock in stock_list:
                response_stock = {**stock.to_dict(), **{"score_level": self.__signal_type}}
                self.__insert_into_db(connection, response_stock)
                res_dict.append(response_stock)
        #WebSocketUtility.get_instance().set_send_status(True)
        #for i in WebSocketUtility.get_instance().WebSocketDict:
        #    #i.send(json.dumps(res_dict, sort_keys=True, indent=4))
        #    WebSocketUtility.get_instance().WebSocketDict[i] = True
        #WebSocketUtility.get_instance().set_stock_list(res_dict)
        
        """ with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT version()"
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)"""
        print('signaled')
