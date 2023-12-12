from django.contrib import admin
from .models import Task, Kanban

# Register your models here.
class KanbanAdmin(admin.ModelAdmin):
    list_display = ('id','title','author',)
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','author', 'assigned_to')

admin.site.register(Kanban, KanbanAdmin)
admin.site.register(Task, TaskAdmin)