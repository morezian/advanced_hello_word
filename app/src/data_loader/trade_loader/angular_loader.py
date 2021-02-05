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
        self.connection = pymysql.connect(host='localhost',
                             user='admin',
                             password='vwB75K',
                             database='trade_db',
                             cursorclass=pymysql.cursors.DictCursor)
        
    def get_signal_count(self):
        return self.__signal_count

    def load_stock_list(self, stock_list):
        print(stock_list)
        self.__signal_count += len(stock_list)
        res_dict = []
        for stock in stock_list:
            response_stock = {**stock.to_dict(), **{"score_level": self.__signal_type}}
            res_dict.append(response_stock)
        #WebSocketUtility.get_instance().set_send_status(True)
        #for i in WebSocketUtility.get_instance().WebSocketDict:
        #    #i.send(json.dumps(res_dict, sort_keys=True, indent=4))
        #    WebSocketUtility.get_instance().WebSocketDict[i] = True
        #WebSocketUtility.get_instance().set_stock_list(res_dict)
        
        with self.connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
                
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT version()"
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)
            
        print('signaled')
