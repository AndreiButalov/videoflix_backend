from django.urls import path
from .views import RegistrationView, ActivateAccountView, LoginView, LogoutView, CookieTokenRefreshView, PasswordConfirmView, PasswordResetView
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = "auth"

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),

    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()), 

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),

    path('password_reset/', PasswordResetView.as_view()),
    path('password_confirm/<uidb64>/<token>/', PasswordConfirmView.as_view()),
]
