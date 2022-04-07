from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import os
import json

from .forms import NewAudition, Selftapeform
from .models import Audition, User, Script
from .movie import complete, set_end, get_end, time_validate


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
def login_view(request):

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
def logout_view(request):

    # Log the user out and return them to the index
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
            audition = Audition.objects.create(title=form.cleaned_data["title"], role=form.cleaned_data["role"], date=form.cleaned_data["date"], user=user)
            audition.save()

            # Seperate the scripts
            if form.cleaned_data["script"] is not None:
                scripts_form = form.cleaned_data["script"] + '###'
                scripts = seperate_scripts(scripts_form)
                scene_form = form.cleaned_data["scene"] + ','
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
            script_cut = script[stop_point:i]
            scripts.append(script_cut)
            stop_point = i + 3
    return scripts


def get_scenes(scene_list):
    scenes = []
    stop_point = 0
    for i in range(len(scene_list)):
        if scene_list[i] == ",":
            scene_cut = scene_list[stop_point:i]
            scenes.append(scene_cut)
            stop_point = i + 1
    return scenes


# View audition
def view_auditon(request, id):
    audition = Audition.objects.get(pk=id)
    return JsonResponse(audition.serialize())


# Get Scripts
def view_scripts(request, id):
    audition = Audition.objects.get(pk=id)
    scripts = Script.objects.filter(audition=audition)
    return JsonResponse([script.serialize() for script in scripts], safe=False)


# Delete audition
@csrf_exempt
def delete_auditon(request, id):
    
    # Find the audition and delete it
    audition = Audition.objects.get(pk=id)
    audition.delete()
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def save_edit(request):
    
    # Get JSON data
    data = json.loads(request.body)
    script_id = data.get("id", "")
    title = data.get("scene", "")
    script_body = data.get("script", "")

    # Update the script
    script = Script.objects.get(pk=script_id)
    script.scene = title
    script.script = script_body
    script.save()

    # Return response
    return JsonResponse({"message": "Script updated."}, status=201)


# Delete audition
@csrf_exempt
def delete_script(request, id):
    
    # Find the audition and delete it
    audition = Script.objects.get(pk=id)
    audition.delete()
    return JsonResponse({"message": "Script deleted."}, status=201)


@login_required(login_url="login")
def self_tape(request, scene_id):
    
    # For the form to submit video
    if request.method == "GET":
        script = Script.objects.get(pk=scene_id)
        return render(request, "audition/self_tape.html", {
            "script": scene_id,
            "form": Selftapeform()
        })

    # Process the video
    else:

        # Check if the form is valid
        script = Script.objects.get(pk=scene_id)
        audition = Audition.objects.get(pk=script.audition.id)
        user = User.objects.get(pk=audition.user.id)
        form = Selftapeform(request.POST)
        if form.is_valid():

            # Project data
            name = f"{user.first_name} {user.last_name}"
            agent = user.agent
            pin = user.pin
            duration = int(form.cleaned_data["duration"])
            project = audition.title
            role = audition.role
            scene = script.scene
            slate_start = form.cleaned_data["slate_start"]
            slate_end = form.cleaned_data["slate_end"]
                            
            # Set the name for the final edit
            edit_name = (f"{name.upper()} - {role} {project} - {scene}.mp4")

            # Load video
            # Check the user has uploaded a video
            if not request.FILES["clip"]:
                return render(request, "audition/self_tape.html", {
                    "message": "Error uploading video",
                    "script": scene_id,
                    "form": Selftapeform(form)
                })

            clip = request.FILES["clip"]
            store = FileSystemStorage()
            name = store.save(clip.name, clip)
            clip_name = "./files/" + clip.name
            url = store.url(name)

            # Get the crop timings
            # Set the start time
            start = request.POST["start"]
            print(f" start is {start}")
            if start == "":
                start = "00:00.000"

            # Set the end time
            set_end(clip_name)
            end = request.POST["end"]
            if end == "":
                end = get_end()

            # Check if the user has entered valid times
            check = time_validate(start, end)
            if check == "valid":
                start = f"00:{start}"
                end = f"00:{end}"
            else:
                return render(request, "audition/self_tape.html", {
                    "message": check,
                    "script": scene_id
                })

            # Crop the clip and add the slate
            complete(name, agent, pin, project, role, scene, duration, edit_name, clip_name, start, end, slate_start, slate_end)     

            # Delete files made
            #@after_this_request
            #def remove_files(response):
                #os.remove(f'/files/{edit_name}')
                #os.remove(f'/files/{clip_name}')
                #return response

            # Post to /download
            return render(request, "audition/self_tape.html", {
                "script": scene_id,
                "form": Selftapeform(),
                "url": url
            })

        # If the form wasn't valid
        else:
            return render(request, "audition/self_tape.html", {
                "message": "Please fill out all fields correctly.",
                "script": scene_id,
                "form": Selftapeform(form)
            })