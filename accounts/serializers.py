from rest_framework import serializers
from .models import MangaUser


class MangaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=MangaUser
        exclude = []
