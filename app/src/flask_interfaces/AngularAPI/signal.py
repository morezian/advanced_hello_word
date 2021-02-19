import json
import flask
from flask_restful import Resource, Api, request
from app.src.stock.stocks_manager import *
from app.src.data_reader.crawler import *
from app.src.data_loader.status_loader.telegram_loader import *
from datetime import timedelta
import pymysql

class Signal(Resource):

    def myconverter(self, o):
        if isinstance(o, datetime):
            return o.__str__()

    def post(self):
        start_time = time()
        input = json.loads(request.data)
        start_timestamp = input.get("StartTimeStamp")
        end_timestamp = input.get("EndTimeStamp")
        rowCount = input.get("Count")
        rowCount = int(rowCount)
        signal_type_list = input.get("SignalTypeList")
        connection = pymysql.connect(host='79.175.176.165',  # 79.175.176.165
                                     user='admin',
                                     password='vwB75K',
                                     database='trade_db',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                # Read a single record
                if rowCount == -1:
                    sql = "SELECT * FROM `daily_trades` WHERE `score_level` in %s and `created_at` >= %s and `created_at` < %s"
                    cursor.execute(sql, (signal_type_list, start_timestamp, end_timestamp))
                else:
                    sql = "SELECT * FROM `daily_trades` WHERE `score_level` in %s and `created_at` >= %s and `created_at` < %s limit %s"
                    cursor.execute(sql, (signal_type_list, start_timestamp, end_timestamp, rowCount))
                result = cursor.fetchall()
                #ans = {
                #    "name": result["name"]
                #}
                res_dict = []
                for r in result:
                    ans = {
                        "name": r["name"],
                        "latin_name": r["latinName"],
                        "score": r["score"],
                        "score_level" : r["score_level"],
                        "5m_buy_sell_status": {
                            "5m_human_buy_vol": r["5m_human_buy_vol"],
                            "5m_human_buy_count": r["5m_human_buy_count"],
                            "5m_human_sell_vol": r["5m_human_sell_vol"],
                            "5m_human_sell_count": r["5m_human_sell_count"],
                            "5m_civil_buy_vol": r["5m_civil_buy_vol"],
                            "5m_civil_buy_count": r["5m_civil_buy_count"],
                            "5m_civil_sell_vol": r["5m_civil_sell_vol"],
                            "5m_civil_sell_count": r["5m_civil_sell_count"],
                            "5m_trade_price": r["5m_trade_price"],
                            "5m_vol": r["5m_vol"],
                            "5m_first_trade": r["5m_first_trade"],
                            "5m_final_price": r["5m_final_price"],
                            "5m_start_time_stamp": str(r["5m_start_time_stamp"]),
                            "5m_end_time_stamp": str(r["5m_end_time_stamp"]),
                            "5m_min_day_price": r["5m_min_day_price"],
                            "5m_max_day_price": r["5m_max_day_price"],
                            "5m_min_day_touched_price": r["5m_min_day_touched_price"],
                            "5m_max_day_touched_price": r["5m_max_day_touched_price"],
                            "5m_get_average_buy_per_code_in_million_base": r["5m_get_average_buy_per_code_in_million_base"],
                            "5m_get_human_buy_ratio_power": r["5m_get_human_buy_ratio_power"],
                            "5m_trade_price_in_percent": r["5m_trade_price_in_percent"],
                            "5m_final_price_in_percent": r["5m_final_price_in_percent"],
                            "5m_max_day_price_in_percent": r["5m_max_day_price_in_percent"],
                            "5m_first_trade_in_percent": r["5m_first_trade_in_percent"],
                            "5m_max_day_touched_in_percent": r["5m_max_day_touched_in_percent"],
                            "5m_min_day_touched_in_percent": r["5m_min_day_touched_in_percent"]
                        },
                        "30s_buy_sell_status": {
                            "30s_human_buy_vol": r["30s_human_buy_vol"],
                            "30s_human_buy_count": r["30s_human_buy_count"],
                            "30s_human_sell_vol": r["30s_human_sell_vol"],
                            "30s_human_sell_count": r["30s_human_sell_count"],
                            "30s_civil_buy_vol": r["30s_civil_buy_vol"],
                            "30s_civil_buy_count": r["30s_civil_buy_count"],
                            "30s_civil_sell_vol": r["30s_civil_sell_vol"],
                            "30s_civil_sell_count": r["30s_civil_sell_count"],
                            "30s_trade_price": r["30s_trade_price"],
                            "30s_vol": r["30s_vol"],
                            "30s_first_trade": r["30s_first_trade"],
                            "30s_final_price": r["30s_final_price"],
                            "30s_start_time_stamp": str(r["30s_start_time_stamp"]),
                            "30s_end_time_stamp": str(r["30s_end_time_stamp"]),
                            "30s_min_day_price": r["30s_min_day_price"],
                            "30s_max_day_price": r["30s_max_day_price"],
                            "30s_min_day_touched_price": r["30s_min_day_touched_price"],
                            "30s_max_day_touched_price": r["30s_max_day_touched_price"],
                            "30s_get_average_buy_per_code_in_million_base": r["30s_get_average_buy_per_code_in_million_base"],
                            "30s_get_human_buy_ratio_power": r["30s_get_human_buy_ratio_power"],
                            "30s_trade_price_in_percent": r["30s_trade_price_in_percent"],
                            "30s_final_price_in_percent": r["30s_final_price_in_percent"],
                            "30s_max_day_price_in_percent": r["30s_max_day_price_in_percent"],
                            "30s_first_trade_in_percent": r["30s_first_trade_in_percent"],
                            "30s_max_day_touched_in_percent": r["30s_max_day_touched_in_percent"],
                            "30s_min_day_touched_in_percent": r["30s_min_day_touched_in_percent"]
                        },
                        "board_buy_sell_status": {
                            "board_human_buy_vol": r["board_human_buy_vol"],
                            "board_human_buy_count": r["board_human_buy_count"],
                            "board_human_sell_vol": r["board_human_sell_vol"],
                            "board_human_sell_count": r["board_human_sell_count"],
                            "board_civil_buy_vol": r["board_civil_buy_vol"],
                            "board_civil_buy_count": r["board_civil_buy_count"],
                            "board_civil_sell_vol": r["board_civil_sell_vol"],
                            "board_civil_sell_count": r["board_civil_sell_count"],
                            "board_trade_price": r["board_trade_price"],
                            "board_vol": r["board_vol"],
                            "board_first_trade": r["board_first_trade"],
                            "board_final_price": r["board_final_price"],
                            "board_start_time_stamp": str(r["board_start_time_stamp"]),
                            "board_end_time_stamp": str(r["board_end_time_stamp"]),
                            "board_min_day_price": r["board_min_day_price"],
                            "board_max_day_price": r["board_max_day_price"],
                            "board_min_day_touched_price": r["board_min_day_touched_price"],
                            "board_max_day_touched_price": r["board_max_day_touched_price"],
                            "board_get_average_buy_per_code_in_million_base": r["board_get_average_buy_per_code_in_million_base"],
                            "board_get_human_buy_ratio_power": r["board_get_human_buy_ratio_power"],
                            "board_trade_price_in_percent": r["board_trade_price_in_percent"],
                            "board_final_price_in_percent": r["board_final_price_in_percent"],
                            "board_max_day_price_in_percent": r["board_max_day_price_in_percent"],
                            "board_first_trade_in_percent": r["board_first_trade_in_percent"],
                            "board_max_day_touched_in_percent": r["board_max_day_touched_in_percent"],
                            "board_min_day_touched_in_percent": r["board_min_day_touched_in_percent"]
                        },
                        "created_at": str(r["created_at"])
                    }
                    res_dict.append(ans)
                #print(result)
        #return json.dumps(res_dict, default = self.myconverter)
        return res_dict
