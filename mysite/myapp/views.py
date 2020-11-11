from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, timezone


from . import models
from . import forms

def logout_view(request):
    logout(request)
    return redirect("/login/")


# Create your views here.
@login_required
def index(request):
    title = "Braggin Board"
    if request.method == "POST":
           if request.user.is_authenticated:
            suggestion_form = forms.SuggestionForm(request.POST)
            if suggestion_form.is_valid():
                suggestion_form.save(request)
                suggestion_form = forms.SuggestionForm()

        
    else:
        suggestion_form = forms.SuggestionForm()
    suggestions = models.SuggestionModel.objects.all()
    suggestion_objects = models.SuggestionModel.objects.all()
    suggestion_list = []
    for sugg in suggestion_objects: 
        comment_objects = models.CommentModel.objects.filter(suggestion=sugg)
        temp_sugg = {}
        temp_sugg["suggestion"] = sugg.suggestion
        temp_sugg["id"] = sugg.id
        temp_sugg["author"] = sugg.author.username
        temp_sugg["comments"] = comment_objects
        suggestion_list+=[temp_sugg]


    #comments = models.CommentModel.objects.all()
    context = {
        "title": title,
        "suggestions":suggestion_list,
        "form":suggestion_form,
       #"comments":comments,
    }
    return render(request, "index.html", context=context)


@login_required
def page(request):
    title = "Assignment 3"
    content = "CINS465 Hello World"
    context = {
        "title":title,
        "body":content
    }
    return render(request, "base.html", context=context)


def add_suggestion(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect("/")
    else:
        form = forms.SuggestionForm()
    context = {
        "title":"Suggestion",
        "form":form
    }
    return render(request, "suggestion.html", context=context)

def comment(request, sugg_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            form.save(request, sugg_id)
            return redirect("/")
    else:
        form = forms.CommentForm()
    context = {
        "title":"Comment",
        "sugg_id":sugg_id,
        "form":form
    }
    return render(request, "comment.html", context=context)

def get_suggestions(request):
    suggestion_objects = models.SuggestionModel.objects.all()
    suggestion_list = {}
    suggestion_list["suggestions"]=[]
    for sugg in suggestion_objects:
        comment_objects = models.CommentModel.objects.filter(suggestion=sugg)
        temp_sugg = {}
        temp_sugg["suggestion"]=sugg.suggestion
        temp_sugg["author"]=sugg.author.username
        temp_sugg["id"]=sugg.id
        temp_sugg["date"]=sugg.published_on.strftime("%Y-%m-%d %H:%M:%S")
        temp_sugg["comments"]=[]
        for comm in comment_objects:
            temp_comm={}
            temp_comm["comment"]=comm.comment
            temp_comm["id"]=comm.id
            temp_comm["author"]=comm.author.username
            time_diff = datetime.now(timezone.utc) - comm.published_on
            time_diff_s = time_diff.total_seconds()
            if time_diff_s < 60:
                temp_comm["date"] = "published " + str(int(time_diff_s)) + " seconds ago"
            else:
                time_diff_m = divmod(time_diff_s, 60)[0]
                if time_diff_m < 60:
                    temp_comm["date"] = "published " + str(int(time_diff_m)) + " minutes ago"
                else:
                    time_diff_h = divmod(time_diff_m, 60)[0]
                    if time_diff_h < 24:
                        temp_comm["date"] = "published " + str(int(time_diff_h)) + " hour ago"
                    else:
                        temp_comm["date"]  = "published on " + comm.published_on.strftime("%Y-%m-%d %H:%M:%S")
            # published {{ comm.date }} minutes ago
            # temp_comm["date"]=comm.published_on
            temp_sugg["comments"]+=[temp_comm]
        suggestion_list["suggestions"]+=[temp_sugg]
    return JsonResponse(suggestion_list)
        



def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)