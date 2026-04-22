from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
import uuid
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user, token = serializer.save()

            token = str(uuid.uuid4())
            cache.set(f"activation_{user.id}", token, timeout=3600)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain

            activation_link = f"http://{domain}/api/activate/{uid}/{token}/"

            send_mail(
                subject="Activate your account",
                message=f"Click this link to activate your account:\n{activation_link}",
                from_email="kokos3101@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
                html_message=f"""
                    <p>Click this link to activate your account:</p>
                    <a href="{activation_link}">{activation_link}</a>
                """
            )

            return Response({
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "token": token
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        saved_token = cache.get(f"activation_{user.id}")
        
        if token == saved_token:
            user.is_active = True
            user.save()

            return Response({"message": "Account activated"}, status=200)

        return Response({"error": "Invalid token"}, status=400)
    
    

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"detail": "Account not activated"},
                status=status.HTTP_403_FORBIDDEN
            )

        # JWT erzeugen
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            "detail": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username
            }
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 60 
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 60 * 24 * 7 
        )

        return response