from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    #userName = models.CharField(max_length=128)
    #password = models.CharField(max_length=128)
    #email = models.CharField(max_length=128, blank=True, null=True)
    age = models.IntegerField(default=0)
    preference = models.CharField(max_length=128)
    
    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username 