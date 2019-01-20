from django.db import models
from django.contrib.auth.models import User
from home.models import Pack,Notification

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bookmarks = models.ManyToManyField(Pack)
    img = models.ImageField(default='default.jpg',upload_to='profile_img')
    followers = models.ManyToManyField(User,related_name='follower_set')

    def __str__(self):
        return f'{self.user.username} Profile'