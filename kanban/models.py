from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Kanban(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.id} {self.title}"
   

class Task(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=[
        ('to_do', 'to_do'),
        ('in_progress', 'in_progress'),
        ('testing', 'testing'),
        ('done', 'done'),
    ])
    assigned_channel = models.ForeignKey(Kanban, on_delete=models.CASCADE)
    