from datetime import datetime
class Filter:
    BAD = -20
    WEAK = -7
    NORMAL = 0
    GOOD = 2
    STRONG = 5
    SUPER = 8
    def __init__(self, current_buy_sell_status_dict, current_interval_buy_sell_status_dict):
        self.__current_buy_sell_status_dict = current_buy_sell_status_dict
        self.__current_interval_buy_sell_status_dict = current_interval_buy_sell_status_dict
        self.__filter_name = [Filter.BAD, Filter.WEAK, Filter.NORMAL, Filter.GOOD, Filter.STRONG, Filter.SUPER]

    def __get_key (self, is_real):
        if is_real == True:
            return "real"
        return "all"

    def __get_buy_sell_status (self, is_real, is_interval):
        key = self.__get_key(is_real)
        if is_interval == True:
            buy_sell_status = self.__current_interval_buy_sell_status_dict[key][-1]  # 5mins
        else:
            buy_sell_status = self.__current_buy_sell_status_dict[key]
        return buy_sell_status



    def __scale (self, value, old_max, old_min, new_max, new_min):
        old_range = (old_max - old_min)
        new_range = (new_max - new_min)
        new_value = (((value - old_min) * new_range) / old_range) + new_min
        return new_value

    def __filter_smaller (self, input, cmp_list):
        if len (cmp_list) != len (self.__filter_name):
            raise Exception("length of cmp and filter must be equal")
        for i in range (len (cmp_list)):
            if input < cmp_list [i]:
                if i == 0:
                    return self.__filter_name[i]
                return self.__scale(input, cmp_list [i], cmp_list[i-1], self.__filter_name[i], self.__filter_name[i-1])
        return self.__filter_name[-1]


    def buy_power_ratio (self, is_real, is_interval):
        buy_sell_status =  self.__get_buy_sell_status(is_real, is_interval)
        ratio = buy_sell_status.get_human_buy_ratio_power()

        cmp_list = [0.6, 0.9, 1.1, 1.4, 2, 4]
        ans = self.__filter_smaller(ratio, cmp_list)


        #print (f"buy power ration is {ans}")
        return ans


    def avg_buy_per_code (self, is_real, is_interval):
        buy_sell_status =  self.__get_buy_sell_status(is_real, is_interval)
        per_code = buy_sell_status.get_average_buy_per_code_in_million_base()
        cmp_list = [12, 18, 21, 25, 35, 55]
        ans = self.__filter_smaller(per_code, cmp_list)
        #print (f"avg buy per code is {ans}")
        return ans


    def human_buy_count (self, is_real, is_interval):
        buy_sell_status =  self.__get_buy_sell_status(is_real, is_interval)
        count = buy_sell_status.human_buy_count
        time_duration_second = buy_sell_status.end_time_stamp - buy_sell_status.start_time_stamp
        time_duration_minute = time_duration_second // 60
        print (is_interval, time_duration_minute)
        if time_duration_minute <= 10:
            cmp_list = [3, 10, 25, 40, 70, 150]
        elif time_duration_minute <= 45:
            cmp_list = [5, 25, 40, 100, 200, 300]
        elif time_duration_minute <= 120:
            cmp_list = [20, 60, 120, 300, 600, 800]
        else:
            cmp_list = [40, 90, 180, 450, 900, 1400]
        ans = self.__filter_smaller(count, cmp_list)
        #print (f"human buyt count is {ans}")
        return ans


    def trade_price (self):
        buy_sell_status =  self.__get_buy_sell_status(False, False)
        price_in_percent = buy_sell_status.trade_price_in_percent
        price_in_rial = buy_sell_status.trade_price
        if price_in_rial == buy_sell_status.max_day_price:
            return -100000
        domain = buy_sell_status.max_day_price_in_percent
        low = Filter.WEAK
        high = Filter.SUPER

        y = (high-low)/(2*domain)
        ans = price_in_percent*y +domain*y - high
        ans = -ans
        #print (f"trade price is {ans}")
        return ans



    def recent_to_board_buy_power_ratio(self):
        recent_buy_sell = self.__get_buy_sell_status(is_real=False, is_interval=True)
        board_buy_sell = self.__get_buy_sell_status(is_real=False, is_interval=False)
        previous_board_buy_sell = board_buy_sell - recent_buy_sell
        if previous_board_buy_sell.is_significant() == False: #first minutes of the bazzar
            return Filter.NORMAL
        previous_board_power = previous_board_buy_sell.get_human_buy_ratio_power()
        recent_power = recent_buy_sell.get_human_buy_ratio_power()
        input = recent_power / (previous_board_power + 0.0000000001)
        cmp_list = [0.4, 0.6, 1, 1.3, 2.5, 5]
        ans = self.__filter_smaller(input, cmp_list)
        #print (f"recent power is {ans}")
        return ans


    def recent_to_board_vol(self):
        recent_buy_sell = self.__get_buy_sell_status(is_real=False, is_interval=True)
        board_buy_sell = self.__get_buy_sell_status(is_real=False, is_interval=False)
        board_vol = board_buy_sell.vol
        recent_vol = recent_buy_sell.vol
        board_time = board_buy_sell.end_time_stamp - board_buy_sell.start_time_stamp
        recent_time = recent_buy_sell.end_time_stamp - recent_buy_sell.start_time_stamp
        input = (recent_vol / (board_vol+0.0000001))*(board_time/(recent_time+0.00000001))
        cmp_list = [0.4, 0.6, 0.9, 1.3, 2.5, 5]
        ans = self.__filter_smaller(input, cmp_list)
        #print (f"recent vol is {ans}")

        return ans

    def __get_score (self):
        is_real = False
        is_interval = False
        ans = 3*(self.human_buy_count(is_real, is_interval) + 1.5*self.avg_buy_per_code(is_real, is_interval) + \
              2*self.buy_power_ratio(is_real, is_interval))/4.5
        is_interval = True
        ans+= 3*((self.human_buy_count(is_real, is_interval) + 1.5*self.avg_buy_per_code(is_real, is_interval) + \
              2*self.buy_power_ratio(is_real, is_interval)))/4.5
        ans += self.trade_price()
        ans += self.recent_to_board_buy_power_ratio()
        ans += self.recent_to_board_vol()
        ans = ans / 9
        return ans


    def __get_score_level (slef, score):
        if score >= Filter.STRONG:
            return Filter.SUPER
        if score >= Filter.GOOD+1.5:
            return Filter.STRONG
        if score >= Filter.NORMAL:
            return Filter.GOOD
        if score >= Filter.WEAK:
            return Filter.NORMAL
        else:
            return Filter.WEAK


    def get_total_strength (self):
        score = self.__get_score()
        score_level = self.__get_score_level(score)
        #print (f"total score is {score}")
        return score, score_level



    def filter_event (self, is_real, is_interval):
        key = self.__get_key(is_real)
        #interval_list = self.__stock.interval_list_dict [key]
        #TODO implement event detection on interval list.
        return 0