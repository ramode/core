import asyncio
import uvloop
import aioamqp
import msgpack
import uuid

from .client import Client
from .service import rpc


async def test():
    c = Client('test')
    await c("Hello")


if "__main__" in __name__:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop=asyncio.get_event_loop()

    try:
        server = loop.run_until_complete(test())
        loop.run_forever()
    finally:

        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
