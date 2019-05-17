from peewee import MySQLDatabase

from apps.users.models import User
from tech_forum.settings import database


def init():
    """生成表"""
    database.create_tables([User])


if __name__ == '__main__':
    init()
