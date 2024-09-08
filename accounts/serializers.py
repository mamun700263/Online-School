from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentAccount, TeacherAccount


    

class BaseUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password after validation
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.is_active = False 
        user.save()
        return user
class StudentAccountSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer() 

    class Meta:
        model = StudentAccount
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = BaseUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        student_account = StudentAccount.objects.create(user=user, **validated_data)
        return student_account


class TeacherAccountSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()  

    class Meta:
        model = TeacherAccount
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = BaseUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        teacher_account = TeacherAccount.objects.create(user=user, **validated_data)
        return teacher_account


class LoginSerializer(serializers.Serializer):
    username =  serializers.CharField(required = True)
    password =  serializers.CharField(required = True)