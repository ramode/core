from .base import *

from .constants import *
from .nases import Nas

class Account(BaseModel):
    consumer = PrimaryKeyField()
    provider = ForeignKeyField('self', to_field='consumer', related_name='consumers')
    personal_data = HStoreField()
    balance = CurrencyField()
    currency = SmallIntegerField(default=643)
    deleted = BooleanField(default=False)

    class Meta:
        indexes = (
            (('provider'), True),
        )

class Service(BaseModel):
    account = ForeignKeyField(Account, related_name='services')
    type = CharField(choices = SERVICE_TYPE)
    access = ForeignKeyField(Nas, related_name='services')

    check = HStoreField()
    respond = HStoreField()
    location = HStoreField() # адрес

    debiting = SmallIntegerField(choices = DEBITING_METHODS)
    state = SmallIntegerField(choices = SERVICE_STATE, default=3)

    debit_at = DateTimeField(default = datetime.datetime.now)
    periodic = BooleanField(default = False)

    start_at = CurrencyField(default = 0)
    stop_at = CurrencyField(default = 0)
    cost = CurrencyField()

    class Meta:
        indexes = (
            (('account'), True),
            (('access'), True),
        )


@post_save(sender=Service)
def on_change(model_class, instance, created):
    ServiceChange.insert(service=instance.id, state=instance.state)

class ServiceChange(BaseModel):
    service = ForeignKeyField(Service)
    date = DateTimeField(default = datetime.datetime.now)
    state = SmallIntegerField(choices = SERVICE_STATE)


class Balance(BaseModel):
    account = ForeignKeyField(Account, related_name='balances')
    txn_id = IntegerField()
    ammount = CurrencyField()
    currency = SmallIntegerField(default=643)
    cash = SmallIntegerField(choices=CASH_TYPE)
    vat = CurrencyField(default=0) #ндс
    check = JSONField()

    class Meta:
        indexes = (
            (('account','txn_id'), True),
        )


@post_save(sender=Balance)
def on_pay(model_class, instance, created):
    if created:
        if instance.currency == instance.account.currency:
            q = Account.update(balance=Account.balance+instance.ammount).where(Account.consumer == instance.account)
            q.execute()
