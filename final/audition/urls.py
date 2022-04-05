from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("new_audition", views.new_audtion, name="new_audition"),

    # JS Routes
    path("audition/<int:id>", views.view_auditon, name="audition"),
    path("script/<int:id>", views.view_scripts, name="scripts"),
    path("delete/<int:id>", views.delete_auditon, name="delete"),
    path("save", views.save_edit, name="save")
]