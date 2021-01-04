from app.src.interfaces.buysell_interface import BuySellStatus

class Symbol:
    def __init__(self,name,latin_name,unique_id,current_buy_sell_status):
        self.name: str = name
        self.latin_name: str = latin_name
        self.unique_id: str = unique_id
        self.current_buy_sell_status:BuySellStatus = current_buy_sell_status