from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    title = "My Title"
    content = "Content"
    context = {
        "title":title,
        "body":content
    }

    return render(request, "base.html", context=context)