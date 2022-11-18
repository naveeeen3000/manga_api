from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import MangaUser

@admin.register(MangaUser)
class MangaUserAdmin(admin.ModelAdmin):
    list_display=['first_name','email','created_at','is_active','is_superuser']
    search_fields=["first_name__startswith"]
    readonly_fields=['created_at','updated']
    exclude=['password','permissions']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    pass