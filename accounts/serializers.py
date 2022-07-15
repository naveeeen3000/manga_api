from rest_framework import serializers
from .models import MangaUser,EmailTemplate


class MangaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=MangaUser
        exclude = []


class AWSEmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmailTemplate
        exclude=[]
        

class EmailSerializer(serializers.Serializer):
    email=serializers.EmailField()