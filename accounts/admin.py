from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MangaUser,EmailTemplate

admin.site.register(MangaUser)
admin.site.register(EmailTemplate)