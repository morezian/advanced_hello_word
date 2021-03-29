from app.src.loggers.file_logger import logger
from requests import sessions
from app.src.interfaces.buysell_interface import BuySellStatus
import datetime
from app.src.interfaces.stock_history_interface import StockHistory
from bs4 import BeautifulSoup
session = sessions.session()
import concurrent.futures

xxx =0

class HistoryCrawler:
    data = []
    def __init__(self,data,history_period_by_days=5):
        self.data = data
        self.history_period_by_days = self.__get_list_of_past_days(history_period_by_days)

    def parse_history_data(self,raw_history ,name,latin_name):
        buy_sell_status_list = []
        for single_day in raw_history:
            extracted_data = extract_info_from_html_page(single_day)
            if extracted_data:
                buy_sell_status_list.append(BuySellStatus(human_buy_count=int(extracted_data['human_buy_count']),
                                                          civil_buy_count=int(extracted_data['civil_buy_count']),
                                                          human_sell_count=int(extracted_data['human_sell_count']),
                                                          civil_sell_count=int(extracted_data['civil_sell_count']),
                                                          human_buy_vol=int(extracted_data['human_buy_vol']),
                                                          civil_buy_vol=int(extracted_data['civil_buy_vol']),
                                                          human_sell_vol=int(extracted_data['human_sell_vol']),
                                                          civil_sell_vol=int(extracted_data['civil_sell_vol']),
                                                          final_price= extracted_data['final_price'],
                                                          trade_price= extracted_data['last_traded_price'],
                                                          first_trade= extracted_data['first_traded_price'],
                                                          min_day_touched_price= extracted_data['min_traded_price'],
                                                          max_day_touched_price= extracted_data['max_traded_price'],
                                                          min_day_price= extracted_data['min_valid_price'],
                                                          max_day_price= extracted_data['max_valid_price'],
                                                          end_time_stamp = int(extracted_data['end_timestamp']),
                                                          # start_time_stamp= int(extracted_data['start_timestamp']),
                                                          vol= extracted_data['vol']
                                                          )
                                                )
                history = StockHistory(name=name, latin_name=latin_name, buy_sell_status_list=buy_sell_status_list)
                history.market_cap = extracted_data['shares_count'] * buy_sell_status_list[0].final_price
                history.shares_count = extracted_data['shares_count']

        return history

    def __get_list_of_past_days(self,num_days: int):
        days_list = []
        for d in range(1,num_days+1):
            days_list.append((datetime.datetime.now() - datetime.timedelta(days=d)).strftime("%Y%m%d"))
        return days_list

    def __crawl_signle_history_data(self, url):
        global xxx
        while True:
            history_data = session.get(url,timeout = 20)
            if history_data.status_code == 200: break
        print (f"feteched {xxx}")
        xxx += 1
        return history_data

    def __get_history_data_list(self):
        final_result = []
        i = 0
        for symbol in self.data:
            if symbol.unique_id == '57944184894703821':
                with concurrent.futures.ThreadPoolExecutor() as executor:
                        x = [f"http://cdn.tsetmc.com/Loader.aspx?ParTree=15131P&i={symbol.unique_id}&d={day}" for day in self.history_period_by_days]
                        results = executor.map(self.__crawl_signle_history_data, x)
                        final_result.append(results)
                        break

        return final_result

    def get_stock_name2history(self):
        self.data = self.data
        histoed_buy_sell_status_dict = dict()
        history_data_list = self.__get_history_data_list()
        for symbol , history_data in zip(self.data,history_data_list):
            histoed_buy_sell_status_dict[symbol.name] = self.parse_history_data(history_data, symbol.name,
                                                                                symbol.latin_name)
        # for symbol in self.data:
        #     history_data = session.get(f"http://www.tsetmc.com/tsev2/data/clienttype.aspx?i={symbol.unique_id}"
        #                                 )
        #     histoed_buy_sell_status_dict[symbol.name] = self.parse_history_data(history_data.text,symbol.name,symbol.latin_name)
        #     print (f"added {len (histoed_buy_sell_status_dict)}")
        #     logger.info(f"fetched {symbol.name}")
        return histoed_buy_sell_status_dict

def __get_timestamp(input_date):
    return int(datetime.datetime(year=int(input_date[0:4]),
                                month=int(input_date[4:6]),
                                day=int(input_date[6:]),
                                hour=20, minute=30, second=0, tzinfo=datetime.timezone.utc).timestamp()
            )

def extract_info_from_html_page(response)-> dict:
    res = []
    output_dict = dict()
    if response.status_code == 200:
        soup = BeautifulSoup(response.text)
        page_variables = soup.findAll('script')
        try:
            BestLimitData = str(page_variables[6].contents[0]).split('=')[1].split(';')[0]
            BestLimitData = eval(BestLimitData)[-1]
        except:
            return None
        page_variables = str(page_variables[5].contents[0]).split(';')
        for idx,x in enumerate(page_variables):
            v = x.split('=')
            try:
                res.append(eval(v[1]))
            except:
                pass
        res[1] = res[1][-1]
        res[2] = res[2][-1]
        res[4] = res[4][-1]
        res.append(BestLimitData)
        output_dict['human_buy_count'] = res[7][0]
        output_dict['human_sell_count'] = res[7][2]
        output_dict['human_buy_vol'] = res[7][4]
        output_dict['human_sell_vol'] = res[7][6]
        output_dict['civil_buy_count'] = res[7][1]
        output_dict['civil_sell_count'] = res[7][3]
        output_dict['civil_buy_vol'] = res[7][5]
        output_dict['civil_sell_vol'] = res[7][7]
        output_dict['human_buy_price'] = res[7][16]
        output_dict['civil_buy_price'] = res[7][17]
        output_dict['human_sell_price'] = res[7][18]
        output_dict['civil_sell_price'] = res[7][19]
        output_dict['min_valid_price'] = res[0][1][2]
        output_dict['max_valid_price'] = res[0][1][1]
        output_dict['min_traded_price'] = int(res[1][7])
        output_dict['max_traded_price'] = int(res[1][6])
        output_dict['first_traded_price'] = int(res[1][4])
        output_dict['final_price'] = int(res[1][3])
        output_dict['last_traded_price'] = int(res[1][2])
        # output_dict['start_timestamp'] =
        output_dict['end_timestamp'] = __get_timestamp(str(res[3][0][0]))
        output_dict['vol'] =  int(res[1][10])
        output_dict['shares_count'] = round(100 / res[6][0][3] * res[6][0][2])
        return output_dict
    else:
        raise Exception("error 500")

