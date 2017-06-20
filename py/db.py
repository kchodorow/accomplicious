import os

from flask import g
from pymongo import MongoClient

def get_db():
    if not hasattr(g, 'mongodb'):
        g.mongodb = connect_db()
    return g.mongodb[os.environ['MONGODB_DB']]

def connect_db():
    return MongoClient(os.environ['MONGODB_URI'])

def close_db():
    if hasattr(g, 'mongodb'):
        g.mongodb.close()
