import json
import flask
from flask_restful import Resource, Api, request
from flask import Response
from app.src.stock.stocks_manager import *
from app.src.data_reader.crawler import *
from app.src.data_loader.status_loader.telegram_loader import *
from datetime import timedelta
import datetime
import pymysql

class History(Resource):

    def myconverter(self, o):
        if isinstance(o, datetime):
            return o.__str__()
            
    def get_timestamp(self,input_date):
        return int(datetime.datetime(year=int(input_date[0:4]),
                                    month=int(input_date[5:7]),
                                    day=int(input_date[8:10]),
                                    hour=20, minute=30, second=0, tzinfo=datetime.timezone.utc).timestamp()
                )

    def post(self):
        start_time = time()
        input = json.loads(request.data)
        name = input.get("Name")
        end_timestamp = input.get("EndTimeStamp")

        connection = pymysql.connect(host='localhost',  # 79.175.176.165
                                     user='admin',
                                     password='vwB75K',
                                     database='trade_db',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                # Read a single record
                #if rowCount == -1:
                
                if name == '*':
                    sql = "SELECT * FROM `history_tbl` WHERE `end_time_stamp` >= %s"
                    cursor.execute(sql, (self.get_timestamp(end_timestamp)))
                else:
                    sql = "SELECT * FROM `history_tbl` WHERE `latinName` = %s and `end_time_stamp` >= %s"
                    cursor.execute(sql, (name, self.get_timestamp(end_timestamp)))

                result = cursor.fetchall()
                res_dict = []
                for r in result:
                    buy_sell_status = BuySellStatus(human_buy_vol= float(r["human_buy_vol"]),
                                human_buy_count= int(r["human_buy_count"]),
                                human_sell_vol= float(r["human_sell_vol"]),
                                human_sell_count= int(r["human_sell_count"]),
                                civil_buy_vol= float(r["civil_buy_vol"]),
                                civil_buy_count= int(r["civil_buy_count"]),
                                civil_sell_vol= float(r["civil_sell_vol"]),
                                civil_sell_count= int(r["civil_sell_count"]),
                                trade_price= int(r["trade_price"]),
                                vol= float(r["vol"]),
                                final_price= int(r["final_price"]),
                                first_trade= int(r["first_trade"]),
                                min_day_price=float(r["min_day_price"]),
                                max_day_price=float(r["max_day_price"]),
                                start_time_stamp= r["start_time_stamp"],
                                max_day_touched_price= int(r["max_day_touched_price"]),
                                min_day_touched_price= int(r["min_day_touched_price"]),
                                end_time_stamp= r["end_time_stamp"]
                                )
                    ans = {
                        "name": r["name"],
                        "latin_name": r["latin_name"],
                        "market_cap": r["market_cap"],
                        "shares_count" : r["shares_count"],
                        "score": -1,
                        "buy_sell_status": buy_sell_status.to_dict()
                    }
                    res_dict.append(ans)

        return res_dict