from rest_framework import serializers
from .models import MangaUser


class MangaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=MangaUser
        exclude = []


class AWSEmailTemplateSerializer(serializers.Serializer):
    template_name=serializers.CharField(max_length=200)
    subject_part=serializers.CharField(max_length=200)
    text_part=serializers.CharField(max_length=200)
    html_part=serializers.CharField(max_length=200)