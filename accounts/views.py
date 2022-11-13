from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework.views import APIView
from Helpers.sql_helpers import UserHelper
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .serializers import MangaUserSerializer
import bcrypt


class CreateUserView(APIView):
    """View to create a user"""

    authentication_classes=[TokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        body=request.data
        try:
            user_helper=UserHelper()
            user=user_helper.create_user(body)
            if user:
                return Response({},status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"User not creaeted"},status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"error":"user already exists"},status=status.HTTP_403_FORBIDDEN)






@api_view(['post'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def login_APIView(request):
    payload=request.data
    email=payload.get('email')
    password=payload.get('password')
    query=get_object_or_404(MangaUser,email=email)
    serializer_data=MangaUserSerializer(query)
    data=serializer_data.data
    enc_pass=data['password'].encode('utf-8')
    password=password.encode('utf-8')
    if bcrypt.checkpw(password,enc_pass):
        data.pop('password')
        return Response({'data':data},status=status.HTTP_200_OK)
    else:
        return Response({'error':{'message':'Invalid password'}},status=status.HTTP_400_BAD_REQUEST)



@api_view(['post'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def getUserDetailsAPIView(request):
    payload=request.data
    token=payload.get('token', None)
    if token is None:
        return Response({'error':{'message':'token not provided'}},status=status.HTTP_400_BAD_REQUEST)
    user=get_object_or_404(MangaUser,token=token)
    serializer_data=MangaUserSerializer(user)
    user_data=serializer_data.data
    user_data.pop('token')
    user_data.pop('id')
    user_data.pop('password')
    
    return Response({'user':user_data},status=status.HTTP_200_OK)

