from .base import *

DEBITING_METHODS = [
    (0,'day'),
    (1,'mounthbyday'),
    (2,'mounth'),
    (3,'onetimestart')
    (4,'onetimeend')
]

SERVICE_STATE = [
    (0,'on'), # доступна
    (1,'admin off'), # запрещенна админом, включается админом
    (2,'suspend'), # не включать при пополнении баланса, включается пользователем
    (3,'block') # включать при пополнении баланса
]

class Account(BaseModel):
    consumer = PrimaryKeyField()
    provider = ForeignKeyField(self, to_field='consumer', related_name='consumers')
    form = CharField()
    personal_data = HStoreField()
    balance = CurrencyField()
    deleted = BooleanField(default=False)


from .nases import Nas
from .constants import SERVICE_TYPE

class Service(BaseModel):
    account = ForeignKeyField(Account, related_name='services')
    type = CharField()
    access = ForeignKeyField(Nas, related_name='services')

    check = HStoreField()
    respond = HStoreField()
    location = HStoreField() # адрес

    debiting = SmallIntegerField(choices = DEBITING_METHODS)
    state = SmallIntegerField(choices = SERVICE_STATE)
    start_at = CurrencyField()
    stop_at = CurrencyField()
    cost = CurrencyField()

    @post_save(sender=Service)
    def on_change(model_class, instance, created):
        ServiceChange.insert(service=instance.id, state=instance.state)

class ServiceChange(BaseModel):
    service = ForeignKeyField(Service)
    date = DateTimeField(default = datetime.datetime.now)
    state = SmallIntegerField(choices = SERVICE_STATE)


class Balance(BaseModel):
    account = ForeignKeyField(Account, related_name='balances')
    ammount = CurrencyField()
    check = JSONField()

    @post_save(sender=Balance)
    def on_pay(model_class, instance, created):
        if created:
            q = Account.update(balance=Account.balance+instance.ammount).where(Account.consumer == instance.account)
            q.execute()
