from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("new_audition", views.new_audtion, name="new_audition"),
    path("self_tape/<str:scene_id>", views.self_tape, name="self_tape"),

    # JS Routes
    path("audition/<int:id>", views.view_auditon, name="audition"),
    path("script/<int:id>", views.view_scripts, name="scripts"),
    path("delete/<int:id>", views.delete_auditon, name="delete"),
    path("save", views.save_edit, name="save"),
    path("delete_script<int:id>", views.delete_script, name="delete_script")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)