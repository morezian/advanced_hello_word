import asyncio
import websockets
import logging
from websockets import *

logging.basicConfig(level=logging.INFO)

async def consumer_handler(websocket: WebSocketClientProtocol) -> None:
    async for message in websocket:
        log_message(message)
        print('r: ' + message)

async def consume(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}"
    async with websockets.connect(websocket_resource_url) as websocket:
        await consumer_handler(websocket)

def log_message(message: str) -> None:
    logging.info(f"Message: {message}")

async def produce(message: str, hostname: str, port: int) -> None:
    async with websockets.connect(f"ws://{hostname}:{port}") as ws:
        await ws.send(message)
        received = await ws.recv()
        print('received', received)

if __name__ == '__main__':
    print('start')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume(hostname='localhost', port=4000))
    loop.run_forever()