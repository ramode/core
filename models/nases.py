from .base import *

NAS_TYPE = [
    ('radius','Radius')
]
from .constants import SERVICE_TYPE

class Nas(BaseModel):
    type = CharField(choices=NAS_TYPE)
    service = CharField(choices=SERVICE_TYPE)
    identity = CharField()
    secret = CharField()
    location = HStoreField()
