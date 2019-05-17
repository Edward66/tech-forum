from datetime import datetime

from peewee import *

from tech_forum.settings import database


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        database = database
