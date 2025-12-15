from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from django.utils.crypto import get_random_string

from pms_api.serializer import AccountSerializer, AccountDetailsSerializer, ForgotPasswordSerializer
from core.models import Account

User = get_user_model()


@extend_schema(tags=["Account"])
class AccountListView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountDetailsSerializer

@extend_schema(tags=["Account"])
class AccountDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountDetailsSerializer

@extend_schema(tags=["Authentication"])
class AccountRegistrationView(generics.CreateAPIView):
    queryset = Account.objects.all()  # Define the queryset for the view
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        
        user = serializer.save()
        user.set_password(request.data['password'])  
        user.save() 

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'User registered successfully',
            'user_id': user.id,
            'username': user.username,
            'token': token.key
        }, status=201)  

@extend_schema(tags=["Authentication"])
class AccountLoginView(APIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny] 

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user_type': user.user_type
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        

@extend_schema(tags=["Authentication"])
class ObtainAuthTokenView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny] 


@extend_schema(tags=["Authentication"])
class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')

        if not email:
            raise ValidationError({"error": "Email is required"})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Generate a reset token (this can be further secured with an expiration time)
        reset_token = get_random_string(length=32)

        # Store the token temporarily (e.g., in the database or cache)
        user.reset_token = reset_token
        user.save()

        # Send the reset token via email (you can customize this)
        send_mail(
            'Password Reset Request',
            f'Use the following token to reset your password: {reset_token}',
            'michealnoya159@gmail.com',
            [email],
            fail_silently=False,
        )

        return Response({"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)