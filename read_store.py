from app.src.stock.stocks_manager import *
import json
#sorted_history = [(y.market_human_buy_power_ratio, x) for x, y in crawler.history.items()]
#sorted_history.sort(reverse=True)

START_BAZAR_HOUR = 9
END_BAZAR_HOUR = 13
CRAWLING_HOUR = 3

def is_in_bazar_time():
    now_hour = datetime.now().hour
    if now_hour >=START_BAZAR_HOUR and now_hour <END_BAZAR_HOUR:
        return True
    return False

def pause_until_hour (hour):
    while True:
        if datetime.now().hour == hour: break

if __name__ == "__main__":
    cfg = json.load(open("config"))
    TESTING = cfg ["TESTING"]
    crawl_history = cfg ["crawl_history"]
    real_time = cfg ["realtime"]
    csv_file_path = cfg.get("csv_file_path")

    while True:
        if not is_in_bazar_time() and not TESTING:
            pause_until_hour(CRAWLING_HOUR)
        crawler = DataCrawler(crawl_history=crawl_history, realtime=real_time, csv_file=csv_file_path)
        print("crawler created")
        if not is_in_bazar_time() and not TESTING:
            pause_until_hour(START_BAZAR_HOUR)

        manager = StocksManager(crawler, LoadData())
        while (datetime.now().hour != END_BAZAR_HOUR):
            manager.update()
            manager.load()