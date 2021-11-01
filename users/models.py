from django.db import models
from django.contrib.auth.models import User

# User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    # Profile fields below
