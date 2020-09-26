from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class tweet(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=120, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updatedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.content[:60])

    @property
    def Owner(self):
        return self.User
