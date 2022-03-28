from django.shortcuts import render



# Index request
def index(request):
    return render(request, "audition/index.html")


# Login


# Register


# Logout


# New audition
def new_audtion(request):
    return render(request, "auditon/index.html", {
        "user": user
    })


# Edit audition
def edit_auditon(request):
    return render(request, "audition/index.html", {
        "user": user
    })


# Mark done
def mark_done(request):
    return render(request, "audition/index.html")


# Mark undone
def mark_undone(request):
    return render(request, "audition/index.html", {
        "user": user
    })


# Delete audition
def delete_auditon(request):
    return render(request, "audition/index.html", {
        "user": user
    })