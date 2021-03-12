from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    contact = models.IntegerField()
    gender = models.CharField(max_length=1)
    dob = models.DateTimeField()

