from peewee import *
from playhouse.postgres_ext import *
from playhouse.signals import Model, post_save
from playhouse.pool import PooledPostgresqlExtDatabase
import datetime

# http://docs.peewee-orm.com/en/latest/peewee/database.html#dynamically-defining-a-database
# http://docs.peewee-orm.com/en/latest/peewee/api.html#Database.init

psql_db = PooledPostgresqlExtDatabase(None)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

class CurrencyField(DecimalField):
    pass
