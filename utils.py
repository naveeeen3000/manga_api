from pymongo import MongoClient
from decouple import config
import dns
import random
import uuid


def get_connection(collection_name):
    client=MongoClient(config('MONGO_URL'))
    collection=client[config("MONGO_DB")][collection_name]
    # if collection.acknowledged:
    #     print("Mongo db not connected")
    #     return False
    return collection


def update_manga(collection_name):
    coll=get_connection(collection_name)
    

    res=coll.find({},{"_id":0})
    i=0
    for r in res:
        id=uuid.uuid1().hex
        status=coll.update_one(r,{"$set":{"manga_id":id}})
        if status.acknowledged:
            print("changes made...")