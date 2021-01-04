from datetime import datetime

def get_today_market_opening_time():
    return int(datetime(year=datetime.now().year,
                                    month=datetime.now().month,
                                    day=datetime.now().day,
                                    hour=9, minute=0, second=0).timestamp())