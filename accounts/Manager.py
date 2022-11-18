from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Permission
class MangaUserManager(BaseUserManager):
    
    def __init__(self) -> None:
        super(MangaUserManager,self).__init__()

    def create_user(self,email,password, **extra_fields):
        if not email:
            raise ValueError(_("User must have an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        token=Token.objects.get_or_create(user=user)[0]
        user.user_token=token
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('SuperUser must have is_staff = True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email,password,**extra_fields)
