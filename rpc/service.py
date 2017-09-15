if "__main__" in __name__:
    import sys
    sys.path.insert(0,'..')

import models.accounts

import asyncio
import uvloop
import aioamqp
import msgpack
import string

def keygen(l):
    return "".join([random.choice(string.ascii_lowercase+string.digits) for i in range(l)])

"""
class ServerHandler(aiozmq.rpc.AttrHandler):
    @aiozmq.rpc.method
    def new_user(self, provider:int, personal_data:dict) -> int:
        database = models.accounts.Account.Meta.database
        with database.atomic():
            account = models.accounts.Account.create(provider=provider,personal_data=personal_data)

            check = {
                'login': str(account).zfill(8),
                'password': keygen(6)
                }
            respond = {
                'rights': ['cabinet','help']
            }
            lk = models.accounts.Service.create(account=account,type="web-user",access=None,check=check,respond=respond)

        return account.consumer

    @aiozmq.rpc.method
    def user(self,provider:int, consumer:int) -> dict:
        return models.accounts.Account.get((Account.provider == provider) & (Account.consumer == consumer))


    @aiozmq.rpc.method
    def users(self,provider:int) -> list:
        return models.accounts.Account.select().where(Account.provider == provider)
"""


def rpc(cb):
    async def rpc_inner(channel, body, envelope, properties):
        print(body)
        body = msgpack.unpackb(body)

        async for i in cb(body):
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


@rpc
async def accounts_cb(body):
    print (body)
    for i in range(110):
        yield i




async def go():
    transport, protocol = await aioamqp.connect()
    channel = await protocol.channel()
    await channel.queue('accounts')
    await channel.basic_consume(accounts_cb, queue_name='accounts')


    return transport, protocol


if "__main__" in __name__:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop=asyncio.get_event_loop()

    try:
        server = loop.run_until_complete(go())
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
