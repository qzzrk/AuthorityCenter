from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    open_id = models.CharField(max_length=64, unique=True, null=True, blank=True)
