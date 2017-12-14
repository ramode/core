import asyncio
import uvloop
import aioamqp
import umsgpack as msgpack
import uuid


class Client():

    def __init__(self, routing_key, protocol=None):
        self.routing_key = routing_key
        self.protocol = protocol
        self.channel = None
        self.q = asyncio.Queue()

#    def on_response(self,channel, body, envelope, properties): # async *
#        return self.q.put(msgpack.unpackb(body))               # await *

    async def on_response(self,channel, body, envelope, properties): # async *
        data = msgpack.unpackb(body)
        print(data)
        await self.q.put(data)               # await *

    async def connect(self):
        self.transport, self.protocol = await aioamqp.connect()

    async def get_channel(self):
        self.channel = await self.protocol.channel()
        result = await self.channel.queue_declare(queue_name='', exclusive=True)
        self.callback_queue = result['queue']
        await self.channel.basic_consume(self.on_response, no_ack=True, queue_name=self.callback_queue)


    async def __call__(self,*args):
        if not self.protocol:
            await self.connect()
        if not self.channel:
            await self.get_channel()

        corr_id = str(uuid.uuid4())

        data = msgpack.packb(args)

        await self.channel.basic_publish(
            payload=data,
            exchange_name='',
            routing_key=self.routing_key,
            properties={
                'reply_to': self.callback_queue,
                'correlation_id': corr_id,
                'delivery_mode': 2,
            },
        )


