from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer
from utils import get_connection




@api_view(['GET'])
@authentication_classes([TokenAuthentication,BasicAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def manga_api_view(request):
    base_url =  "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
    result={
        "search":base_url+'search/?q=naruto',
        "manga_details":base_url+'manga/details/',
        'popular_manga':base_url+'manga/popular/',
        "by_genre":base_url+'manga/?genre=action',
        "by_tags":base_url+'manga/tags/?tag=comedy',
        'read_manga':base_url+'manga/read?manga_id=83f4e399-ca79-56b3-9058-9462f702ffa2'
    }
    return Response(result,status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def searchView(request):
    query_params=request.query_params
    search_query=query_params.get("q",False)
    if not search_query:
        return Response(data={"data":"no query provided"},status=status.HTTP_406_NOT_ACCEPTABLE)
    Collection=get_connection('manga')
    if not Collection['status']:
        return Response({'data':Collection['data']},status=status.HTTP_406_NOT_ACCEPTABLE)
    Collection=Collection['data']
    try:
        res=Collection.aggregate([
            {
                "$search":{
                    "index":"search_index",
                    "text":{
                        "query":search_query,
                        "path":["title"],
                        "fuzzy":{
                            "maxEdits":2,
                    }
                }
            }
            },
            {
                "$project":{
                    "_id":0,
                    'chapters':0
                    # "canonicalTitle":1,
                    # "score": { "$meta": "searchScore" }
                    }
            },
            {
            "$limit":5
            }
        ])
        
        return Response(data={"data":res},status=status.HTTP_200_OK)
    except:
        return Response(data={'data':"No response found"},status=status.HTTP_400_BAD_REQUEST)


class AccountsAPIView(APIView):
    
    authentication_classes=[BasicAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,*args,**kwargs):
        coll=get_connection('users')
        if not coll['status']:
            return Response({"data":coll['data']},status=status.HTTP_406_NOT_ACCEPTABLE)
        coll=coll['data'] 
        res=coll.find({},{"_id":0,'password':0})
        if not res:
            return Response({"data":"not able to fetch accounts"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"data":list(res)},status=status.HTTP_200_OK)


    def post(self,request,*args,**kwargs):
        payload=request.data
        collection=get_connection('users')
        if not collection['status']:
            return Response({"data":collection['data']},status=status.HTTP_400_BAD_REQUEST)
        collection=collection['data']
        validated=validate_login_creds(payload)
        if not validated['status']:
            return Response({'data':validated['data']},status=status.HTTP_406_NOT_ACCEPTABLE)
        login_data=validated['data']
        res=collection.insert_one(login_data)
        if not res.acknowledged:
            return Response({"data":"not inserted into database"},status=status.HTTP_200_OK)
        return Response({"data":"data inserted"},status=status.HTTP_201_CREATED)
        


@api_view(["post"])
@authentication_classes([TokenAuthentication,BasicAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def loginAPIView(request,*args,**kwargs):
    pass



class MangaAPIView(APIView):
    """
    
    Manga Api: 
    
    GET:
    \tquery_params={manga_id}

    """
    
    authentication_classes=[BasicAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticated]


    def get(self,request):
        manga_id=request.query_params.get("manga_id",False)
        if not manga_id:
            return Response({"data":"please provide manga_id as parameter"},status=status.HTTP_400_BAD_REQUEST)

        collection=get_connection('anime-2')
        if not collection['status']:
            return Response({"data":collection['data']},status=status.HTTP_406_NOT_ACCEPTABLE)
        collection=collection['data']
        res=collection.find_one({"manga_id":manga_id},{"_id":0})
        if not res:
            return Response({"data":"invalid manga_id"},status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"data":res},status=status.HTTP_200_OK)



@api_view(['get'])
@authentication_classes([TokenAuthentication,BasicAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_popular_manga(request):
    coll=get_connection('manga')
    if not coll['status']:
        return Response({"data":coll['data']},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    coll=coll['data']
    popular_manga=list(coll.find({},{'_id':0,'chapters':0}).sort('popularity_rank',1).limit(10))
    if not popular_manga:
        return Response({'data':"No response"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"data":popular_manga})


@api_view(['get'])
@authentication_classes([TokenAuthentication,BasicAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_manga_by_genre(request):
    params=request.query_params
    genre=params.get('genre',False)
    if not genre:
        return Response({"data":"genre not provided"},status=status.HTTP_406_NOT_ACCEPTABLE)
    coll=get_connection('manga')
    if not coll['status']:
        return Response({'data':coll['data']},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    coll=coll['data']
    try:
        response=list(coll.find({'genre':genre},{'_id':0,'chapters':0}).sort('popularity_rank').limit(10))
        print(len(response))
        if not response:
            return Response({'data':'db fetch error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'data':response},status=status.HTTP_200_OK)
    except:
        return Response({"data":"db query error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['get'])
@authentication_classes([TokenAuthentication,BasicAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_anime_by_tags(request):
    params=request.query_params
    tag=params.get('tag',False)
    print(tag)
    if not tag:
        return Response({"data":"provide Query parameter"},status=status.HTTP_406_NOT_ACCEPTABLE)
    collection=get_connection('anime')
    if not collection['status']:
        return Response({"data":collection['data']},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    coll=collection['data']
    try:
        response=list(coll.find({'tags':[tag]},{'_id':0}).limit(10))
        
        if not response:
            return Response({"data":"db fetch error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"data":response},status=status.HTTP_200_OK)
    except:
        return Response({"data":"db fetch error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['get'])
@authentication_classes([TokenAuthentication,BasicAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_read_manga(request):
    try:
        manga_id=request.query_params.get('manga_id',False)
        if not manga_id:
            return Response({'data':"no query provided"},status=status.HTTP_406_NOT_ACCEPTABLE)

        collection=get_connection('manga')
        if not collection['status']:
            return Response({'data':collection['data']},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        coll=collection['data']
        manga=list(coll.find({'manga_id':manga_id},{'_id':0}))
        return Response({"data":manga},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":{"message":e.__str__()}},status=status.HTTP_400_BAD_REQUEST)
