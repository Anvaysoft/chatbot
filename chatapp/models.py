from django.db import models

# Create your models here.


class UserDataLog(models.Model):
    user_ip = models.CharField(max_length=10000)
    limit = models.IntegerField(default=0)
    email = models.CharField(max_length=10000, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
