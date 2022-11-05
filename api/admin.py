from django.contrib import admin
from .models import Manga,Chapters


@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    readonly_fields=('manga_id','manga_uuid','release_date')
    list_display=["title","author","manga_status","end_date"]
    search_fields=['title__startswith','manga_uuid__startswith']

@admin.register(Chapters)
class ChaptersAdmin(admin.ModelAdmin):
    list_display=['chapter_id','chapter_name']
    search_fields=['chapter_name']
    readonly_fields=('manga_uuid','chapter_id')

