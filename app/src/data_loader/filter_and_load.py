from app.src.stock.filter import *
from app.src.data_loader.csv_loader import *
from app.src.data_loader.telegram_loader import *

class FiliterAndLoad:
    def __init__(self, stock):
        self.__filter = Filter(stock)
        self.__csv_loader = CsvLoader()
        self.__all_tel_loader = TelegramLoader(token="1483369722:AAFQJOLnQeKZd5QjRD4wiI6pfAqoOu-m0Rk", id ="-444966767")
        self.__super_tel_loader =TelegramLoader(token="1370460089:AAHda25aodvumQO98eR50tnvVouohJ3_VlY", id="-412898183")
        self.__strong_tel_loader = TelegramLoader(token="1486040039:AAEDA2JVfpu14VbCWhYdV8mShlyYYoGHPrU", id="-408293635")