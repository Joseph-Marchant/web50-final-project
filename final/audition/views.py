from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Audition, User, Script


# Index request
@login_required(login_url="login")
def index(request):

    # Get the user and their auditions
    user_id = request.user
    user = User.objects.get(pk=user_id.id)
    auditions = Audition.objects.filter(user=user)

    # Render the index page
    return render(request, "audition/index.html", {
        "user": user,
        "auditions": auditions
    })


# Login
def login(request):

    # If the request is GET then generate the page
    if request.method == "GET":
        return render(request, "audition/login.html")

    # Otherwise process the request
    else:
        
        # Get the info from the form
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if they are authenticated
        if user is not None:

            # If they are then log them in
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        # Otherwise return them to the login page
        else:
            return render(request, "audition/login.html", {
                "message": "Invalid username or password."
            })


# Register
def register(request):
    
    # If method is GET then generate page
    if request.method == "GET":
        return render(request, "audition/register.html")

    # Otherwise process the form
    else:

        # Get info from the form
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        email = request.POST["email"]

        # Check the password and confirmation match
        if password != confirmation:
            return render(request, "audition/register.html", {
                "message": "Passwords must match"
            })
        
        # Try to create the user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        # If fail then return message to user
        except:
            return render(request, "audition/register.html", {
                "message": "Username already taken"
            })

        # Log the user in and send them to the index
        login(request, user)
        return HttpResponseRedirect("index")


# Logout
@login_required(login_url="login")
def logout(request):

    # Log the user out and return them to the index
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# New audition form
class NewAudition(forms.Form):
    title = forms.CharField(label="Title*")
    role = forms.CharField(label="Role*")
    script = forms.CharField(label="Script", required=False)
    scene = forms.CharField(label="Scene", required=False)
    date = forms.CharField(label="Audition Date*")


# New audition
def new_audtion(request):

    # If request is GET the generate the web page
    if request.method == "GET":
        return render(request, "audition/new_audition.html", {
            "form": NewAudition()
        })
    
    # Otherwise process the form
    else:

        # Check the form is valid
        form = NewAudition(request.POST)
        if form.is_valid():

            # Process the forms information
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            audition = Audition.objects.create(title=form.cleaned_data["title"], role=form.cleaned_data["role"], user=user)
            audition.save()

            # Seperate the scripts
            if form.cleaned_data["script"] is not None:
                scripts = seperate_scripts(form.cleaned_data["script"])
                scene_form = form.cleaned_data["scene"]
                scenes = get_scenes(scene_form)

                # Make a new script for every script
                for i in range(len(scripts)):
                    script = Script.objects.create(scene=scenes[i], script=scripts[i], audition=audition)
                    script.save()
            return HttpResponseRedirect(reverse("index"))
        
        # If form was not valid
        else:
            return render(request, "audition/new_audition.html", {
                "form": NewAudition(form),
                "message": "Please make sure all fields are filled out correctly"
            })


# For seperating scripts
def seperate_scripts(script):
    scripts = []
    stop_point = 0
    for i in range(len(script)):
        if script[i:i+3] == "###":
            script_cut = script[stop_point:i-1]
            scripts.append(script_cut)
            stop_point = i + 3
    return scripts


def get_scenes(scene_list):
    scenes = []
    stop_point = 0
    for i in range(len(scene_list)):
        if scene_list[i] == ",":
            scene_cut = scene_list[i][stop_point:i]
            scenes.append(scene_cut)
            stop_point = i + 1
    return scenes


# Edit audition
def edit_auditon(request):
    # Done through JS
    return HttpResponseRedirect(reverse("index"))


# Mark done
def mark_done(request):
    # Done through JS
    return HttpResponseRedirect(reverse("index"))


# Mark undone
def mark_undone(request):
    # Done through JS
    return HttpResponseRedirect(reverse("index"))


# Delete audition
def delete_auditon(request):
    # JS call
    audition = Audition.objects.get(pk=audition_id)
    audition.remove()
    return HttpResponseRedirect(reverse("index"))
