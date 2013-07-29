from django.db import models
from modeltools import Enum, EnumField


class MyModel(models.Model):

    class Color(Enum):
        RED = 'r'
        GREEN = 'g'
        BLUE = 'b'

    color = EnumField(Color, max_length=1)
