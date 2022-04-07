from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    agent = models.CharField(max_length=100, null=True, blank=True)
    pin = models.CharField(max_length=11, null=True, blank=True)
    def __str__(self):
        return f"{self.username}"
    pass


class Audition(models.Model):
    title = models.CharField(max_length=64)
    role = models.CharField(max_length=64)
    date = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auditions")

    def __str__(self):
        return f"{self.user} is auditioning for {self.role} in {self.title}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "role": self.role,
            "date": self.date
        }


class Script(models.Model):
    scene = models.CharField(max_length=64)
    script = models.CharField(max_length=1000)
    audition = models.ForeignKey(Audition, on_delete=models.CASCADE, related_name="scenes")

    def __str__(self):
        return f"{self.scene} for {self.audition}"

    def serialize(self):
        return {
            "scene": self.scene,
            "script": self.script,
            "id": self.id
        }
