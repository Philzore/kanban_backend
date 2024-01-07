from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.authtoken.models import Token

from kanban.views import *
from rest_framework import status
# Create your tests here.
class KanbanTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'test_user', 'password': 'test_password'}
        self.user = User.objects.create_user(**self.user_data)
        self.login_url = '/login/'  
        self.board_url = '/board/'  

    def test_login_and_access_board(self):
        # Login
        response_login = self.client.post(self.login_url, data=self.user_data)

        # set token
        token = response_login.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='token ' + token)

        # call /board/ 
        response_board = self.client.get(self.board_url)
        self.assertEqual(response_board.status_code, status.HTTP_200_OK)

    