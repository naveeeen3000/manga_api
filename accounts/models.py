from django.db import models
from django.contrib.auth.models import User


class MangaUser(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    token=models.CharField(max_length=255, db_index=True,unique=True)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField()
    updated=models.DateTimeField()
    
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['email'],name='email_constraint')
        ]

    def __str__(self):
        return self.name
    