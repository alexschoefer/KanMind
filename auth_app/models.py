from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    #Ein Account gehört genau zu einem User und ein User hat genau einen Account
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=80)

    def __str__(self):
        return self.fullname
