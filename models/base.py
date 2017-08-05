from peewee import *
from playhouse.postgres_ext import *
from playhouse.signals import Model, post_save

psql_db = PostgresqlDatabase('billing')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

class CurrencyField(DecimalField):
    pass
