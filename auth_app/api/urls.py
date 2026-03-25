from django.urls import path
from .view import RegistrationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register')
]
