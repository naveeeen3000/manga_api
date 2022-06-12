from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MangaUser

admin.site.register(MangaUser)