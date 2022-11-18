from django.db import models


class Manga(models.Model):
    manga_id=models.BigAutoField(primary_key=True)
    cover_image=models.URLField(max_length=50)
    title=models.CharField(max_length=50)	
    alternative_titles=models.TextField(max_length=200)
    author=models.CharField(max_length=20)
    manga_status=models.CharField(max_length=10)
    average_rating=models.CharField(max_length=6)
    popularity_rank=models.IntegerField()
    rating_rank=models.IntegerField()
    cover=models.TextField(max_length=100)
    end_date=models.DateField(max_length=10)
    release_date=models.DateField(max_length=20)
    description=models.TextField(max_length=1000)
    manga_uuid=models.CharField(max_length=20)

    class Meta:
        db_table='manga'

    def __str__(self):
        return self.title[:10]+".."

class Chapters(models.Model):
    chapter_id=models.BigAutoField(primary_key=True)
    manga_uuid=models.CharField(max_length=40)
    chapter_name=models.CharField(max_length=50)
    chapter_images=models.TextField()

    class Meta:
        db_table='chapters'

    def __str__(self):
        return self.chapter_name