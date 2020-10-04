from django.shortcuts import render
from django.http import HttpResponse

from . import models
from . import forms

# Create your views here.
def index(request):
    title = "Assignment 4"
    if request.method == "POST":
        suggestion_form = forms.SuggestionForm(request.POST)
        if suggestion_form.is_valid():
            suggestion_form.save()
            suggestion_form = forms.SuggestionForm()
    else:
        suggestion_form = forms.SuggestionForm()
    suggestions = models.SuggestionModel.objects.all()
    context = {
        "title": title,
        "suggestions":suggestions,
        "form":suggestion_form,
    }
    return render(request, "index.html", context=context)


def page(request):
    title = "Assignment 3"
    content = "CINS465 Hello World"
    context = {
        "title":title,
        "body":content
    }

    return render(request, "base.html", context=context)