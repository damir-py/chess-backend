from django.db import models
from django.contrib.auth import get_user_model

ROLE_CHOICES = (
    (1, 'USER'),
    (2, 'ADMINISTRATOR')
)


class User(get_user_model()):
    Username = models.CharField(max_length=14, unique=True, validators=[])
