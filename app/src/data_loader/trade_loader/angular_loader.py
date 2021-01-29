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
            response_stock = stock.to_dict()
            
            #response_stock["stock_info"] = 
            #response_stock["5 minute"] = stock.last_second_buy_sell_status(False, 5 * 60).to_dict()
            #response_stock["30 seconds"] = stock.last_second_buy_sell_status(False, 30).to_dict()
            #response_stock["board"] = stock.current_buy_sell_status_dict['all'].to_dict()
            #get_average_buy_per_code_in_million_base
            #human_buy_count
            #trade_price
            #trade_price_in_percent
            # type = score_level 
            #dict1["score"] = stock.score
            #a = json.dumps(dict1)
            
            res_dict.append(response_stock)
        #WebSocketUtility.get_instance().set_send_status(True)
        for i in WebSocketUtility.get_instance().WebSocketDict:
            WebSocketUtility.get_instance().WebSocketDict[i] = True
        WebSocketUtility.get_instance().set_stock_list(res_dict)
        print('signaled')
