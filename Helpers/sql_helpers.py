from sqlite3 import IntegrityError
from accounts.models import MangaUser
from accounts.Manager import MangaUserManager
from utils import generate_user_token
from django.utils import timezone

class UserHelper:

    def __init__(self):
        self.manga_user=MangaUser
        self.manga_user_manager=MangaUserManager()

    def create_user(self,data,**kwargs):
        
        user=self.manga_user.objects.create(
                                first_name=data['first_name'],
                                last_name=data['last_name'],
                                email=data['email'],
                                country=data['country'],
                                created_at=timezone.now(),
                                updated=timezone.now()
                                )
        user.set_password(data['password'])
        user.save()
        return user