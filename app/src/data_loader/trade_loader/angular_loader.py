from app.src.data_loader.trade_loader.server import *

import asyncio
import websockets
import threading
import pymysql
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
    
    def __insert_into_db(self, connection, stock_dict):
        #with self.connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `daily_trades` (`name`) VALUES (%s)"
            print('name ', stock_dict["name"])
            cursor.execute(sql, (stock_dict["name"]))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

    def load_stock_list(self, stock_list):
        print(stock_list)
        self.__signal_count += len(stock_list)
        res_dict = []
        connection = pymysql.connect(host='localhost', #79.175.176.165
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
