from flask import current_app, g
from pymongo import MongoClient


def get_db():
    if 'db' not in g:
        mongo_uri = current_app.config['MONGO_URI']
        client = MongoClient(mongo_uri)
        g.db = client[current_app.config['MONGO_DBNAME']]
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.client.close()

def init_app(app):
    app.teardown_appcontext(close_db)