from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "base.html")


def page(request):
    title = "Assignment 3"
    content = "CINS465 Hello World"
    context = {
        "title":title,
        "body":content
    }

    return render(request, "base.html", context=context)