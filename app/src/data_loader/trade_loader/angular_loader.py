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
        print('Server Started')

    def load_stock_list(self, stock_list):
        print(stock_list)
        res_dict = []
        for stock in stock_list:
            dict1 = {}
            
            dict1['company'] = stock.name
            dict1['board power'] = stock.current_buy_sell_status_dict['all'].get_human_buy_ratio_power()
            dict1['score'] = stock.score
            res_dict.append(dict1)
        #WebSocketUtility.get_instance().set_send_status(True)
        for i in WebSocketUtility.get_instance().WebSocketDict:
            WebSocketUtility.get_instance().WebSocketDict[i] = True
        WebSocketUtility.get_instance().set_stock_list(res_dict)
        print('signaled')
