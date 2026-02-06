# Django imports
from django.urls import path

# Local Imports
from .views import RegistrationView, CustomLoginView

urlpatterns = [
    path('api/registration/', RegistrationView.as_view(), name="registration"), #View for user registration
    path('api/login/', CustomLoginView.as_view(), name="login") #View for user login
]
