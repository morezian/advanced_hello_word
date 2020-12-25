from app.src.stock.filter import *
from app.src.data_loader.csv_loader import *
from app.src.data_loader.telegram_loader import *

class FiliterAndLoad:
    def __init__(self, stock):
        self.__filter = Filter(stock)
        self.__csv_loader =