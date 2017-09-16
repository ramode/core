if "__main__" in __name__:
    import sys
    sys.path.insert(0,'..')

import models
import models.accounts
import asyncio
import uvloop

class Actor:

    async def run(self):
        while True:
            await self.action()

    async def action(self):
        print(models.accounts.Service)
        exit()



if "__main__" in __name__:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop=asyncio.get_event_loop()

    models.psql_db.init('billing', host='127.0.0.1')

    a=Actor()

    try:
        loop.create_task(a.run())
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
