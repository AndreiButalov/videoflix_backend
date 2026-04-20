from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user, token = serializer.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))

            domain = get_current_site(request).domain

            activation_link = f"http://{domain}/api/activate/{uid}/{token}/"

            send_mail(
                subject="Activate your account",
                message=f"Click this link to activate your account:\n{activation_link}",
                from_email="noreply@example.com",
                recipient_list=[user.email],
                fail_silently=False,
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
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except:
            return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)