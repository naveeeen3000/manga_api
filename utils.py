from decouple import config
import random
import uuid
import bcrypt
from uuid import uuid4


def get_connection(collection_name):
    try:
        from pymongo import MongoClient
        client=MongoClient(config('MONGO_URL'))
        collection=client[config("MONGO_DB")][collection_name]
        # if collection.acknowledged:
        #     print("Mongo db not connected")
        #     return False
        return {'status':True,'data':collection}
    except Exception as e:
        return {"status":False,'data':e.__str__()}


def update_manga(collection_name):
    coll=get_connection(collection_name)
    

    res=coll.find({},{"_id":0})
    i=0
    for r in res:
        id=uuid.uuid1().hex
        status=coll.update_one(r,{"$set":{"manga_id":id}})
        if status.acknowledged:
            print("changes made...")




def validate_login_creds(data):
    collection=get_connection("users")
    if not collection['status']:
        return {'status':False,'data':'db connection failure'}
    collection=collection['data']
    email=data['email']
    if not email:
        return {'status':False,'data':'email not present'}
    res=collection.find_one({"email":email},{'_id':0})
    if res:
        print("already there............................")
        return {"status":False,'data':"email already registered"}
    if not res:
        salt=bcrypt.gensalt()
        hashed_password=bcrypt.hashpw(str(data['password']).encode('utf-8'),salt)
        data['password']=hashed_password
        return {"status":True,"data":data}



def generate_user_token():

    return uuid4()


def get_mysql_connection():
    import mysql.connector
    con=mysql.connector.connect(host=config("MYSQL_HOST"),
                                user=config("MYSQL_USER"),
                                passwd=config("PASSWORD"),
                                database=config("DATABASE")
                                    )
    return con
    # print(con)
def insert_into_sql(con,query:str,values:tuple):
    try:
        cursor=con.cursor()
        cursor.execute(str(query),values)
        con.commit()
        # if res != None:
        print("inserted",values[1])
    except Exception as e:
        print(query,values)
        print(e.__str__())
        con.rollback()

def insert_query_builder(mongo_con,uuid):
    res=mongo_con.find_one({'manga_id':uuid},{
        '_id':0,
        'chapters':0,
        'genre':0
    })
    
    try:
        query="INSERT INTO {table_name} \
                (cover_image,title,alternative_titles,author,manga_status,average_rating,\
                    popularity_rank,rating_rank,cover,end_date,release_date,description,manga_uuid)\
                    VALUES  \
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(
                    table_name="manga")
        values=(    res.get('cover_image',None),
                    res.get('title',None).replace("'",''),
                    res.get('alternative',None).replace("'",""),
                    res.get('author',None).replace("'",''),
                    res.get('status',None),
                    res.get('average_rating',None),
                    res.get('popularity_rank',None),
                    res.get('rating_rank',None),
                    str(res.get('cover',None)),
                    res.get('end_date',None),
                    res.get('release_date',None),
                    res.get('description',None).replace("'",""),
                    res.get('manga_id',None)
                )
    except Exception as e:
        print(e.__str__())
        return False,False
    
    return query,values


def migrate():
    res=get_connection('manga')
    if res['status']==True:
        mongo_collection=res['data']
    else:
        print(res['data'])
        return 
    manga_uuids=list(mongo_collection.find({},{'_id':0,'manga_id':1}))
    connection=get_mysql_connection()
    for manga_uuid in manga_uuids:
        id=manga_uuid['manga_id']
        query,values=insert_query_builder(mongo_collection,id)
        if query==False and values==False:
            continue
        insert_into_sql(connection,query,values)
