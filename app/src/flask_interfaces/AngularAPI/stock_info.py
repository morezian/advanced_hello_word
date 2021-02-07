import json
import flask
from flask_restful import Resource, Api, request
from app.src.stock.stocks_manager import *
from app.src.data_reader.crawler import *
from app.src.data_loader.status_loader.telegram_loader import *
from datetime import timedelta
import pymysql


class StockInfo(Resource):

    def myconverter(self, o):
        if isinstance(o, datetime):
            return o.__str__()

    def post(self):
        start_time = time()
        input = json.loads(request.data)
        start_timestamp = input.get("StartTimeStamp")
        count = input.get("Count")
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
                sql = "SELECT * FROM `daily_trades` WHERE `score_level`=%s"
                cursor.execute(sql, (signal_type_list,))
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
                        "5m_buy_sell_status": {
                            "al": r["5m_human_buy_vol"]
                        },
                        "30s_buy_sell_status": {
                            "al": r["30s_human_buy_vol"]
                        },
                        "board_buy_sell_status": {
                            "al": r["board_human_buy_vol"]
                        }
                    }
                    res_dict.append(ans)
                #print(result)
        # return json.dumps(result, default = self.myconverter)
        return res_dict
