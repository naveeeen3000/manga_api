# from typing import Collection
import collections
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from utils import get_connection
from rest_framework import status

class SearchAPIView(APIView):
    """
    Search Api
    Usage:
        <https://127.0.0.1:8080/api/v1/search/?q={keyword}>

    """


    permission_classes=[permissions.IsAdminUser]


    def get(self,request,*args,**kwargs):
        query_params=request.query_params
        print(query_params)
        Collection=get_connection('anime-2')
        if not collections:
            return Response(data={"Database error":"Connection error"},status=status.HTTP_400_BAD_REQUEST)
        res=Collection.aggregate([{
            "$search":{
                "index":"search_index",
                "text":{
                    "query":query_params,
                "path":{
                    "wildcard":"*"
                }
                }
            },
                "fuzziness":2,
                "prefix_length":1
            
        }])
        return Response(data={
            "data":res
        },status=status.HTTP_200_OK)


