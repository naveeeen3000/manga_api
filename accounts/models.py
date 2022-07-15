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
    

class EmailTemplate(models.Model):
    template_name=models.CharField(max_length=200,unique=True)
    from_address=models.EmailField()
    subject=models.CharField(max_length=50)
    body=models.TextField()
    surl=models.URLField()
    furl=models.URLField()


    def __str__(self):
        return self.template_name

