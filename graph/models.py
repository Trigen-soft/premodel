from django.db import models
from django.contrib.auth.models import User

class GraphModel(models.Model):
    title = models.CharField(max_length=100)
    Date  = models.DateField()
    Revenue = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)