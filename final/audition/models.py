from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    pass


class Audition(models.Model):
    title = models.CharField(max_length=64)
    role = models.CharField(max_length=64)
    script_1 = models.CharField(max_length=1000, blank=True, null=True)
    script_2 = models.CharField(max_length=1000, blank=True, null=True)
    script_3 = models.CharField(max_length=1000, blank=True, null=True)
    script_4 = models.CharField(max_length=1000, blank=True, null=True)
    script_5 = models.CharField(max_length=1000, blank=True, null=True)
    date = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auditions")

    def __str__(self):
        return f"{self.user} is auditioning for {self.role} in {self.title}"