from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentAccount, TeacherAccount,Account
from .serializers import StudentAccountSerializer, TeacherAccountSerializer, LoginSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import generics
from skill.models import CourseModel
from skill.serializers import CourseSerializer




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

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get(self, request):
        user = request.user
        account = Account.objects.get(user=user)
        u_id = getattr(account, 'unique_id', '')
        
        # Check if the user is a student or teacher based on the prefix of the unique_id
        if u_id.startswith("ST"):  # For student
            courses = CourseModel.objects.filter(students=account)  # Enrolled courses for student
        elif u_id.startswith("TE"):  # For teacher
            courses = CourseModel.objects.filter(taken_by=account)  # Courses taught by teache

        # Serialize the course data
        serializer = CourseSerializer(courses, many=True)
        print(courses)
        data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'mobile': getattr(account, 'mobile', ''),
            'date_of_birth': getattr(account, 'date_of_birth', ''),
            'unique_id': getattr(account, 'unique_id', ''),
            'profile_picture': getattr(account, 'profile_picture', ''),
            'courses': serializer.data,  # Use serialized data
        }
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        try:
            account = StudentAccount.objects.get(user=user)
        except StudentAccount.DoesNotExist:
            try:
                account = TeacherAccount.objects.get(user=user)
            except TeacherAccount.DoesNotExist:
                return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()

        account.mobile = data.get('mobile', account.mobile)
        account.date_of_birth = data.get('date_of_birth', account.date_of_birth)
        account.profile_picture = data.get('profile_picture', account.profile_picture)
        account.save()

        return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)




web_site = 'https://online-school-1wkk.onrender.com'
# web_site = 'http://127.0.0.1:8000'

class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Simply delete the token to force a login
        request.user.auth_token.delete()
        return redirect(reverse_lazy('login'))


class UserLoginApiView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny] 
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
    authentication_classes = [] 
    permission_classes = [AllowAny] 

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



login_page_front_end = "https://mamun700263.github.io/Ghor-School/login.html"

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(login_page_front_end)
    else:
        return HttpResponseRedirect(login_page_front_end)





# # List view for StudentAccount
class StudentListView(generics.ListAPIView):
    authentication_classes = [] 
    permission_classes = [AllowAny] 
    queryset = StudentAccount.objects.all()
    serializer_class = StudentAccountSerializer

# # List view for TeacherAccount
class TeacherListView(generics.ListAPIView):
    authentication_classes = [] 
    permission_classes = [AllowAny] 
    queryset = TeacherAccount.objects.all()
    serializer_class = TeacherAccountSerializer
