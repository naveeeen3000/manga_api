from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext as _ 
from .Manager import MangaUserManager
from django.utils import timezone

class MangaUser(AbstractBaseUser,PermissionsMixin):
    user_id=models.AutoField(unique=True,primary_key=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    country=models.CharField(max_length=20,null=True)
    dob=models.DateField(null=True)
    created_at=models.DateTimeField(default=timezone.now())
    updated=models.DateTimeField(default=timezone.now())
    last_login=models.DateField(default=timezone.now())
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    email=models.EmailField(_("email address"),unique=True)

    USERNAME_FIELD: str='email'
    REQUIRED_FIELDS=['first_name','last_name']

    objects=MangaUserManager()
    
    class Meta:
        
        db_table='manga_user'
        constraints=[
            models.UniqueConstraint(fields=['email'],name='email_constraint')
        ]

    def __str__(self):
        return self.email
    
