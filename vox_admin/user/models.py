from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model."""
    
    username = models.CharField(
        max_length=140,
        error_messages={
            "required": "Ez a mező kötelező.",
        },
        unique=True
    )
    
    def __str__(self):
        return self.username


