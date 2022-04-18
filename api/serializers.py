from rest_framework import serializers
from utils import get_connection
import bcrypt



class LoginSerializer(serializers.Serializer):
	name=serializers.CharField(max_length=100)
	email=serializers.EmailField()
	password=serializers.CharField(max_length=20)
	created_at=serializers.CharField(max_length=100)


	def validate(self,data):
		"""
		check if user is already present in DB

		"""

		coll=get_connection('users')
		res=coll.find_one({"mail":data['email']})
		if res:
			
			raise serializers.ValidationError("Email already exists...")
		return data


	def save(self):
		"""
		
		Storing account info in DB

		"""

		data=dict(self.validated_data)
		data['created_at']=str(data['created_at'])
		salt=bcrypt.gensalt()
		hashed_password=bcrypt.hashpw(str(data['password']).encode("utf-8"),salt)
		data['password']=hashed_password
		coll=get_connection('users')
		res=coll.insert_one(data)
		if not res.acknowledged:
			raise serializers.ValidationError("Server Error.....")
		

		







