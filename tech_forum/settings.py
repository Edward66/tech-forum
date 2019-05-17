import peewee_async

settings = {
    'static_path': '/Users/liangshaohua/workspace/tech-forum/tech_forum/static',
    'static_url_prefix': '/static/',
    'template_path': 'templates',
    'secret_key': 'niP*9UhUTQ7!Ybs&',
    'db': {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '112233',
        'name': 'message_board',
        'port': 3306,
    },
    'redis': {
        'host': '127.0.0.1',
    }

}

database = peewee_async.MySQLDatabase(
    'forum', host='127.0.0.1', port=3306, user='root', password='112233',
)
