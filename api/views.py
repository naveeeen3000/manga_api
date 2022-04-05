from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from utils import get_connection
from rest_framework import status

class SearchAPIView(APIView):
    """
    <font color="red">/search</font>
    """


    # permission_classes=[permissions.IsAdminUser]


    def get(self,request,*args,**kwargs):
        query_params=request.query_params
        search_query=query_params.get("q",False)
        if not search_query:
            return Response(data={"data":"no query provided"},status=status.HTTP_406_NOT_ACCEPTABLE)
        Collection=get_connection('anime-2')
        # if not Collect:
        #     return Response(data={"Database error":"Connection error"},status=status.HTTP_400_BAD_REQUEST)
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
            return Response(data={'data':"No response found"},
                                                status=status.HTTP_400_BAD_REQUEST)