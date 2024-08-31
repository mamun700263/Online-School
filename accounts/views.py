from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentAccount, TeacherAccount
from .serializers import StudentAccountSerializer, TeacherAccountSerializer,LoginSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.shortcuts import redirect 
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login as auth_login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class UserLogout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return redirect(reverse_lazy('login'))


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                # Create or get the token for the user
                token, created = Token.objects.get_or_create(user=user)
                auth_login(request, user)  # Correctly log in the user
                return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
                
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class StudentAccountCreateView(APIView):
    serializer_class = StudentAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            student_account = serializer.save()  # Save the StudentAccount instance
            user = student_account.user  # Access the User instance associated with the StudentAccount

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/accounts/activate/{uid}/{token}"

            email_subject = "Confirm Your Email"
            email_body = render_to_string('email/confirmation_email.html', {'confirm_link': confirm_link, 'user': user})
            
            # Set up email
            email = EmailMultiAlternatives(
                email_subject,
                email_body,
                to=[user.email]
            )
            email.content_subtype = "html"
            email.send()

            return Response({"message": "Student created successfully. Please check your email to confirm your account."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









class TeacherAccountCreateView(APIView):
    serializer_class = TeacherAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            teacher_account = serializer.save()  # Save the TeacherAccount instance
            user = teacher_account.user  # Access the User instance associated with the TeacherAccount

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/account/activate/{uid}/{token}"

            email_subject = "Confirm Your Email"
            email_body = render_to_string('email/confirmation_email.html', {'confirm_link': confirm_link, 'user': user})
            
            # Set up email
            email = EmailMultiAlternatives(
                email_subject,
                email_body,
                to=[user.email]
            )
            email.content_subtype = "html"
            email.send()

            return Response({"message": "Teacher created successfully. Please check your email to confirm your account."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(reverse_lazy('login'))
    else:
        return redirect(reverse_lazy('login'))




