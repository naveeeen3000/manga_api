from tokenize import Token
from django.contrib import admin
from .models import UserModel
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields=['user']

admin.site.register(UserModel)