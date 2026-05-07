from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.conf import settings
from rest_framework.response import Response
from .serializers import RegistrationSerializer, PasswordConfirmSerializer, PasswordResetSerializer
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.template.loader import render_to_string
from django.conf import settings




class RegistrationView(APIView):
    """Handle user registration with email activation.
    
    This view allows new users to register by providing email and password.
    An activation email with a unique token is sent to the user after successful registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user and send activation email.
        
        Args:
            request: HTTP request containing email and password in the body.
            
        Returns:
            Response: Created user data (id, email) with activation token on success (201).
                     Validation errors if data is invalid (400).
                     
        Raises:
            ValueError: If email sending fails.
        """
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user, token = serializer.save()

            token = str(uuid.uuid4())
            cache.set(f"activation_{user.id}", token, timeout=3600)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            frontend_url = getattr(settings, "FRONTEND_URL", "").rstrip("/")
            user_name = user.get_full_name() or user.username

            if frontend_url:
                activation_link = (
                    f"{frontend_url}/pages/auth/activate.html"
                    f"?uid={uid}&token={token}"
                )
            else:
                domain = get_current_site(request).domain
                activation_link = (
                    f"http://{domain}/pages/auth/activate.html"
                    f"?uid={uid}&token={token}"
                )

            html_message = render_to_string(
                "email_activation.html",
                {
                    "activation_link": activation_link,
                    "user_name": user_name
                }
            )


            email = EmailMultiAlternatives(
                subject="Activate your account",
                body=f"Click this link:\n{activation_link}",
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )

            email.attach_alternative(html_message, "text/html")
            email.send() 

            return Response({
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "token": token
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
import uuid



class RegistrationView(APIView):
    """Handle user registration with email activation.
    
    This view allows new users to register by providing email and password.
    An activation email with a unique token is sent to the user after successful registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user and send activation email.
        
        Args:
            request: HTTP request containing email and password in the body.
            
        Returns:
            Response: Created user data (id, email) with activation token on success (201).
                     Validation errors if data is invalid (400).
                     
        Raises:
            ValueError: If email sending fails.
        """
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user, token = serializer.save()

            token = str(uuid.uuid4())
            cache.set(f"activation_{user.id}", token, timeout=3600)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            frontend_url = getattr(settings, "FRONTEND_URL", "").rstrip("/")
            user_name = user.get_full_name() or user.username

            if frontend_url:
                activation_link = (
                    f"{frontend_url}/pages/auth/activate.html"
                    f"?uid={uid}&token={token}"
                )
            else:
                domain = get_current_site(request).domain
                activation_link = (
                    f"http://{domain}/pages/auth/activate.html"
                    f"?uid={uid}&token={token}"
                )

            html_message = render_to_string(
                "email_activation.html",
                {
                    "activation_link": activation_link,
                    "user_name": user_name
                }
            )


            email = EmailMultiAlternatives(
                subject="Activate your account",
                body=f"Click this link:\n{activation_link}",
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )

            email.attach_alternative(html_message, "text/html")
            email.send() 

            return Response({
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "token": token
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class ActivateAccountView(APIView):
    """Activate user account using token from activation email."""
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        """Activate a user account with valid token.
        
        Args:
            request: HTTP request.
            uidb64 (str): Base64 encoded user ID.
            token (str): Unique activation token from cache.
            
        Returns:
            Response: Success message if token is valid (200).
                     Error message if token is invalid or expired (400).
        """
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        saved_token = cache.get(f"activation_{user.id}")
        
        if token == saved_token:
            user.is_active = True
            user.save()

            return Response(
                {"message": "Account successfully activated."},
                status=200
            )

        return Response({"error": "Invalid token"}, status=400)
    
    

class LoginView(APIView):
    """Handle user login and JWT token generation.
    
    Authenticates user credentials and returns JWT tokens in HTTP-only cookies.
    """
    permission_classes = []

    def post(self, request):
        """Authenticate user and generate JWT tokens.
        
        Args:
            request: HTTP request containing email and password.
            
        Returns:
            Response: User data with access_token and refresh_token cookies on success (200).
                     Unauthorized error if credentials are invalid (401).
                     Forbidden error if account is not activated (403).
                     
        Note:
            Tokens are set as HTTP-only, secure cookies with appropriate expiration times.
        """
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            return Response(
                {"detail": "Bitte überprüfe deine Eingaben und versuche es erneut."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"detail": "Bitte überprüfe deine Eingaben und versuche es erneut."},
                status=status.HTTP_401_UNAUTHORIZED
            )

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
    


class LogoutView(APIView):
    """Handle user logout and token blacklisting.
    
    Blacklists the refresh token and clears authentication cookies.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Logout user by blacklisting refresh token.
        
        Args:
            request: HTTP request with refresh_token in cookies.
            
        Returns:
            Response: Success message and cleared cookies (200).
                     Bad request error if refresh token is missing or invalid (400).
        """
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Bitte überprüfe deine Eingaben und versuche es erneut."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except TokenError:
            return Response(
                {"detail": "Bitte überprüfe deine Eingaben und versuche es erneut."},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = Response(
            {
                "detail": "Logout erfolgreich! Alle Tokens wurden gelöscht."
            },
            status=status.HTTP_200_OK
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
    

class CookieTokenRefreshView(APIView):
    """Refresh access token using refresh token from cookies.
    
    Generates a new access token without requiring re-authentication.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Generate a new access token from refresh token.
        
        Args:
            request: HTTP request with refresh_token in cookies.
            
        Returns:
            Response: New access token in cookie and response body (200).
                     Bad request if refresh token is missing (400).
                     Unauthorized if refresh token is invalid (401).
        """
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh-Token fehlt."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

        except TokenError:
            return Response(
                {"detail": "Ungültiger Refresh-Token."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response(
            {
                "detail": "Token refreshed",
                "access": access_token
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=3600
        )

        return response
    


class PasswordResetView(APIView):
    """Initiate password reset process.
    
    Sends a password reset email with a unique token to the user's email address.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Send password reset email to user.
        
        Args:
            request: HTTP request containing email address.
            
        Returns:
            Response: Confirmation message (200) regardless of email existence (security).
                     Validation errors if email format is invalid (400).
                     
        Note:
            Returns same message whether email exists or not for security.
        """
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Falls die E-Mail existiert, erhältst du eine Nachricht zum Zurücksetzen des Passworts."},
                    status=status.HTTP_200_OK
                )

            token = str(uuid.uuid4())
            cache.set(f"password_reset_{user.id}", token, timeout=3600)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            frontend_url = getattr(settings, "FRONTEND_URL", "").rstrip("/")

            if frontend_url:
                reset_link = (
                    f"{frontend_url}/pages/auth/password-reset.html"
                    f"?uid={uid}&token={token}"
                )
            else:
                domain = get_current_site(request).domain
                reset_link = (
                    f"http://{domain}/pages/auth/password-reset.html"
                    f"?uid={uid}&token={token}"
                )

            html_message = render_to_string(
                "password_reset.html",
                {
                    "reset_link": reset_link,
                }
            )

            email = EmailMultiAlternatives(
                subject="Passwort zurücksetzen",
                body=f"Klicke auf diesen Link um dein Passwort zurückzusetzen:\n{reset_link}",
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )

            email.attach_alternative(html_message, "text/html")
            email.send()

            return Response(
                {"detail": "Falls die E-Mail existiert, erhältst du eine Nachricht zum Zurücksetzen des Passworts."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class PasswordConfirmView(APIView):
    """Reset user password with valid token.
    
    Validates the password reset token and updates the user's password.
    """
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        """Reset user password after token validation.
        
        Args:
            request: HTTP request containing new_password and confirm_password.
            uidb64 (str): Base64 encoded user ID.
            token (str): Password reset token from email.
            
        Returns:
            Response: Success message if password is updated (200).
                     Bad request if token is invalid/expired or data is invalid (400).
                     
        Note:
            Token must match the one stored in cache and be within 1 hour of creation.
        """
        serializer = PasswordConfirmSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response(
                {"detail": "Ungültiger oder abgelaufener Link."},
                status=400
            )

        saved_token = cache.get(f"password_reset_{user.id}")

        if token != saved_token:
            return Response(
                {"detail": "Ungültiger oder abgelaufener Link."},
                status=400
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        cache.delete(f"password_reset_{user.id}")

        return Response(
            {"detail": "Dein Passwort wurde erfolgreich zurückgesetzt."},
            status=status.HTTP_200_OK
        )