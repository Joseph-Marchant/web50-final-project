from django.contrib import admin

from .models import User, Audition, Script


admin.site.register(User)
admin.site.register(Audition)
admin.site.register(Script)