from .base import *

DEBITING_METHODS = [
    (0,'day'),
    (1,'mounthbyday'),
    (2,'mounth'),
    (3,'onetimestart')
    (4,'onetimeend')
]

SERVICE_STATE = [
    (0,'off'),
    (1,'on'),
    (2,'suspend') #не включать при пополнении баланса
]

class Account(BaseModel):
    consumer = PrimaryKeyField()
    provider = ForeignKeyField(Account, to_field='consumer', related_name='consumers')
    form = CharField()
    personal_data = HStoreField()
    balance = CurrencyField()
    deleted = BooleanField(default=False)


class Service(BaseModel):
    account = ForeignKeyField(Account, related_name='services')
    type = CharField()
    check = HStoreField()
    respond = HStoreField()
    debiting = SmallIntegerField(choices = DEBITING_METHODS)
    state = SmallIntegerField(choices = SERVICE_STATE)
    start = CurrencyField()
    stop = CurrencyField()

class Balance(BaseModel):
    account = ForeignKeyField(Account, related_name='balances')
    ammount = CurrencyField()
    check = JSONField()

    @post_save(sender=Balance)
    def on_pay(model_class, instance, created):
        if created:
            q = Account.update(balance=Account.balance+instance.ammount).where(Account.consumer == instance.account)
            q.execute()
