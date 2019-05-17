from peewee_async import Manager

import tornado
from tornado import web

from tech_forum.urls import urlpatterns
from tech_forum.settings import settings, database

if __name__ == '__main__':
    # 集成json到wtforms
    import wtforms_json

    wtforms_json.init()

    app = web.Application(urlpatterns, debug=True, **settings)
    app.listen(8001)

    objects = Manager(database=database)
    # no need for sync anymore!
    database.set_allow_sync(False)
    app.objects = objects

    tornado.ioloop.IOLoop.current().start()
