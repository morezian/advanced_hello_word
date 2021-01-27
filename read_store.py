from app.src.stock.stocks_manager import *
import json
from datetime import *
#import _thread
import threading
from app.src.data_loader.trade_loader.websocket_utility import *
#sorted_history = [(y.market_human_buy_power_ratio, x) for x, y in crawler.history.items()]
#sorted_history.sort(reverse=True)

START_BAZAR_HOUR = 0
END_BAZAR_HOUR = 24
CRAWLING_HOUR = 3

SIGNAL_DETECTED = False

def is_in_bazar_time():
    now_hour = datetime.now().hour
    print(now_hour)
    if now_hour >= START_BAZAR_HOUR and now_hour <END_BAZAR_HOUR:
        return True
    return False

def pause_until_hour (hour):
    while True:
        if datetime.now().hour == hour: break


def start_srv(thread_name, delay):
    start_server = websockets.serve(handle, "localhost", 4000)
    
    loop.run_until_complete(start_server)
    #loop.run_forever()

async def register(websocket):
    WebSocketUtility.getInstance().Users.add(websocket)
    #USERS.add(websocket)

def main_process():
    sleep(5)
    while True:
        if not is_in_bazar_time() and not TESTING:
            pause_until_hour(CRAWLING_HOUR)
        crawler = DataCrawler(crawl_history=crawl_history, realtime=real_time, csv_file=csv_file_path)
        #print("crawler created")
        if not is_in_bazar_time() and not TESTING:
            pause_until_hour(START_BAZAR_HOUR)

        manager = StocksManager(crawler, LoadData(True))
        while (datetime.now().hour != END_BAZAR_HOUR):
            manager.update()
            manager.load()

async def handle(websocket, path):
    #name = await websocket.recv()
    #while True:
    print('ghasem')
    WebSocketUtility.getInstance().Users.add(websocket)
    for wws in WebSocketUtility.getInstance().Users:
        await wws.send('ishalla')
    #await register(websocket)

if __name__ == "__main__":
    cfg = json.load(open("config"))
    TESTING = cfg ["TESTING"]
    crawl_history = cfg ["crawl_history"]
    real_time = cfg ["realtime"]
    csv_file_path = cfg.get("csv_file_path")
    
    #_thread.start_new_thread(main_process, ())
    x = threading.Thread(target=main_process)
    x.start()
    
    start_server = websockets.serve(handle, "localhost", 4001)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
    print('salam')
    
    
#    start_server = websockets.serve(WebSocketUtility.getInstance().notify_all, "localhost", 6789)
#    asyncio.get_event_loop().run_until_complete(start_server)
#    asyncio.get_event_loop().run_forever()

