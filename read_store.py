from app.src.stock.stocks_manager import *
import json
from datetime import *
import threading
from app.src.data_loader.trade_loader.websocket_utility import *
#sorted_history = [(y.market_human_buy_power_ratio, x) for x, y in crawler.history.items()]
# sorted_history.sort(reverse=True)

START_BAZAR_HOUR = 9
END_BAZAR_HOUR = 13
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
        print("crawler created")
        if not is_in_bazar_time() and not TESTING:
            pause_until_hour(START_BAZAR_HOUR)

        manager = StocksManager(crawler, LoadData(True))
        while (datetime.now().hour != END_BAZAR_HOUR):
            manager.update()
            manager.load()


async def handle(websocket, path):
    WebSocketUtility.get_instance().WebSocketDict[websocket] = False
    while True:
        if WebSocketUtility.get_instance().WebSocketDict[websocket]:
            print('before sending')
            mm = WebSocketUtility.get_instance().get_stock_list()
            await websocket.send(str(type(mm)))
            WebSocketUtility.get_instance().WebSocketDict[websocket] = False

if __name__ == "__main__":
   
    x = threading.Thread(target=main_process)
    x.start()
    try:
        start_server = websockets.serve(handle, "0.0.0.0", 4001)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server)
        loop.run_forever()
    except:
        print('exception')
    finally:
        print('finally')
        await start_server.wait_closed()