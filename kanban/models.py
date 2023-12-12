from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Kanban(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

   

class Task(models.Model):
    title = models.CharField(max_length=20)
    author = author = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=20)

    