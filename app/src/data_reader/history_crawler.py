from time import timezone
from app.src.loggers.file_logger import logger
from requests import sessions
from app.src.data_reader import crawler
from requests_futures.sessions import FuturesSession
from app.src.interfaces.buysell_interface import BuySellStatus
import datetime
import requests
data = crawler.crawl_data()
session = sessions.session()
# past_year_timestamp = int((datetime.datetime.utcnow() - datetime.timedelta(days=365)).timestamp())
# current_timestamp = int(datetime.datetime.now().timestamp())
def __get_timestamp(input_date):
    return int(datetime.datetime(year=int(input_date[0:4]),
                                month=int(input_date[4:6]),
                                day=int(input_date[6:]),
                                hour=20,minute=30,second=0,tzinfo=datetime.timezone.utc).timestamp()
                )

def parse_history_data(raw_history: str):
    raw_history = raw_history.split(';')
    buy_sell_status_list = []
    raw_history = [i.split(',') for i in raw_history]
    [i.append(__get_timestamp(i[0])) for i in raw_history]
    for i in raw_history:
        buy_sell_status_list.append(BuySellStatus(human_buy_count=i[1],civil_buy_count=i[2],human_sell_count=i[3],civil_sell_count=i[4],
                        human_buy_vol=i[5],civil_buy_vol=i[6],human_sell_vol=i[7],civil_sell_vol=i[8],
                        human_buy_value=i[9],civil_buy_value=i[10],human_sell_value=i[11],civil_sell_value=i[12],
                        histored_timestamp=i[13]
                        ))
    return buy_sell_status_list

def get_stock_name2history():
    histoed_buy_sell_status_dict = dict()
    for symbol in data:
        history_data = session.get(f"http://www.tsetmc.com/tsev2/data/clienttype.aspx?i={symbol.unique_id}",
                                    )
        histoed_buy_sell_status_dict[symbol.latin_name] = parse_history_data(history_data.text)
        logger.info(f"fetched {symbol.name}")
    return histoed_buy_sell_status_dict
