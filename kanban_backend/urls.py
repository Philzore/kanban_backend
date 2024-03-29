"""
URL configuration for kanban_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from kanban.views import LoginView, RegisterView , BoardView, KanbanView, AddKanbanChannelView, AddTaskView, EditTaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('board/', KanbanView.as_view()),
    path('board/<int:channel_id>/', BoardView.as_view()),
    path('board/create_channel/', AddKanbanChannelView.as_view()),
    path('board/<int:channel_id>/add_task/', AddTaskView.as_view()),
    path('edit_task/<int:task_id>/', EditTaskView.as_view()),
]
