from django.shortcuts import render
from django.http import HttpResponse

from . import models

# Create your views here.
def index(request):
    title = "Assignment 4"
    suggestions = models.SuggestionModel.objects.all()
    context = {
        "title": title,
        "suggestions":suggestions
        
    }
    return render(request, "index.html", context = context)


def page(request):
    title = "Assignment 3"
    content = "CINS465 Hello World"
    context = {
        "title":title,
        "body":content
    }

    return render(request, "base.html", context=context)