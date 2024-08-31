from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentAccount, TeacherAccount


# class UserSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(write_only=True)  

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'password2']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def validate(self, data):
#         password = data.get('password')
#         password2 = data.get('password2')

#         # Check if passwords match
#         if password != password2:
#             raise serializers.ValidationError({"password2": "Passwords must match."})

#         # Check if the email already exists
#         if User.objects.filter(email=data.get('email')).exists():
#             raise serializers.ValidationError({"email": "Email is already in use."})

#         return data

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user
    
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        
        if password != password2:
            raise serializers.ValidationError({'error' : "Password Doesn't Mactched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already exists"})
        account = User(username = username, email=email, first_name = first_name, last_name = last_name)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account


class StudentAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer() 

    class Meta:
        model = StudentAccount
        fields = "__all__"
        

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        student_account = StudentAccount.objects.create(user=user, **validated_data)
        return student_account

class TeacherAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer() 

    class Meta:
        model = TeacherAccount
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        teacher_account = TeacherAccount.objects.create(user=user, **validated_data)
        return teacher_account



class LoginSerializer(serializers.Serializer):
    username =  serializers.CharField(required = True)
    password =  serializers.CharField(required = True)