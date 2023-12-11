from django.shortcuts import render
from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class LoginView(ObtainAuthToken):
    pass

class RegisterView():
    pass

class BoardView():
    pass