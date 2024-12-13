from sqlalchemy.orm import DeclarativeBase
from .custom_types import *


class BaseModel(DeclarativeBase):
    pass



from .event import *