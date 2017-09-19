import models.accounts
import string
import types


class User:
    def __init__(self, database):
        self.database = database

#    def connect(self,cb):
#        def inner(*a,**kw):
#            self.database.connect()
#            res = cb(*a,**kw)
#            self.database.close()
#            return res
#        return inner

    async def new(self, provider:int, personal_data:dict):
        def keygen(l):
            return "".join([random.choice(string.ascii_lowercase+string.digits) for i in range(l)])

        await self.database.connect_async()
        async with self.database.atomic_async():
            account = models.accounts.Account.create(
                provider=provider,
                personal_data=personal_data
                ).execute()
            check = {
                'login': str(account).zfill(8),
                'password': keygen(6)
                }
            respond = {
                'rights': ['cabinet','help']
            }
            lk = models.accounts.Service.create(
                account=account,
                type="web-user",
                access=None,
                check=check,
                respond=respond
                ).execute()

        yield account
        self.database.close()


    async def get(self, provider:int, consumer:int):
        await self.database.connect_async()
        yield models.accounts.Account.get((Account.provider == provider) & (Account.consumer == consumer)).execute()
        self.database.close()

    async def list(self, provider:int):
        await self.database.connect_async()
        for row in  models.accounts.Account.select().where(Account.provider == provider & Account.deleted == False).execute():
            yield row
        self.database.close()

