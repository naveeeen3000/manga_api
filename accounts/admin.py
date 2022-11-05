from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MangaUser

@admin.register(MangaUser)
class MangaUserAdmin(admin.ModelAdmin):
    list_display=['first_name','email','created_at']
    search_fields=["first_name__startswith"]
    readonly_fields=['created_at','updated']