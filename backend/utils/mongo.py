from os import getenv
from pymongo import MongoClient

mgclient = MongoClient(getenv('MONGO_DB_CONNECT'))
global_db = mgclient[getenv('GLOBAL_DB_NAME', default='global')]