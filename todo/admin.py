from django.contrib import admin
from todo.models import ToDo

class ToDoAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'created_by', 'assigned_to', 'due_date', 'completed_date',)
    ordering = ('due_date',)
admin.site.register(ToDo, ToDoAdmin)
