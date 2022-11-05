from django.db import models
from django.contrib.auth.models import User


class MangaUser(models.Model):
    user_id=models.AutoField(unique=True,primary_key=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    country=models.CharField(max_length=20)
    dod=models.DateField()
    created_at=models.DateTimeField()
    updated=models.DateTimeField()
    
    class Meta:
        db_table='manga_user'
        constraints=[
            models.UniqueConstraint(fields=['email'],name='email_constraint')
        ]

    def __str__(self):
        return self.first_name
    