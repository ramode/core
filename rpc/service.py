if "__main__" in __name__:
    import sys
    sys.path.insert(0,'..')

import models.accounts

import asyncio
import aiozmq.rpc

import string

def keygen(l):
    return "".join([random.choice(string.ascii_lowercase+string.digits) for i in range(l)])


class ServerHandler(aiozmq.rpc.AttrHandler):
    @aiozmq.rpc.method
    def new_user(self, provider:int, personal_data:dict) -> int:
        database = models.accounts.Account.Meta.database
        with database.transaction():
            account = models.accounts.Account.create(provider=provider,personal_data=personal_data)

            check = {
                'login':str(account).zfill(8),
                'password': keygen(6)
                }
            respond = {
                'rights': ['cabinet','crm']
            }

            lk = models.accounts.Service.create(account=account,type="web-user",access=None,check=check,respond=respond)

        return account.consumer



async def go():
    server = await aiozmq.rpc.serve_rpc(
        ServerHandler(), bind='tcp://127.0.0.1:5672')
    return server


if "__main__" in __name__:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop=asyncio.get_event_loop()

    try:
        server = loop.run_until_complete(go())
        loop.run_forever()
    finally:
        server.close()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
