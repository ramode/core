from .base import *

from .constants import *

class Nas(BaseModel):
    type = CharField(choices=NAS_TYPE)
    service = CharField(choices=SERVICE_TYPE)
    identity = CharField()
    secret = CharField()
    location = HStoreField()
