from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from mailer import Mailer
from .serializers import MangaUserSerializer,AWSEmailTemplateSerializer,EmailSerializer
from .models import MangaUser,EmailTemplate
from validate_email_address import validate_email
from cryptography.fernet import Fernet
from decouple import config
import datetime
import bcrypt
import uuid





# def send_custom_template_mail(email,token,request,template_name='verify_email_template'):
#     mail_template=get_object_or_404(EmailTemplate,template_name=template_name)
#     temp_data=AWSEmailTemplateSerializer(mail_template).data
#     crypt_str=''
    
#     fernet=Fernet(config("FERNET_KEY"))
#     crypt_str=fernet.encrypt(token.encode())
#     redirect_url="{0}://{1}{2}/accounts/verify/{3}".format(request.scheme,request.get_host(),request.path,crypt_str)
#     mail=Mailer(email=config("SECRET_EMAIL"),password=config('MAIL_PASSWORD'))
#     res=mail.send(receiver=email,subject=temp_data['subject'],message=temp_data['body'].format(redirect_url))
#     # res=send_mail(
#     #     subject=temp_data['subject'],
#     #     message=temp_data['body'].format(redirect_url),
#     #     from_email=config('SECRET_EMAIL'),
#     #     recipient_list=[email],
#     #     fail_silently=False
#     # )
#     print(res)
#     return {status:True}





@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def accounts_api(request):
    base_url =  "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
    result={
        "create_user":base_url+'user/create',
        'login':base_url+'user/login',
        "user_details":base_url+'user/details',
        # "verify_user":base_url + 'user/verify',
        'create_email_template':base_url+"email/template",
        # "get_verified_addresses":base_url+'verified/mails'
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
    # queryset=MangaUser.objects.all()
    authentication_classes=[TokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self,request,*args,**kwargs):
        body=request.data
        password=body.get('password',None)
        password=password.encode('utf-8')
        hashed_password=bcrypt.hashpw(password,bcrypt.gensalt())
        hashed_password=hashed_password.decode('utf-8')
        try:
            
            ##checking for email existence
            email_is_valid=validate_email(body['email'],verify=True)
            if not email_is_valid:
                return Response({"error":{"message":"email doesn't exist"}},status=status.HTTP_400_BAD_REQUEST)
            user=MangaUser.objects.create(
                                    name=body['name'],
                                    email=body['email'],
                                    password=hashed_password,
                                    created_at=datetime.datetime.now(),
                                    updated=datetime.datetime.now())
            token=str(uuid.uuid5(uuid.NAMESPACE_DNS,body['name']+body['email']))
            user.token = token
            user.save()
            # print("user saved")
            # ##verify user

            # email = body['email']
            mail_sent=False
            # res=send_custom_template_mail(email,token,request)
            # if res.status:
            #     mail_sent=True
            


            return Response({'data':'user %s created'%body['name'],'email_is_valid':email_is_valid,'mail_sent':mail_sent},status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'error':{'message':e.__str__()}},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':{'message':e.__str__()}},status=status.HTTP_400_BAD_REQUEST)



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


class CreateEmailTemaplateView(APIView):

    serializer_class=AWSEmailTemplateSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication,TokenAuthentication,SessionAuthentication]
    
    # def get(self,request):
    #     try:
    #         templates=EmailTemplate.objects.all()
    #         # print(templates.body)
    #         data=AWSEmailTemplateSerializer(templates)
    #         return Response({"data":data},status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error':{"message":e.__str__()}},status=status.HTTP_400_BAD_REQUEST)
    

    def post(self,request,*args,**kwargs):
        error_hint={}
        try:
            serializer_data=self.serializer_class(data=request.data)
            ses=boto3.client('ses',region_name='ap-south-1')
            if serializer_data.is_valid(raise_exception=True):
                serializer_data.save()
                data=serializer_data.data
                return Response({'data':"template created"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':{"message":e.__str__()}},status=status.HTTP_400_BAD_REQUEST)
    
