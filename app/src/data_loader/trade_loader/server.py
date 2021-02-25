import asyncio
import logging
import websockets
from websockets import *

logging.basicConfig(level=logging.INFO)

class Server:
    clients = set()

    async def register(self, ws: WebSocketClientProtocol) -> None:
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects.')
    
    async def unregister(self, ws: WebSocketClientProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects.')
    
    async def send_to_clients(self, message: str) -> None:
        print('to client')
        if self.clients:
            await asyncio.wait([client.send('hello: ' + message) for client in self.clients])
    
    async def ws_handler(self, ws: WebSocketClientProtocol, uri: str) -> None:
        print('await register')
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)
    
    async def distribute(self, ws: WebSocketClientProtocol) -> None:
        async for message in ws:
            await self.send_to_clients(message)