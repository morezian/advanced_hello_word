



def get_vip_stock_list (stock_name2stock_obj):
    vip_data_file = open ("app/data/vip")
    vip_stock_list = []
    for stock_name in vip_data_file:
        stock_name = stock_name.strip()
        stock = stock_name2stock_obj.get (stock_name)
        if stock:
            vip_stock_list.append(stock)
    return vip_stock_list
