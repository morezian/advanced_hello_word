from app.src.stock.stocks_manager import *
import json
from datetime import *
import threading
import asyncio
from app.src.data_loader.trade_loader.websocket_utility import *
#sorted_history = [(y.market_human_buy_power_ratio, x) for x, y in crawler.history.items()]
# sorted_history.sort(reverse=True)

START_BAZAR_HOUR = 9
END_BAZAR_HOUR = 24
CRAWLING_HOUR = 3
cfg = json.load(open("config"))
TESTING = cfg["TESTING"]
crawl_history = cfg["crawl_history"]
real_time = cfg["realtime"]
csv_file_path = cfg.get("csv_file_path")


def is_in_bazar_time():
    now_hour = datetime.now().hour
    print(now_hour)
    if now_hour >= START_BAZAR_HOUR and now_hour < END_BAZAR_HOUR:
        return True
    return False


def pause_until_hour(hour):
    while True:
        if datetime.now().hour == hour:
            break


def main_process():
    sleep(5)
    while True:
        if not is_in_bazar_time() and not TESTING:
            pause_until_hour(CRAWLING_HOUR)
        crawler = DataCrawler(crawl_history=crawl_history,
                              realtime=real_time, csv_file=csv_file_path)
        print("Crawler created")
        if not is_in_bazar_time() and not TESTING:
            pause_until_hour(START_BAZAR_HOUR)

        manager = StocksManager(crawler, LoadData(True))
        while (datetime.now().hour != END_BAZAR_HOUR):
            manager.update()
            manager.load()

def send_message_thread():
    print('\n In send_message_thread ... \n')
    asyncio.run(send_message())

async def send_message():
    sleep(5)
    print('\n Start sending messages to clients \n')
    while True:
        for ws in WebSocketUtility.get_instance().WebSocketDict:
            print('There is at least one websocket')
            if WebSocketUtility.get_instance().WebSocketDict[ws]:
                print(' \n Before sending \n')
                mm = WebSocketUtility.get_instance().get_stock_list()
                dict1 = {}
                dict1["response"] = mm 
                result = json.dumps(mm, sort_keys=True, indent=4)
                #print(result)
                await ws.send(result) 
                WebSocketUtility.get_instance().WebSocketDict[ws] = False

"""async def send_message(ws):
    sleep(5)
    print('start sending messages to clients')
    while True:
        if WebSocketUtility.get_instance().WebSocketDict[ws]:
            print('before sending')
            mm = WebSocketUtility.get_instance().get_stock_list()
            dict1 = {}
            dict1["response"] = mm 
            result = json.dumps(mm, sort_keys=True, indent=4)
            #print(result)
            await ws.send(result) 
            WebSocketUtility.get_instance().WebSocketDict[ws] = False"""

async def handle(websocket, path):
    WebSocketUtility.get_instance().WebSocketDict[websocket] = False
    print('\n New Connection \n')
    try:
        #y = threading.Thread(target=send_message, args=(websocket,))
        #y.start()
        """while True:
            if WebSocketUtility.get_instance().WebSocketDict[websocket]:
                print('before sending')
                mm = WebSocketUtility.get_instance().get_stock_list()
                dict1 = {}
                dict1["response"] = mm 
                result = json.dumps(mm, sort_keys=True, indent=4)
                #print(result)
                await websocket.send(result) 
                WebSocketUtility.get_instance().WebSocketDict[websocket] = False
"""
        """if WebSocketUtility.get_instance().WebSocketDict[websocket]:
                print('before sending')
                mm = WebSocketUtility.get_instance().get_stock_list()
                dict1 = {}
                dict1["response"] = mm 
                result = json.dumps(mm, sort_keys=True, indent=4)
                #print(result)
                await websocket.send(result) 
                WebSocketUtility.get_instance().WebSocketDict[websocket] = False"""
        """    #print('new Con')
            for ws in WebSocketUtility.get_instance().WebSocketDict.keys(): 
                if WebSocketUtility.get_instance().WebSocketDict[ws]:
                    print('before sending')
                    mm = WebSocketUtility.get_instance().get_stock_list()
                    dict1 = {}
                    dict1["response"] = mm 
                    result = json.dumps(mm, sort_keys=True, indent=4)
                    #print(result)
                    await ws.send(result) 
                    WebSocketUtility.get_instance().WebSocketDict[ws] = False
        """
        
    finally:
        print('delete websocket key')
        #del WebSocketUtility.get_instance().WebSocketDict[websocket]

if __name__ == "__main__":
    
    x = threading.Thread(target=main_process)
    x.start()
    
    y = threading.Thread(target=send_message_thread)
    y.start()
       #asyncio.run(send_message())
    try:
        print('\n Before handle... \n')
        start_server = websockets.serve(handle, "0.0.0.0", 4001)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server)
        loop.run_forever()
    except Exception as e:
        print(' Exception', str(e))
    finally:
        print(' Finally')
        #start_server.wait_closed()