from rest_framework import serializers
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email']
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self,validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            password = validated_data['password'],
            email = validated_data['email']
        )
        return user
    
class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):

        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username,password=password)
            
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is inactive")
            else:
                raise serializers.ValidationError("Invalid Username or Password")
            
        else:
            raise serializers.ValidationError("Must include both Username and Password")
        
        data['user'] = user
        return data
    
