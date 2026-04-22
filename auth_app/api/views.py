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