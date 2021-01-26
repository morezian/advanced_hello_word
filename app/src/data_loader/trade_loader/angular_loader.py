#import websocket
#ws = websocket.WebSocket()
#ws.connect("ws://example.com/websocket", http_proxy_host="proxy_host_name", http_proxy_port=3128)

from app.src.data_loader.trade_loader.server import *

import asyncio
import websockets
import threading
from app.src.data_loader.trade_loader.websocket_utility import *

class AngularLoader():
    def __init__(self, signal_type):
        #threading.Thread.__init__(self)
        #start_server = websockets.serve(producer_handler, "localhost", 8765)
        #asyncio.get_event_loop().run_until_complete(start_server)
        #asyncio.get_event_loop().run_forever()
        self.__signal_detected = False
        self.__signal = None
        print('before server started')
        #self.__server = Server()
        
        #start_server = websockets.serve(self.__server.ws_handler, 'localhost', 4000)
        #start_server = websockets.serve(self.send_signal, 'localhost', 4000)
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(start_server)

        #_thread.start_new_thread(self.listen_ws_server, ('ali', 2, ))

        print('Server Started')
    
    def listen_ws_server(self, threadName, delay):
        print('saieedi')


        loop = self.get_or_create_eventloop() #asyncio.get_event_loop()
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        loop.run_until_complete(start_server)
        print('after creating ws server')
        loop.run_forever()

    async def send_signal(self, websocket, path):
        while True:
            print('wait send signal') #now = datetime.datetime.utcnow().isoformat() + "Z"
            #if self.__signal_detected == True:
            await websocket.send('ali')
            #   self.__signal_detected = False

    def get_or_create_eventloop(self):
        try:
            print('mdt')
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                print('exxxxxx')
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop() 

    def load_stock_list (self, stock_list):
        #WebSocketUtility.getInstance().set_send_status(True)
        #WebSocketUtility.getInstance().set_stock_list(stock_list)
        print('signaled')
        if USERS:  # asyncio.wait doesn't accept an empty list
            #message = users_event()
            asyncio.wait([user.send(stock_list) for user in USERS])
        
        #self.__signal = stock_list
        #self.__signal_detected = True
        #for stock in stock_list:
        #self.__server.send_to_clients('sammmmm')
        #return "salam"
        """
        string_stock = self.__get_string_stock_list(stock_list)#urllib.parse.quote(self.__get_string_stock(stock))
        url = f'https://api.telegram.org/bot' + str(self.__token) + '/sendMessage?text=' + string_stock + '&chat_id=' + str(self.__id)
        #requests.get(url)
        #self.__session = FuturesSession()
        if self.is_special == False and 1 == 2:
            self.__session.get(url,hooks={'response': self.response_hook})
            #sleep(1)
        else:
            resp = requests.get(url)
            #print (resp)
        #requests.get(url)
        """
    

"""async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")"""