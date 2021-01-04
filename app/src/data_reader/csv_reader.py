from app.src.interfaces.buysell_interface import BuySellStatus
import csv
from app.src.interfaces.symbol import Symbol
counter = 0
from app.src.data_reader.crawler import get_today_market_opening_time
class CsvReader:
    def __init__(self,file: str):
        in_file = open(file, 'rt')
        self.data = csv.reader(in_file)
        self.counter = 0

    def read_next_batch(self,batch_size = 500):
        result = []
        counter = 0
        for row in self.data:
            if counter == batch_size: break
            counter += 1
            if self.data.line_num == 1:
                continue
            status = BuySellStatus(
                                    end_time_stamp= int(row[1]),
                                    trade_price= int(row[2]),
                                    final_price= int(row[3]),
                                    human_buy_count= int(row[4]),
                                    human_buy_vol= int(row[5]),
                                    human_sell_count= int(row[6]),
                                    human_sell_vol= int(row[7]),
                                    civil_buy_count= int(row[8]),
                                    civil_buy_vol= int(row[9]),
                                    civil_sell_count=int(row[10]),
                                    civil_sell_vol=int(row[11]),
                                    first_trade=int(row[12]),                                                                                   start_time_stamp=get_today_market_opening_time()
                                    )
            result.append(
                Symbol(name=row[0],current_buy_sell_status=status,latin_name='',unique_id='')
            )
        return result