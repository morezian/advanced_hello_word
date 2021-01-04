from app.src.interfaces.buysell_interface import BuySellStatus
import csv
from app.src.interfaces.symbol import Symbol
from app.src.data_reader.crawler import get_today_market_opening_time
class CsvReader:
    def __init__(self,file: str):
        in_file = open(file, 'rt')
        self.__data = csv.DictReader(in_file)


    def read_next_batch(self,batch_size = 500):
        result = []
        for row in self.__data:
            if batch_size == 0: break
            batch_size -= 1
            status = BuySellStatus(
                end_time_stamp= int(row["time_stamp"]),
                trade_price= float(row["trade_price"]),
                final_price= float(row["final_price"]),
                human_buy_count= int(row["human_buy_count"]),
                human_buy_vol= int(row["human_buy_vol"]),
                human_sell_count= int(row["human_sell_count"]),
                human_sell_vol= int(row["human_sell_vol"]),
                civil_buy_count= int(row["civil_buy_count"]),
                civil_buy_vol= int(row["civil_buy_vol"]),
                civil_sell_count=int(row["civil_sell_count"]),
                civil_sell_vol=int(row["civil_sell_vol"]),
                first_trade=int(row["first_trade"]),
                min_day_price=float (row["min_day_price"]),
                max_day_price=  float (row["max_day_price"]),
                min_day_touched_price=float (row["min_day_touched_price"]),
                max_day_touched_price=float(row["max_day_touched_price"]),
                vol= float (row["vol"]),
                start_time_stamp=get_today_market_opening_time()
            )
            result.append(
                Symbol(name=row["name"],current_buy_sell_status=status,latin_name='',unique_id='')
            )
        return result