from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentAccount, TeacherAccount
from .serializers import StudentAccountSerializer, TeacherAccountSerializer, LoginSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



def send_email(subject, template_name, context, recipient_list):
    """
    Let's use it where ever it needs 
    don't wast time and mind
    """
    # Render the email body using the provided template and context
    email_body = render_to_string(template_name, context)

    # Set up email
    email = EmailMultiAlternatives(
        subject=subject,
        body=email_body,
        to=recipient_list
    )
    email.content_subtype = "html"  # eta na dile code jabe
    email.send()


web_site = 'https://online-school-1wkk.onrender.com'

class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Simply delete the token to force a login
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
                auth_login(request, user)  
                return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
                
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class AccountCreateView(APIView):
    serializer_class = None  # I will set this int the classes

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()  # Save the account instance
            user = account.user  # Access the User instance associated with the account 

            # Generate email confirmation token and link
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"{web_site}/accounts/activate/{uid}/{token}"

            # Prepare email context
            context = {'confirm_link': confirm_link, 'user': user}

            # Use the utility function to send the email
            send_email(
                subject="Confirm Your Email",
                template_name='email/confirmation_email.html',
                context=context,
                recipient_list=[user.email]
            )

            return Response(
                {"message": "Account created successfully. Please check your email to confirm your account."},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentAccountCreateView(AccountCreateView):
    serializer_class = StudentAccountSerializer


class TeacherAccountCreateView(AccountCreateView):
    serializer_class = TeacherAccountSerializer


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(reverse_lazy('login'))
    else:
        return redirect(reverse_lazy('login'))
