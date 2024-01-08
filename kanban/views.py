from django.shortcuts import render
from .models import Kanban, Task
from .serializer import KanbanSerializer, TaskSerializer
from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json


# Create your views here.
class LoginView(ObtainAuthToken, APIView):

    def options(self, request, channel_id):
        # Implementing OPTIONS method for Preflight requests
        response = Response()
        response["Access-Control-Allow-Origin"] = "https://philipp-moessl.developerakademie.net/"  # Set the appropriate origin
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    """
    login user
    """
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name' : user.first_name
            })
        except Exception as e:
            return JsonResponse({'success': False})

class RegisterView(APIView):
    """
    register new user
    """
    def post(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('firstName')
            last_name = request.data.get('lastName')
            new_user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False})


class BoardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    update tasks if the category has changed
    """
    def post(self, request, channel_id):
        try:
            data = json.loads(request.body)
            for category, tasks in data.items():
                for task_data in tasks:
                    task_id = task_data.get('id')
                    task = Task.objects.get(id=task_id)
                    task.category = task_data.get('category')
                    task.save()

            return JsonResponse({'message' : 'Arrays updated successfull'})
        except Exception as e:
            return JsonResponse({'error' : f'Something wen´t wrong: {str(e)}'})
        
    """
    show the correct tasks for the active kanban channel
    """
    def get(self, request, channel_id):
        taks = Task.objects.filter(assigned_channel=channel_id)
        serializer = TaskSerializer(taks, many= True)
        return Response(serializer.data)
    
    """
    delete a single kanban channel
    """
    def delete(self, request, channel_id):
        kanban = get_object_or_404(Kanban, id=channel_id)
        kanban.delete()

        kanban_channels = Kanban.objects
        serializer = KanbanSerializer(kanban_channels, many=True)
        return Response(serializer.data)
        
    def options(self, request, channel_id):
        # Implementing OPTIONS method for Preflight requests
        response = Response()
        response["Access-Control-Allow-Origin"] = "https://philipp-moessl.developerakademie.net"  # Set the appropriate origin
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

class AddTaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    add new task to a specific channel
    """
    def post(self, request, channel_id): 
        author = request.user
        task_name = request.data.get('name')
        task_assigned = request.data.get('assigned')
        kanban_id = get_object_or_404(Kanban, id=channel_id)
        new_task = Task.objects.create(title=task_name, author=author, assigned_to=task_assigned, assigned_channel=kanban_id, category='to_do')
        new_task.save()
        channel_tasks = Task.objects.filter(assigned_channel=channel_id)
        serializer = TaskSerializer(channel_tasks, many=True)
        return Response(serializer.data)

class KanbanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    show the available channels, when current active user is the creator
    """
    def get(self, request, format=None):
        kanban_channels = Kanban.objects.filter(author=request.user)
        serializer = KanbanSerializer(kanban_channels, many=True)
        return Response(serializer.data)
    
class AddKanbanChannelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    add a new kanban channel
    """
    def post(self, request):
        channel_name = request.data.get('title')
        author = request.user
        new_channel = Kanban.objects.create(title=channel_name, author=author)
        new_channel.save()
        kanban_channels = Kanban.objects
        serializer = KanbanSerializer(kanban_channels, many=True)
        return Response(serializer.data)