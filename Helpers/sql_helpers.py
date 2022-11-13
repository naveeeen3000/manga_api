from sqlite3 import IntegrityError
from accounts.models import MangaUser
from utils import generate_user_token
import bcrypt
import datetime

class UserHelper:

    def __init__(self):
        self.manga_user=MangaUser

    def create_user(self,data,**kwargs):
        password=data.get('password')
        password=password.encode('utf-8')
        hashed_password=bcrypt.hashpw(password,bcrypt.gensalt())
        hashed_password=hashed_password.decode('utf-8')
        user=self.manga_user.objects.create(
                                first_name=data['first_name'],
                                last_name=data['last_name'],
                                email=data['email'],
                                password=hashed_password,
                                country=data['country'],
                                created_at=datetime.datetime.now(),
                                updated=datetime.datetime.now())
        token=generate_user_token()
        user.token = token
        user.save()
        return user