import requests

from app.src.stock.stock import *
class csv_loader:
    def __init__(self, file_path, col_name):
        self.__file_path = file_path
        self.__col_name = col_name

    def add_stock (self, stock:Stock):
        pass