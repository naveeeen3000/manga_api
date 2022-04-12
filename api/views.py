from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer
from utils import get_connection



@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def searchView(request):
    query_params=request.query_params
    search_query=query_params.get("q",False)
    if not search_query:
        return Response(data={"data":"no query provided"},status=status.HTTP_406_NOT_ACCEPTABLE)
    Collection=get_connection('anime-2')
    try:
        res=Collection.aggregate([
            {
                "$search":{
                    "index":"search_index",
                    "text":{
                        "query":search_query,
                        "path":"canonicalTitle",
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
    
    serializer_class=LoginSerializer
    authentication_classes=[BasicAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,*args,**kwargs):
        coll=get_connection('users')
        # out={}
        res=coll.find({},{"_id":0,'password':0})
        if not res:
            return Response({"data":"not able to fetch accounts"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"data":list(res)},status=status.HTTP_200_OK)


    def post(self,request,*args,**kwargs):
        payload={
                "name":request.POST.get('name'),
                "email":request.POST.get('email'),
                "password":request.POST.get('password'),
                "created_at": request.POST.get("created_at")
            }
        # payload=dict(payload)
        # payload.pop('csrfmiddlewaretoken')
        # print(payload)
        serializer=self.serializer_class(data=payload)
        if serializer.is_valid(raise_exception=True):
            # print(serializer.data)
            serializer.save()
            return Response({"data":"user created"},status=status.HTTP_201_CREATED)
        return Response({"data":"invalid data"},status=status.HTTP_400_BAD_REQUEST)
        # serializer=this.serializer_class()



@api_view(["post"])
@authentication_classes([TokenAuthentication,BasicAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def loginAPIView(request,*args,**kwargs):
    pass