from pymongo import MongoClient
from decouple import config
from uuid import uuid4
import dns
import random
import uuid
import bcrypt

def get_connection(collection_name):
    try:
        client=MongoClient(config('MONGO_URL'))
        collection=client[config("MONGO_DB")][collection_name]
        # if collection.acknowledged:
        #     print("Mongo db not connected")
        #     return False
        return {'status':True,'data':collection}
    except Exception as e:
        return {"status":False,'data':e.__str__()}

