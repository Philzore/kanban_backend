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

# Create your views here.
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
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

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('firstName')
        last_name = request.data.get('lastName')
        new_user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
        #new_user.is_active = False
        new_user.first_name = first_name
        new_user.last_name = last_name
        #new_user.is_active = True
        new_user.save()
        return JsonResponse({'success': True})

class BoardView(APIView):
    """
    show the correct tasks for the active kanban channel
    """
    def get(self, request, channel_id):
        pass

class AddTaskView(APIView):
    
    def post(self, request, channel_id):
        """
        add new task to a specific channel
        """
        author = request.user
        task_name = request.data.get('name')
        task_assigned = request.data.get('assigned')
        kanban_id = get_object_or_404(Kanban, id=channel_id)
        new_task = Task.objects.create(title=task_name, author=author, assigned_to=task_assigned, assigned_channel=kanban_id)
        new_task.save()
        channel_tasks = Task.objects.filter(assigned_channel=channel_id)
        serializer = TaskSerializer(channel_tasks, many=True)
        return Response(serializer.data)

class KanbanView(APIView):
    """
    show all kanban channels
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        """
        return list of all kanban channels
        """
        kanban_channels = Kanban.objects
        serializer = KanbanSerializer(kanban_channels, many=True)
        return Response(serializer.data)
    
class AddKanbanChannelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        channel_name = request.data.get('title')
        author = request.user
        new_channel = Kanban.objects.create(title=channel_name, author=author)
        new_channel.save()
        kanban_channels = Kanban.objects
        serializer = KanbanSerializer(kanban_channels, many=True)
        return Response(serializer.data)