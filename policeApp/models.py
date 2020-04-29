from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PoliceStation(models.Model):
    pid = models.CharField(max_length=8)
    pname = models.CharField(max_length=100)
    district = models.CharField(max_length=30)
    pincode = models.CharField(max_length=6)
    paddress = models.CharField(max_length=150)
    mobile = models.CharField(max_length=13)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)

    def __str__(self):
        return self.pname
