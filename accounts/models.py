from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.utils.translation import gettext as _ 
from .Manager import MangaUserManager



class MangaUser(AbstractBaseUser):
    user_id=models.AutoField(unique=True,primary_key=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    # user_token=models.OneToOneField(Token,on_delete=models.CASCADE)
    country=models.CharField(max_length=20)
    dob=models.DateField()
    created_at=models.DateTimeField()
    updated=models.DateTimeField()
    last_login=models.DateField()
    is_superuser=models.BooleanField(default=False)


    email=models.EmailField(_("email address"),unique=True)

    USERNAME_FIELD: str='email'
    REQUIRED_FIELDS=['first_name','last_name','country','dob']

    objects=MangaUserManager()
    
    class Meta:
        
        db_table='manga_user'
        _fields=['is_active','is_staff','is_super_user','last_login','']
        constraints=[
            models.UniqueConstraint(fields=['email'],name='email_constraint')
        ]

    def __str__(self):
        return self.first_name
    
