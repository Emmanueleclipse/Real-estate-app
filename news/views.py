# -*- coding: utf-8 -*-
import datetime
from news.models import News
from django.http import HttpResponse, JsonResponse
from django.views.generic import View,TemplateView

#class NewsView(TemplateView):
#    template_name = "news.html"

def json_news(request):
	results = []
	news = News.objects.filter(agent=request.user).order_by('-created_date')[:1000]
	for item in news:
		results.append({ 'id': int(item.id), 'title' : item.title, 'description' : item.description, 'created_date' : item.created_date, 'icon' : item.icon, 'photo' : item.photo, 'url' : item.url })
	return JsonResponse(results, safe=False)
