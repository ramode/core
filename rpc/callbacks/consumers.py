import models.accounts
import string
import types

async def new_user(self, provider:int, personal_data:dict):

    def keygen(l):
        return "".join([random.choice(string.ascii_lowercase+string.digits) for i in range(l)])

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

    yield account


async def get_user(self, provider:int, consumer:int):
    yield models.accounts.Account.get((Account.provider == provider) & (Account.consumer == consumer))


async def list_users(self, provider:int):
    for row in  models.accounts.Account.select().where(Account.provider == provider & Account.deleted == False):
        yield row


