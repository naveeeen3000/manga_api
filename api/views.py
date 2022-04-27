from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer
from utils import get_connection,validate_login_creds


@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def searchView(request):
    query_params=request.query_params
    search_query=query_params.get("q",False)
    if not search_query:
        return Response(data={"data":"no query provided"},status=status.HTTP_406_NOT_ACCEPTABLE)
    Collection=get_connection('anime-2')
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
                        "path":["canonicalTitle","titles","slug"],
                        "fuzzy":{
                            "maxEdits":2,
                    }
                }
            }
            },
            {
                "$project":{
                    "_id":0,
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
        print(coll)
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

