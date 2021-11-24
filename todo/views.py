import datetime
from django.shortcuts import render
from django.db.models import Q
from todo.models import ToDo
from django.http import HttpResponse, JsonResponse
from django.views.generic import View,TemplateView
from agency.utils import JsonException, pkobject, editobject, setobject

class ToDoView(TemplateView):
    template_name = "todo.html"

def json_todo(request):
	if request.method == 'POST':
		fields = [
					{ 'name': 'title', 'required': True }, 
					{ 'name': 'description', },
					{ 'name': 'start_date', },
					{ 'name': 'due_date', },
					{ 'name': 'tags', },
					{ 'name': 'for_client', 'foreignkey': True, },
					{ 'name': 'assigned_to', 'foreignkey': True, 'default': request.user.id },
				]
		newsfields = [
					{ 'name': 'title', 'required': True }, 
					{ 'name': 'description', },
					{ 'name': 'agent', 'key' : 'assigned_to', 'foreignkey' : True, 'default': request.user.id },
				]
		try:
			# Get if ID or create
			pk = pkobject(request.POST)
			item, created = ToDo.objects.filter(Q(pk=pk), Q(created_by = request.user) | Q(assigned_to = request.user)).get_or_create() if pk else (ToDo(), True)
			if editobject(request.POST, item, created):
				# Extra modifications to the object here
				item.completed_date = datetime.datetime.now() if request.POST.get('completed') else None
				if created:
					item.created_by = request.user
				# Set fields and save
				if setobject(request.POST, item, fields):
					item.save()
		except Exception as e:
			return JsonException(e)

	results = []
	tasks = ToDo.objects.filter(Q(created_by=request.user) | Q(assigned_to=request.user)).order_by('due_date')[:1000]
	for task in tasks:
		results.append({ 'id': int(task.id), 'mine': bool(task.assigned_to==request.user), 'title' : task.title, 'description' : task.description, 'tags' : task.tags, 'created_date' : task.created_date, 'due_date' : task.due_date, 'completed_date' : task.completed_date, 'created_by' : str(task.created_by), 'assigned_to' : task.assigned_to_id, 'for_client' : task.for_client_id, 'client' : (task.for_client.name if task.for_client_id else None), 'for_agent' : task.for_agent_id })
	return JsonResponse(results, safe=False)
