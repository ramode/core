if "__main__" in __name__:
    import sys, os
    cwd = os.path.dirname(__file__)
    sys.path.insert(0,cwd)
    sys.path.insert(0,os.path.join(cwd,'..'))

import models

import asyncio
import uvloop
import aioamqp
import msgpack
import string
import types


def rpc(cb):
    async def rpc_inner(channel, body, envelope, properties):
        args = msgpack.unpackb(body)
        if type(args) == list:
            generator = cb(*args)
        if type(args) == dict:
            generator = cb(**args)

        async for i in generator:
            response = msgpack.packb(i)
            await channel.basic_publish(
                payload = response,
                exchange_name='',
                routing_key=properties.reply_to,
                properties={
                    'correlation_id': properties.correlation_id,
                },
                )

        await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)
    return rpc_inner



async def test_cb(body):
    print (body)
    for i in range(110):
        yield i


def bind(protocol):
    async def bind_inner(cb,name):
        channel = await protocol.channel()
        await channel.queue(name)
        await channel.basic_consume(rpc(cb), queue_name=name)
    return bind_inner


async def go():
    models.psql_db.init('billing', host='127.0.0.1', user='postgres')

    transport, protocol = await aioamqp.connect()
    binder = bind(protocol)

    await binder(test_cb,"test")

    import callbacks
    rpc = []

    for class_ in callbacks.callbacks:
        cname = class_.__name__
        holder = class_(class_)

        for name in filter(lambda x: x[0] != '_' and type(getattr(holder,x)) == types.MethodType, dir(holder)):
            print("register method rpc.%s.%s" % (cname, name))
            callback = getattr(holder,name)
            await binder(callback,"rpc.%s.%s" % (cname, name))

        rpc.append(holder)

    return transport, protocol, rpc


if "__main__" in __name__:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop=asyncio.get_event_loop()

    try:
        server = loop.run_until_complete(go())
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
