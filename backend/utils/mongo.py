from os import getenv
from pymongo import MongoClient

mgclient = MongoClient(getenv('DB_CONNECT'))
db = mgclient[getenv('DB_NAME', default='beta')]