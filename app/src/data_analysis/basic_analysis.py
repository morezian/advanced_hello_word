# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from app.src.interfaces.buysell_interface import BuySellStatus
from hazm import *


from app.src.data_reader.crawler import *
name2final_buy_sell_status_dict = {}
data_list = crawl_data()
for data in data_list:
    name2final_buy_sell_status_dict[data.name] = data.current_buy_sell_status

def normal_list (a):
    norm = [(float(i) - min(a)) / (max(a) - min(a)) for i in a]
    return norm

def get_buy_sell_status (row: dict):
    final_buy_sell = name2final_buy_sell_status_dict [row ["name"]]
    total_vol = row["civil_sell_vol"]+row["civil_buy_vol"]+row["human_sell_vol"]+row["human_buy_vol"]
    return BuySellStatus(row["trade_price"], row["final_price"], row.get("vol",total_vol) , row["human_buy_vol"], row["human_buy_count"],
                         row["human_sell_vol"],
                         row["human_sell_count"],
                         row["civil_buy_vol"], row["civil_buy_count"], row["civil_sell_vol"], row["civil_sell_count"],
                         row["first_trade"],
                         get_today_market_opening_time(), row["time_stamp"],
                         row.get("min_day_price", final_buy_sell.min_day_price),
                         row.get("max_day_price", final_buy_sell.max_day_price),
                         row.get("min_day_touched_price", final_buy_sell.min_day_touched_price),
                         row.get("max_day_touched_price", final_buy_sell.max_day_touched_price))


def retrieve_stock_buy_sell_status_list (df, stock_name):
    df_name = df[df ["name"] == stock_name]
    ans = []
    for index, row in df_name.iterrows():
        bs = get_buy_sell_status(row)
        ans.append(bs)
    return ans



def update_df (df):
    min_day_price_list = []
    max_day_price_list = []
    min_day_touched_price_list = []
    max_day_touched_price_list = []
    vol_list = []
    for index, row in df.iterrows():
        try:
            final_buy_sell = get_buy_sell_status(row)
            min_day_price_list.append(final_buy_sell.min_day_price)
            max_day_price_list.append(final_buy_sell.max_day_price)
            min_day_touched_price_list.append(final_buy_sell.min_day_touched_price)
            max_day_touched_price_list.append(final_buy_sell.max_day_touched_price)
            vol_list.append(final_buy_sell.vol)
        except:
            print (row ["name"])
            df.drop(index=index, inplace=True)
    df ["min_day_price"] = min_day_price_list
    df ["max_day_price"] = max_day_price_list
    df ["vol"] = vol_list






def simple_plot (x_list, y_list_list, y_label_list, title):
    for i, y_list in enumerate(y_list_list):
        plt.plot(x_list, y_list, label=y_label_list[i])
    plt.title (title)
    plt.legend()
    plt.show()



def get_df (file_path):
    df = pd.read_csv (file_path)
    return df



def show_power_price(buy_sell_status_list: [BuySellStatus]):
    time_list = [datetime.utcfromtimestamp(buy_sell_status.end_time_stamp + 60*60) for buy_sell_status in buy_sell_status_list]
    price_list = [buy_sell_status.trade_price for buy_sell_status in buy_sell_status_list]
    buy_power_list = [buy_sell_status.get_human_buy_ratio_power() for buy_sell_status in buy_sell_status_list]

    #price_list = normal_list(price_list)
    #buy_power_list = normal_list(buy_power_list)
    simple_plot(time_list, [price_list, buy_power_list], ["price", "buy_power"], title = "Hi Web, price")



df = get_df ("../../data/csv/1609029827.csv")
sahm ="هاي وب"
buy_sell_list = retrieve_stock_buy_sell_status_list(df, sahm)
show_power_price(buy_sell_list)

#update_df(df)
#df.to_csv("../../data/Saved_CSV/1609029828.csv")






