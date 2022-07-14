from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework.views import APIView
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .serializers import MangaUserSerializer
from .models import MangaUser
import datetime
import bcrypt
import boto3
import uuid




@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def accounts_api(request):
    base_url =  "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
    result={
        "create_user":base_url+'user/create',
        'login':base_url+'user/login',
        "user_details":base_url+'user/details',
        "verify_user":base_url + 'user/verify'
    }
    return Response(result,status=status.HTTP_200_OK)

@api_view(['POST'])
def create_user_view(request):
    payload=request.data
    return Response({"data":payload},status=status.HTTP_201_CREATED)


class AccountsAPIView(APIView):

    """

    * POST user

    """
    queryset=MangaUser.objects.all()
    authentication_classes=[TokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self,request,*args,**kwargs):
        body=request.data
        password=body.get('password',None)
        password=password.encode('utf-8')
        hashed_password=bcrypt.hashpw(password,bcrypt.gensalt())
        hashed_password=hashed_password.decode('utf-8')
        print(type(hashed_password))
        try:
            user=MangaUser.objects.create(
                                    name=body['name'],
                                    email=body['email'],
                                    password=hashed_password,
                                    created_at=datetime.datetime.now(),
                                    updated=datetime.datetime.now())
            token=str(uuid.uuid5(uuid.NAMESPACE_DNS,body['name']))
            user.token = token

            user.save()
            return Response({'data':'user %s created'%body['name']},status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error':{'message':'user already exists'}},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':{'message':'User not created'}},status=status.HTTP_400_BAD_REQUEST)



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


@api_view(["post"])
@authentication_classes([BasicAuthentication,TokenAuthentication])
def create_email_template(request):
    pass

@api_view(['post'])
@authentication_classes([BasicAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def verifyUser(request):
    payload=request.data
    email=payload.get('email',False)
    if not email:
        return Response({"data":"email not provided "},status=status.HTTP_400_BAD_REQUEST)
    try:
        ses=boto3.client('ses',region_name='ap-south-1')
        response=ses.verify_email_identity(
            EmailAddress=email
        )
        return Response({"data":response},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":{"message":e.__str__()}},status=status.HTTP_400_BAD_REQUEST)