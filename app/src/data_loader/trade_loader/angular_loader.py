#import websocket
#ws = websocket.WebSocket()
#ws.connect("ws://example.com/websocket", http_proxy_host="proxy_host_name", http_proxy_port=3128)

from app.src.data_loader.trade_loader.server import *

import asyncio
import websockets
import threading
from app.src.data_loader.trade_loader.websocket_utility import *


class AngularLoader():
    def __init__(self, signal_type):
        self.__signal_detected = False
        self.__signal = None
        self.__signal_type = signal_type
        print('Server Started')

    def load_stock_list(self, stock_list):
        print(stock_list)
        res_dict = []
        for stock in stock_list:
            response_stock = {**stock.to_dict(), **{"score_level": self.__signal_type}}
            res_dict.append(response_stock)
        #WebSocketUtility.get_instance().set_send_status(True)
        for i in WebSocketUtility.get_instance().WebSocketDict:
            WebSocketUtility.get_instance().WebSocketDict[i] = True
        WebSocketUtility.get_instance().set_stock_list(res_dict)
        print('signaled')
