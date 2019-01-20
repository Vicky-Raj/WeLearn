from django.db import models
from django.contrib.auth.models import User

class Pack(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    date_posted = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='likes_set')

class Link(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=50)
    link = models.URLField()
    text_color = models.CharField(max_length=8,default='#FFFFFF')
    link_color = models.CharField(max_length=8,default='#FFFFFF')
    pack = models.ForeignKey(Pack,on_delete=models.CASCADE)

class Tag(models.Model):
    tag = models.CharField(max_length=100)
    pack = models.ManyToManyField(Pack)
    
    def __str__(self):
        return self.tag

class Notification(models.Model):
    to_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='to_user_set',null=True)
    liked = models.BooleanField(default=False)
    unliked = models.BooleanField(default=False)
    followed = models.BooleanField(default=False)
    unfollowed = models.BooleanField(default=False)
    link_add  = models.BooleanField(default=False)
    new_pack = models.BooleanField(default=False)
    from_user = models.ForeignKey(User,on_delete=models.CASCADE)
    pack = models.ForeignKey(Pack,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    pack = models.ForeignKey(Pack,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    likes = models.ManyToManyField(User,related_name='comment_like_set')
    date = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    likes = models.ManyToManyField(User,related_name='reply_like_set')
    date = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
